import pandas as pd
from utils.connectors.postgres import PostgresPooledHook
from utils.transformations.generic import transform_and_clean_data
from requests_cache import CachedSession

class RequestToPostgresOperator():
    
    def _get_request_data(self, url: str) -> pd.DataFrame:
        session = CachedSession(cache_name='.cache', expire_after=3600)
        response = session.get(url)
        response.raise_for_status()
        return pd.DataFrame([response.json()])
    
    def __init__(
        self,
        url: str,
        target_table: str,
        target_columns: dict[str, str],

        transform_function: callable = None,
        transform_parameters: dict = {},
        target_postgres_conn_id: str='datawarehouse',
        target_table_pk: list=['uploaded_at'],
        target_table_merge: bool=False,
        target_vacuum: bool=False,
        *args, **kwargs):

        super(RequestToPostgresOperator, self).__init__(*args, **kwargs)

        self.url = url
        self.target_table = target_table
        self.target_columns = target_columns
        self.transform_function = transform_function
        self.transform_parameters = transform_parameters
        self.target_postgres_conn_id = target_postgres_conn_id
        self.target_table_merge = target_table_merge
        self.target_table_pk = target_table_pk
        self.target_vacuum = target_vacuum
    
    def execute(self, context):
        data = self._get_request_data(self.url)

        data = transform_and_clean_data(
            data=data,
            transform_function=self.transform_function,
            target_fields=self.target_columns,
            clean=True,
            parameters=self.transform_parameters,
        )
        conn = PostgresPooledHook(postgres_conn_id=self.target_postgres_conn_id)

        if self.target_table_merge:
            conn.merge_rows_with_copy(
                table_name=self.target_table,
                fields=self.target_columns,
                data=data.to_dict('records'),
                table_pk=self.target_table_pk,
                vacuum=self.target_vacuum
            )
        else:
            conn.insert_rows(
                table_name=self.target_table,
                fields=self.target_columns,
                data=data,
                execute_many = True,
            )