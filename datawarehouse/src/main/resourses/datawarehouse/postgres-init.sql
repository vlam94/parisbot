-- PostgreSQL Initialization Script
-- Create superset database and role if they don't exist

-- Create superset database
CREATE DATABASE IF NOT EXISTS superset;

-- Create superset role if it doesn't exist
DO
$$
BEGIN
  IF NOT EXISTS (
    SELECT FROM pg_catalog.pg_roles
    WHERE rolname = 'superset'
  ) THEN
    CREATE ROLE superset WITH LOGIN PASSWORD 'airflow';
  END IF;
END
$$;

-- Grant privileges
ALTER DATABASE superset OWNER TO postgres;
GRANT ALL PRIVILEGES ON DATABASE superset TO postgres;
GRANT CONNECT ON DATABASE superset TO superset;

-- Connect to superset database and grant schema privileges
\c superset;
GRANT USAGE ON SCHEMA public TO superset;
GRANT CREATE ON SCHEMA public TO superset;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO superset;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO superset;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO superset;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO superset;

-- Return to airflow database
\c airflow;
