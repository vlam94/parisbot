FROM apache/airflow:3.1-python3.11

LABEL description="Apache Airflow webserver and scheduler"

USER root
RUN pip install --no-cache-dir \
    celery[redis]==5.3.4 \
    redis==5.0.1 \
    psycopg2-binary==2.9.9 \
    pandas==2.0.3

USER airflow

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["bash", "-c", "airflow db upgrade && airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@airflow.local || true; airflow webserver"]
