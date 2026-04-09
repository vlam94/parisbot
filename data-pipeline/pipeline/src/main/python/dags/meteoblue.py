import pandas as pd
from os import environ as env
from datetime import timedelta
from tools.transformations.time import convert_utc_timestamp_with_offset_hours, localize_timestamp_with_offset_hours
from tools.transformations.generic import int_to_bool
from tools.operators.postgres import RequestToPostgresOperator
from airflow.sdk import DAG

cache_expire_seconds = 7200  # 2h

target_table_current = "meteoblue.current_fact"
target_table_forecast = "meteoblue.forecast_fact"

target_columns_current = {
    "requested_at" :"timestamptz",
    "weather_data_time" : "timestamptz",
    "isobserveddata" : "boolean",
    "metarid" : "varchar",
    "windspeed" : "numeric",
    "zenithangle" : "numeric",
    "pictocode_detailed" :"smallint",
    "pictocode" :"smallint",
    "temperature" :"numeric",
    "geo_coordinates" :"varchar",
    "last_api_update" :"timestamptz",
    "response_generation_ms" :"numeric",
}

target_columns_forecast = {
    "requested_at": "timestamptz",
    "forecast_time": "timestamptz",
    "windspeed": "numeric",
    "temperature": "numeric",
    "precipitation_probability": "numeric",
    "rainspot": "numeric",
    "pictocode": "smallint",
    "felttemperature": "numeric",
    "precipitation": "numeric",
    "relativehumidity": "numeric",
    "winddirection": "numeric",
    "geo_coordinates": "varchar",
}

def transform_current(data: pd.DataFrame, params: dict = {}) -> pd.DataFrame:

    # Unpacking data from the nested JSON
    data_current = pd.json_normalize(data["data_current"]).reset_index(drop=True)
    data_current = pd.concat([data_current, pd.json_normalize(data["metadata"])], axis=1)

    # Localizing timestamp based on request metadata
    data_current["last_api_update"] = data_current.apply(
    lambda row: convert_utc_timestamp_with_offset_hours(row["modelrun_updatetime_utc"], row["utc_timeoffset"]),
    axis=1
    )
    data_current["requested_at"] = data_current.apply(
    lambda row: convert_utc_timestamp_with_offset_hours(row["modelrun_utc"], row["utc_timeoffset"]),
    axis=1
    )
    data_current["weather_data_time"] = data_current.apply(
    lambda row: localize_timestamp_with_offset_hours(row["time"], row["utc_timeoffset"]),
    axis=1
    )

    # Converting numeric boolean (0,1) to bool (True,False)
    data_current["isobserveddata"] = data_current["isobserveddata"].apply(int_to_bool)

    data_current = data_current.rename(columns={
        'generation_time_ms': 'response_generation_ms',
    })

    data_current['geo_coordinates'] = data_current['latitude'].astype(str) + ',' + data_current['longitude'].astype(str)

    return data_current


def transform_forecast(data: pd.DataFrame, params: dict = {}) -> pd.DataFrame:
    
    # Unpacking data from the nested JSON
    data_forecast = pd.json_normalize(data["data_1h"]).reset_index(drop=True)
    data_forecast = pd.concat([data_forecast, pd.json_normalize(data["metadata"])], axis=1)
    data_forecast = pd.json_normalize(data["data_1h"]).reset_index(drop=True)

    forecast_columns = data_forecast.columns.to_list()
    # Converting timestamp based on request metadata 
    data_forecast = pd.concat([data_forecast, pd.json_normalize(data["metadata"])], axis=1)
    data_forecast["requested_at"] = data_forecast.apply(
        lambda row: convert_utc_timestamp_with_offset_hours(row["modelrun_updatetime_utc"], row["utc_timeoffset"]),
        axis=1
    )

    data_forecast['geo_coordinates'] = data_forecast['latitude'].astype(str) + ',' + data_forecast['longitude'].astype(str)

    data_forecast = data_forecast.explode(forecast_columns).reset_index(drop=True)

    data_forecast["forecast_time"] = data_forecast.apply(
    lambda row: localize_timestamp_with_offset_hours(row["time"], row["utc_timeoffset"]),
    axis=1
    )
    data_forecast = data_forecast[data_forecast['forecast_time'] >= data_forecast['requested_at']].reset_index(drop=True)

    return data_forecast

api_key = env.get('METEO_BLUE_API_KEY')
lat, lon = -22.934, -43.180
url = f"https://my.meteoblue.com/packages/current_basic-1h_basic-day?lat={lat}&lon={lon}&apikey={api_key}&forecast_days=1"

with DAG(
    dag_id="meteoblue_request_to_dw",
    schedule="0 */4 * * *",
    start_date=pd.Timestamp("2020-04-16"),
    catchup=False,
) as dag:    
    
    current_task = RequestToPostgresOperator(
        task_id = "current_data",
        url = url,
        transform_function = transform_current,
        target_table = target_table_current,
        target_columns = target_columns_current,
        target_table_merge=True,
        cache_expire_seconds= cache_expire_seconds,
        retries = 5,
        retry_delay = timedelta(minutes=10)
    )

    forecast_task = RequestToPostgresOperator(
        task_id = "forecast_data",
        url = url,
        transform_function = transform_forecast,
        target_table = target_table_forecast,
        target_columns = target_columns_forecast,
        target_table_merge=True,
        cache_expire_seconds= cache_expire_seconds,
        retries = 5,
        retry_delay = timedelta(minutes=20)
    )

    current_task >> forecast_task