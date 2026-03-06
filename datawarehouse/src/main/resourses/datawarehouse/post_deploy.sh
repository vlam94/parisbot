#!/bin/bash
# Post-deployment setup script for datawarehouse
# This script runs after PostgreSQL initialization

set -e

POSTGRES_USER="${POSTGRES_USER:-datawarehouse}"
POSTGRES_DB="${POSTGRES_DB:-datawarehouse}"

echo "🔧 Running datawarehouse post-deployment setup..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB" &>/dev/null; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
done
echo "✓ PostgreSQL is ready"

# Create extensions if needed
echo "📦 Creating PostgreSQL extensions..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" << EOF
    CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    CREATE EXTENSION IF NOT EXISTS uuid-ossp;
    CREATE EXTENSION IF NOT EXISTS hstore;
    CREATE EXTENSION IF NOT EXISTS json;
EOF

# Create schemas
echo "📋 Creating datawarehouse schemas..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" << EOF
    CREATE SCHEMA IF NOT EXISTS raw_data AUTHORIZATION "$POSTGRES_USER";
    CREATE SCHEMA IF NOT EXISTS staging AUTHORIZATION "$POSTGRES_USER";
    CREATE SCHEMA IF NOT EXISTS analytics AUTHORIZATION "$POSTGRES_USER";
    CREATE SCHEMA IF NOT EXISTS metadata AUTHORIZATION "$POSTGRES_USER";
    
    -- Grant permissions
    GRANT USAGE ON SCHEMA raw_data, staging, analytics, metadata TO "$POSTGRES_USER";
    GRANT CREATE ON SCHEMA raw_data, staging, analytics, metadata TO "$POSTGRES_USER";
EOF

# Create base tables/metadata
echo "🗄️  Creating metadata tables..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" << EOF
    CREATE TABLE IF NOT EXISTS metadata.schema_versions (
        id SERIAL PRIMARY KEY,
        schema_name VARCHAR(255) NOT NULL,
        version VARCHAR(50) NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        applied_by VARCHAR(255),
        description TEXT
    );
    
    CREATE TABLE IF NOT EXISTS metadata.data_sources (
        id SERIAL PRIMARY KEY,
        source_name VARCHAR(255) NOT NULL UNIQUE,
        source_type VARCHAR(50),
        connection_string TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT true
    );
    
    CREATE TABLE IF NOT EXISTS metadata.etl_runs (
        id SERIAL PRIMARY KEY,
        job_name VARCHAR(255) NOT NULL,
        status VARCHAR(50),
        started_at TIMESTAMP,
        ended_at TIMESTAMP,
        record_count INTEGER,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
EOF

echo "✅ Datawarehouse post-deployment setup completed successfully!"
