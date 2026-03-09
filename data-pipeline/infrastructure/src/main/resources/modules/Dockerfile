FROM apache/airflow:2.8.0-python3.11

# Switch to root for package installation
USER root

# Install additional system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    curl \
    bash \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    celery[redis]==5.3.4 \
    redis==5.0.1 \
    psycopg2-binary==2.9.9 \
    pandas==2.0.3

# Create directories
RUN mkdir -p /opt/airflow/dags /opt/airflow/plugins /opt/airflow/utils && \
    chown -R airflow:airflow /opt/airflow

# Switch back to airflow user
USER airflow

# Expose Airflow port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["webserver"]
