FROM apache/superset:3.0.0

# Install Celery and dependencies
RUN pip install --no-cache-dir \
    celery[redis] \
    psycopg2-binary \
    redis

# Expose port if needed
EXPOSE 5555

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:5555/ || exit 1

# Default command - Celery worker
CMD ["celery", "-A", "superset.tasks", "worker", "--loglevel=info", "-c", "4"]
