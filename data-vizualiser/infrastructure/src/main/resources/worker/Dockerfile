FROM apache/superset:6.0-python3.11

LABEL description="Celery worker for Superset async query execution"

USER root
RUN pip install --no-cache-dir \
    celery[redis]==5.3.4 \
    redis==5.0.1 \
    psycopg2-binary==2.9.9
USER superset

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD ps aux | grep 'celery.*worker' | grep -v grep || exit 1

# Default command for Celery Worker
CMD ["celery", "--app", "superset.tasks.celery_app:app", "worker", "--loglevel=info", "--concurrency=2"]
