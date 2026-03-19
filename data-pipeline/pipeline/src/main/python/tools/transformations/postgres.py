import json
from datetime import datetime

def get_cell_sql(cell, field_type=None):
    if cell is None:
        return None
    elif type(cell) in {list, dict}:
        return json.dumps(cell, ensure_ascii=False)
    elif isinstance(cell, datetime):
        return cell.isoformat()
    elif field_type is not None:
        if field_type in ["boolean", "bool"]:
            return False if str(cell).lower() == 'false' else True
        elif field_type in ["integer", "bigint", "biginteger", "int", "int2", "int4", "int8"]:
            return int(cell)
        elif field_type in ["numeric"]:
            return float(cell)
    else:
        return str(cell)
