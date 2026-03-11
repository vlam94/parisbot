FROM apache/airflow:3.1.8rc2-python3.11

LABEL description="Celery worker for async task execution"

USER airflow
RUN pip install --no-cache-dir \
    psycopg[binary]==3.1.9

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD ps aux | grep 'celery.*worker' | grep -v grep || exit 1

# Default command for Celery Worker
CMD ["celery", "-A", "airflow.executors.celery_executor", "worker", "--loglevel=info", "--concurrency=2"]
