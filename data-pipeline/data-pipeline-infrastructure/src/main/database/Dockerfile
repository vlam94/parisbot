FROM postgres:18-alpine

# Set environment variables
ENV POSTGRES_USER=parisbot \
    POSTGRES_PASSWORD=parisbot_secure_123 \
    POSTGRES_DB=parisbot \
    POSTGRES_INITDB_ARGS="-c shared_preload_libraries=pg_stat_statements"

# Install additional useful tools
RUN apk add --no-cache \
    postgresql-client \
    curl \
    bash

# Copy configuration files
COPY conf/postgresql.conf /etc/postgresql/postgresql.conf
COPY conf/pg_hba.conf /etc/postgresql/pg_hba.conf

# Ensure proper permissions
RUN chown postgres:postgres /etc/postgresql/*.conf

# Copy initialization script if needed
COPY --chown=postgres:postgres docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB

# Default command
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
