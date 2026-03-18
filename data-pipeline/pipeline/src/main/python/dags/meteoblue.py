import pandas as pd
from os import environ as env
from utils.transformations.json import unnest_json_columns
from utils.operators.postgres import RequestToPostgresOperator
from airflow import DAG

target_table = "meteoblue.request_fact"
target_columns = {}
api_key = env.get('METEO_BLUE_API_KEY')
lat, lon = -22.934, -43.180
url = f"https://my.meteoblue.com/packages/current_basic-1h_basic-day?lat={lat}&lon={lon}&apikey={api_key}&forecast_days=1"

def transform(data: pd.DataFrame, params: dict = {}) -> pd.DataFrame:
    mapping = {
        
    }

with DAG(
    dag_id="meteoblue_request_to_dw",
    schedule_interval="0 */4 * * *",
    start_date=pd.Timestamp("2020-04-16"),
    catchup=False,
    max_active_runs=1,
) as dag:    
    request_task = RequestToPostgresOperator(
        url = url,
        transform_function = transform,
        target_table = target_table,
        target_columns = target_columns,
    )