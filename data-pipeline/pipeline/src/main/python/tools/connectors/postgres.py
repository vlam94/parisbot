import time
from os import environ as env
from copy import deepcopy
from typing import Iterable
from airflow.models import Connection
from airflow.providers.postgres.hooks.postgres import PostgresHook
from psycopg_pool import ConnectionPool
import psycopg
from tools.transformations.postgres import get_cell_sql


class PostgresPooledHook(PostgresHook):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._conn_obj: Connection | None = kwargs.pop("connection", None)
        self._session: psycopg.Connection = None
        self._db_name: str | None = kwargs.pop("database", None)

        self.min_pool_connections = 2,
        self.max_pool_connections = int(env.get("PG_CONN_POOL_LIMIT", 8)),
        self.lifetime_limit = float(60 * 60 * 6),
        self.idle_limit = float(60 * 12),
        self.prep_level = 0,
        self.auto_commit_mode = False,
        self.conn_timeout_sec = 40.0,
        self.pool_map = dict()

    def __create_pool(self, conn_id):
        conn = deepcopy(self._conn_obj or self.get_connection(conn_id))
        conn_args = dict(
            host=conn.host,
            user=conn.login,
            password=conn.password,
            dbname=self._db_name or conn.schema,
            port=conn.port,
            autocommit=self.auto_commit_mode,
            prepare_threshold=self.prep_level,
        )
        return ConnectionPool(
            min_size=self.min_pool_connections,
            max_size=self.max_pool_connections,
            max_lifetime=self.lifetime_limit,
            max_idle=self.idle_limit,
            timeout=self.conn_timeout_sec,
            kwargs=conn_args,
        )

    def __ensure_pool(self):
        pool = PostgresPooledHook.pool_map.get(self.postgres_conn_id)
        if pool is None:
            PostgresPooledHook.pool_map[self.postgres_conn_id] = self.__create_pool(self.postgres_conn_id)
        else:
            with pool.connection() as conn:
                try:
                    conn.execute("SELECT 'foo'")
                except Exception:
                    PostgresPooledHook.pool_map[self.postgres_conn_id] = self.__create_pool(self.postgres_conn_id)

    def __get_session(self) -> psycopg.Connection:
        self.__ensure_pool()
        self._session = PostgresPooledHook.pool_map[self.postgres_conn_id].connection()
        return self._session

    @staticmethod
    def __format_cell(value, dtype=None, conn=None) -> str | None:
        return get_cell_sql(value, field_type=dtype, conn=conn)

    @classmethod
    def _compose_columns(
        self,
        fields: Iterable[str],
        with_type: bool = False,
        with_cast: bool = False,
        as_var: bool = False,
    ) -> str:
        seq = ""
        if fields is not None:
            for field in fields:
                if isinstance(fields, dict) and with_cast:
                    seq += f"%({field})s::{fields[field]}, " if as_var else f"{field}::{fields[field]}, "
                elif isinstance(fields, dict) and with_type:
                    seq += f"{field} {fields[field]}, "
                else:
                    seq += f"{field}, "
            seq = seq[:-2]
        return seq
    
    def merge_data_with_copy(self, table_name: str, fields: dict[str, str], data: list[dict], table_pk: list[str], vacuum: bool = False):
        conn = self.__get_session()
        with conn.cursor() as cur:
            temp_table_name = f"{table_name}_temp_{int(time.time())}"
            create_temp_table_sql = f"CREATE TEMP TABLE {temp_table_name} ({self._compose_columns(fields, with_type=True)}) ON COMMIT DROP;"
            cur.execute(create_temp_table_sql)

            copy_sql = f"COPY {temp_table_name} ({self._compose_columns(fields)}) FROM STDIN WITH (FORMAT csv, DELIMITER '|', NULL '');"
            with cur.copy(copy_sql) as copy:
                for row in data:
                    formatted_row = [self.__format_cell(row.get(field), dtype=fields.get(field), conn=conn) for field in fields]
                    copy.write_row(formatted_row)

            merge_sql = f"""
                INSERT INTO {table_name} ({self._compose_columns(fields)})
                SELECT {self._compose_columns(fields)}
                FROM {temp_table_name}
                ON CONFLICT ({', '.join(table_pk)}) DO UPDATE SET
                {', '.join([f"{field} = EXCLUDED.{field}" for field in fields if field not in table_pk])};
            """
            cur.execute(merge_sql)
        
        if vacuum:
            self.run_vacuum(table_name)

    def run_vacuum(self, table_name):
        conn = deepcopy(self._conn_obj or self.get_connection(self.postgres_conn_id))
        conn_args = dict(
            host=conn.host,
            user=conn.login,
            password=conn.password,
            dbname=self._db_name or conn.schema,
            port=conn.port,
        )
        with psycopg.Connection.connect(autocommit=True, **conn_args) as conn:
            start = time.time()
            cur = conn.cursor()
            cur.execute("SET statement_timeout = 3600000")
            cur.execute(f"VACUUM VERBOSE ANALYZE {table_name}")
            elapsed = time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
            self.log.info("Vacuum finished for %s in %s", table_name, elapsed)
