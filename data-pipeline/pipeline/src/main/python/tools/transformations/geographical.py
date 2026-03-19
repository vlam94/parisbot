from numpy import round

def get_cardinal_wind_direction(degrees:float) -> str:
    directions = ['N ↓', 'NE ↙', 'E ←', 'SE ↖', 'S ↑', 'SW ↗', 'W →', 'NW ↘']
    idx = round(degrees / 45) % 8
    return directions[int(idx)]

def get_lat_lng_str(coordinates:float,type:str) -> str:
    if not type in ["lat", "lng"]:
        raise ValueError("Type must be 'lat' or 'lng'")
    if type == "lat":
        return f"{abs(coordinates)}°S" if coordinates < 0 else f"{coordinates}°N"
    else:
        return f"{abs(coordinates)}°W" if coordinates < 0 else f"{coordinates}°E"