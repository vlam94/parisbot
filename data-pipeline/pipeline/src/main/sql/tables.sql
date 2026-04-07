-- METEOBLUE CURRENT TASK 
CREATE TABLE IF NOT EXISTS meteoblue.current_fact (
    requested_at TIMESTAMPTZ,
    weather_data_time TIMESTAMPTZ,
    isobserveddata BOOLEAN,
    metarid VARCHAR(50),
    windspeed NUMERIC,
    zenithangle NUMERIC,
    pictocode_detailed SMALLINT,
    pictocode SMALLINT,
    temperature NUMERIC,
    latitude NUMERIC,
    longitude NUMERIC,
    last_api_update TIMESTAMPTZ,
    response_generation_ms NUMERIC
);
ALTER TABLE meteoblue.current_fact OWNER TO datawarehouse;

-- METEOBLUE FORECAST TASK
CREATE TABLE IF NOT EXISTS meteoblue.forecast_fact (
    requested_at TIMESTAMPTZ,
    forecast_time TIMESTAMPTZ,
    windspeed NUMERIC,
    temperature NUMERIC,
    precipitation_probability NUMERIC,
    rainspot NUMERIC,
    pictocode SMALLINT,
    felttemperature NUMERIC,
    precipitation NUMERIC,
    relativehumidity NUMERIC,
    winddirection NUMERIC,
    geo_coordinates VARCHAR
);
ALTER TABLE meteoblue.forecast_fact OWNER TO datawarehouse;