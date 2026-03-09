FROM postgres:18-alpine

LABEL description="PostgreSQL database for Superset metadata store"

# Copy configuration files
COPY ../../../conf/pg_hba.conf /etc/postgresql/
COPY ../../../conf/postgresql.conf /etc/postgresql/

# Set proper permissions
RUN chown postgres:postgres /etc/postgresql/* && \
    chmod 644 /etc/postgresql/*

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD pg_isready -U superset -d superset

# Default command
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]
