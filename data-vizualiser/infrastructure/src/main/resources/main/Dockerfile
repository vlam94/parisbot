FROM apache/superset:6.0-python3.11

LABEL description="Apache Superset webserver for data visualization"

USER root
RUN pip install --no-cache-dir \
    celery[redis]==5.3.4 \
    redis==5.0.1 \
    gunicorn==21.2.0 \
    psycopg2-binary==2.9.9

# Copy Superset configuration
COPY ../../superset_config.py /app/pythonpath/

# Set permissions
RUN chown -R superset:superset /app/pythonpath/

USER superset

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8088/health || exit 1

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8088", "--workers", "2", "--worker-class", "sync", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "superset.app:create_app()"]
