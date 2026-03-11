FROM apache/airflow:3.1.8rc2-python3.11

LABEL description="Apache Airflow webserver and scheduler"

USER airflow
RUN pip install --no-cache-dir psycopg[binary]==3.1.9

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["bash", "-c", "airflow db upgrade && airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@airflow.local || true; airflow webserver"]
