CREATE TABLE IF NOT EXISTS meteoblue.current_fact (
    requested_at TIMESTAMPTZ,
    api_system_time TIMESTAMPTZ,
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