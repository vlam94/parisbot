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

    min_connections = 2
    max_connections = int(env.get("PG_CONN_POOL_LIMIT", 8))
    lifetime_limit = float(60 * 60 * 6)
    idle_limit = float(60 * 12)
    prep_level = 0
    auto_commit_mode = False
    conn_timeout_sec = 40.0
    pool_map = dict()

    conn_attr = "postgres_conn_id"
    default_conn = "postgres_default"
    conn_type = "postgres"
    hook_alias = "Postgres"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._conn_obj: Connection | None = kwargs.pop("connection", None)
        self._session: psycopg.Connection = None
        self._db_name: str | None = kwargs.pop("database", None)

    def _create_pool(self, conn_id):
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
            min_connections=self.min_connections,
            max_connections=self.max_connections,
            max_lifetime=self.lifetime_limit,
            max_idle=self.idle_limit,
            timeout=self.conn_timeout_sec,
            kwargs=conn_args,
        )

    def ensure_pool(self):
        conn_id = getattr(self, self.conn_attr)
        pool = PostgresPooledHook.pool_map.get(conn_id)
        if pool is None:
            PostgresPooledHook.pool_map[conn_id] = self._create_pool(conn_id)
        else:
            with pool.connection() as conn:
                try:
                    conn.execute("SELECT 'foo'")
                except Exception:
                    PostgresPooledHook.pool_map[conn_id] = self._create_pool(conn_id)

    def get_session(self) -> psycopg.Connection:
        self.ensure_pool()
        conn_id = getattr(self, self.conn_attr)
        self._session = PostgresPooledHook.pool_map[conn_id].connection()
        return self._session

    @staticmethod
    def _format_cell(value, dtype=None, conn=None) -> str | None:
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

    def run_vacuum(self, table_name):
        conn_id = getattr(self, self.conn_attr)
        conn = deepcopy(self._conn_obj or self.get_connection(conn_id))
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
