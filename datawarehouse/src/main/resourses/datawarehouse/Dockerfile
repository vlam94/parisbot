FROM postgres:18-alpine

# Install additional tools
RUN apk add --no-cache \
    postgresql-client \
    curl \
    bash \
    jq

# Create app user
RUN useradd -m -s /bin/bash datawarehouse || true

# Copy configuration files
COPY conf/pg_hba.conf /etc/postgresql/pg_hba.conf

# Copy initialization and post-deploy scripts
COPY *.sql /docker-entrypoint-initdb.d/
COPY post_deploy.sh /usr/local/bin/post_deploy.sh
RUN chmod +x /usr/local/bin/post_deploy.sh

# Set proper permissions
RUN chown -R postgres:postgres /etc/postgresql /docker-entrypoint-initdb.d /usr/local/bin/post_deploy.sh

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD pg_isready -U ${POSTGRES_USER:-datawarehouse} -d ${POSTGRES_DB:-datawarehouse}

# Default command
CMD ["postgres"]
