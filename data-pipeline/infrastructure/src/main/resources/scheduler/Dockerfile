FROM apache/airflow:3.1.8rc2-python3.11

LABEL description="Celery Beat scheduler for periodic task execution"

USER airflow
RUN pip install --no-cache-dir psycopg[binary]==3.1.9

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5555/api/workers/ 2>/dev/null | grep -q active || exit 1

# Default command for Celery Beat
CMD ["celery", "-A", "airflow.executors.celery_executor", "beat", "--loglevel=info"]
