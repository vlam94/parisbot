import time
from numpy import nan as np_nan
import logging
import pandas as pd


def isnull(value):
    return pd.isnull(value) or value == {} or value == tuple() or value == [] or value == [{}]

def transform_and_clean_data(
        data: pd.DataFrame,
        transform_function: callable = None,
        parameters:dict = None,
        target_fields: list[str] = None,
        clean: bool = False
        ) -> pd.DataFrame:
    if data.empty:
        logging.info("No data to process, returning empty DataFrame.")
        return data

    logging.info("Starting to process %s rows", len(data))
    start_time = time.time()

    if transform_function:
        data = transform_function(data, parameters)

    if target_fields:
        data = data[target_fields]

    if clean:
        data = data.replace({pd.NA: None, pd.NaT: None, np_nan: None, })

    end_time = time.time()
    elapsed_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
    logging.info("Done processing.\nTotal rows after processing: %s\nElapsed time: %s", len(data), elapsed_time)

    return data

def int_to_bool(value):
    if isinstance(value, int):
        return bool(value)
    return None