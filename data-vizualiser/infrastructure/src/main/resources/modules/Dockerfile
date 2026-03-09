FROM apache/superset:3.0.0

# Switch to root for package installation
USER root

# Install additional system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    bash \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (celery, redis already in Superset)
RUN pip install --no-cache-dir \
    celery[redis]==5.3.4 \
    redis==5.0.1 \
    gunicorn==21.2.0 \
    psycopg2-binary==2.9.9

# Copy Superset configuration
COPY superset_config.py /app/pythonpath/superset_config.py

# Create app user and set permissions
RUN useradd -m -s /bin/bash superset || true
RUN chown -R superset:superset /app

# Switch back to superset user
USER superset

# Expose Superset port
EXPOSE 8088

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8088/health || exit 1

# Default command
CMD ["gunicorn", "-b", "0.0.0.0:8088", "--workers", "2", "--worker-class", "sync", "--timeout", "120", "superset.app:create_app()"]
