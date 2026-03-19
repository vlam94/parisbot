from pandas import Timestamp as pd_Timestamp
from numpy import datetime64 as np_datetime64
from datetime import datetime ,timezone, timedelta
from tools.transformations.generic import isnull

def is_timestamp(val):
    return isinstance(val, (datetime, pd_Timestamp, np_datetime64))

def localize_with_numeric_offset_hours(dt: datetime, offset_hours: float = 0):
    if isnull(dt) or not is_timestamp(dt):
        return dt
    tz_offset_hours = timezone(timedelta(hours=offset_hours))
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(tz_offset_hours)