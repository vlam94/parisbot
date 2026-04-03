CREATE ROLE datawarehouse WITH LOGIN PASSWORD 'datawarehouse';
GRANT CONNECT ON DATABASE datawarehouse TO datawarehouse;
GRANT USAGE, CREATE ON SCHEMA public TO datawarehouse;
ALTER SCHEMA public OWNER TO datawarehouse;

----------------------------------------------------------------------------------------

CREATE ROLE IF NOT EXISTS writer_group NOLOGIN;
GRANT CONNECT ON DATABASE datawarehouse TO writer_group;
GRANT USAGE ON SCHEMA public TO writer_group;
ALTER DEFAULT PRIVILEGES FOR ROLE writer_group IN SCHEMA public 
GRANT SELECT, INSERT, UPDATE ON TABLES TO datawarehouse;

CREATE ROLE "data-pipeline" WITH LOGIN PASSWORD 'data-pipeline';
GRANT writer_group TO "data-pipeline";

----------------------------------------------------------------------------------------

CREATE ROLE read_only_group NOLOGIN;
GRANT CONNECT ON DATABASE datawarehouse TO read_only_group;
GRANT USAGE ON SCHEMA public TO read_only_group;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_only_group;

CREATE ROLE data_analyst WITH LOGIN PASSWORD 'password123';
GRANT read_only_group TO data_analyst;

-----------------------------------------------------------------------------------------

CREATE SCHEMA meteoblue;
ALTER SCHEMA meteoblue OWNER TO datawarehouse;
GRANT USAGE ON SCHEMA meteoblue TO writer_group, read_only_group;
ALTER DEFAULT PRIVILEGES IN SCHEMA meteoblue GRANT SELECT, INSERT, UPDATE ON TABLES TO writer_group;

