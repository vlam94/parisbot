from pandas import to_datetime, Timestamp 
from numpy import datetime64 
from datetime import datetime ,timezone, timedelta
from tools.transformations.generic import isnull

def is_timestamp(val):
    return isinstance(val, (datetime, Timestamp, datetime64))

def convert_utc_timestamp_with_offset_hours(dt: datetime, offset_hours: float = 0):
    
    if isinstance(dt, str):
        dt = to_datetime(dt)

    if isnull(dt) or not is_timestamp(dt):
        return dt
    tz_offset_hours = timezone(timedelta(hours=offset_hours))
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(tz_offset_hours)

def localize_timestamp_with_offset_hours(dt: datetime, offset_hours: float = 0):
    
    if isinstance(dt, str):
        dt = to_datetime(dt)

    if isnull(dt) or not is_timestamp(dt):
        return dt
    tz_offset_hours = timezone(timedelta(hours=offset_hours))
    return dt.tz_localize(tz_offset_hours)