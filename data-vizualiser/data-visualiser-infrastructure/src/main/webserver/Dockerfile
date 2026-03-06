FROM apache/superset:3.0.0

# Install additional packages if needed
RUN pip install --no-cache-dir \
    celery[redis] \
    psycopg2-binary \
    redis

# Note: Copy Superset configuration if it exists in build context
# COPY superset_config.py /app/pythonpath/superset_config.py

# Expose webserver port
EXPOSE 8088

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=5 \
    CMD curl -f http://localhost:8088/health || exit 1

# Default command
CMD ["superset", "run", "-h", "0.0.0.0", "-p", "8088"]
