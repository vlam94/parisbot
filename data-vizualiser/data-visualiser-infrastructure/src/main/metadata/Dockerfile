FROM postgres:18-alpine

# Install PostgreSQL client tools
RUN apk add --no-cache \
    postgresql-client \
    curl \
    bash

# Copy configuration files
COPY conf/ /etc/postgresql/

# Copy initialization scripts
COPY *.sql /docker-entrypoint-initdb.d/

# Expose port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD pg_isready -U ${POSTGRES_USER:-superset}

# Default command
CMD ["postgres"]
