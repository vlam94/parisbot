import pandas as pd
from os import environ as env
from utils.transformations.json import unnest_json_columns
from utils.transformations.time import localize_with_numeric_offset_hours
from utils.operators.postgres import RequestToPostgresOperator
from airflow import DAG

cache_expire_seconds = 3600,  # 1h

target_table_current = "meteoblue.current_fact"
target_table_forecast = "meteoblue.forecast_fact"

target_columns_current = {
    "requested_at" :"timestamptz",
    "time" : "timestampt",
    "isobserveddata" : "boolean",
    "metarid" : "varchar",
    "windspeed" : "numeric",
    "zenithangle" : "numeric",
    "pictocode_detailed" :"smallint",
    "pictocode" :"smallint",
    "temperature" :"numeric",
    "latitude" :"numeric",
    "longitude" :"numeric",
    "last_api_update" :"timestamptz",
    "response_generation_ms" :"numeric",
}

target_columns_forecast = {

}

api_key = env.get('METEO_BLUE_API_KEY')
lat, lon = -22.934, -43.180
url = f"https://my.meteoblue.com/packages/current_basic-1h_basic-day?lat={lat}&lon={lon}&apikey={api_key}&forecast_days=1"

def transform_current(data: pd.DataFrame, params: dict = {}) -> pd.DataFrame:

    # Unpacking data from the nested JSON
    data_current = pd.json_normalize(data["data_current"]).reset_index(drop=True)
    data_current = pd.concat([data_current, pd.json_normalize(data["metadata"])], axis=1)

    # Localizing timestamp based on request metadata
    data_current["last_api_update"] = data_current.apply(
    lambda row: localize_with_numeric_offset_hours(row["modelrun_updatetime_utc"], row["utc_timeoffset"]),
    axis=1
    )
    data_current["requested_at"] = data_current.apply(
    lambda row: localize_with_numeric_offset_hours(row["modelrun_utc"], row["utc_timeoffset"]),
    axis=1
    )

    return data_current


def transform_forecast(data: pd.DataFrame, params: dict = {}) -> pd.DataFrame:
    
    # Unpacking data from the nested JSON
    data_forecast = pd.json_normalize(data["data_1h"]).reset_index(drop=True)
    data_forecast = pd.concat([data_forecast, pd.json_normalize(data["metadata"])], axis=1)

    # Localizing timestamp based on request metadata
    data_forecast = pd.json_normalize(data["data_1h"]).reset_index(drop=True)
    forecast_columns = data_forecast.columns.to_list()
    data_forecast = pd.concat([data_forecast, pd.json_normalize(data["metadata"])], axis=1)
    data_forecast["requested_at"] = data_forecast.apply(
        lambda row: localize_with_numeric_offset_hours(row["modelrun_updatetime_utc"], row["utc_timeoffset"]),
        axis=1
    )
    data_forecast = data_forecast.explode(forecast_columns).reset_index(drop=True)
    data_forecast

    return data_forecast

with DAG(
    dag_id="meteoblue_request_to_dw",
    schedule_interval="0 */4 * * *",
    start_date=pd.Timestamp("2020-04-16"),
    catchup=False,
    max_active_runs=1,
) as dag:    
    
    current_task = RequestToPostgresOperator(
        url = url,
        transform_function = transform_current,
        target_table = target_table_current,
        target_columns = target_columns_current,
        cache_expire_seconds= cache_expire_seconds
    )

    forecast_task = RequestToPostgresOperator(
        url = url,
        transform_function = transform_forecast,
        target_table = target_table_forecast,
        target_columns = target_columns_forecast,
        cache_expire_seconds= cache_expire_seconds
    )