FROM postgres:18-alpine

# Copy configuration files
COPY conf/pg_hba.conf /etc/postgresql/
COPY conf/postgresql.conf /etc/postgresql/

# Set proper permissions
RUN chown postgres:postgres /etc/postgresql/* && \
    chmod 644 /etc/postgresql/*

# Health check to verify PostgreSQL is ready
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD pg_isready -U postgres

# Default command
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf", "-c", "hba_file=/etc/postgresql/pg_hba.conf"]
