FROM apache/superset:3.0.0

# Install query engine and database drivers
RUN pip install --no-cache-dir \
    sqlalchemy \
    psycopg2-binary \
    pymysql \
    redis \
    requests \
    celery[redis]

# Note: Copy query configuration if it exists in build context
# COPY config/ /app/query_config/

# Expose monitoring port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Default command - Celery beat scheduler for query execution
CMD ["celery", "-A", "superset.tasks", "beat", "--loglevel=info"]
