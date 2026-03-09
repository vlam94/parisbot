FROM apache/superset:6.0-python3.11

LABEL description="Celery Beat scheduler for Superset report scheduling"

USER root
RUN pip install --no-cache-dir \
    celery[redis]==5.3.4 \
    redis==5.0.1
USER superset

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD ps aux | grep 'celery.*beat' | grep -v grep || exit 1

# Default command for Celery Beat
CMD ["celery", "--app", "superset.tasks.celery_app:app", "beat", "--loglevel=info"]
