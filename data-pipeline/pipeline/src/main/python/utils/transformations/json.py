import json
import pandas as pd
from utils.transformations.generic import isnull

def check_and_load_json_obj(value: str|dict|None) -> dict|None:
    if isinstance(value, str):
        return json.loads(value)
    return value    
    

def get_nested_json_data(json_obj: dict, path: tuple):
    print(f"Accessing path {path} in JSON object: {json_obj}")
    if isnull(json_obj):
        return None
    if isnull(path):
        return json_obj
    if not isinstance(json_obj, (dict, list)):
        return None
    key = path[0]
    try:
        return get_nested_json_data(json_obj[key], path[1:])
    except:
        print(f"Error accessing key '{key}' in JSON object: {json_obj}")

def unnest_json_columns(data: pd.DataFrame, mapping: dict[str, tuple[str, tuple]]) -> pd.DataFrame:
    for col in set(mapping.values()[0]):
        data[col] = data[col].apply(check_and_load_json_obj)
    for new_col, (df_col, path) in mapping.items():
        data[new_col] = data[df_col].apply(lambda x: get_nested_json_data(x, path))
    return data

    