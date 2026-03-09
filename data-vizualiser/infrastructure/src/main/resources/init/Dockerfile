FROM apache/superset:6.0-python3.11

LABEL description="Superset initialization container"

USER root
RUN pip install --no-cache-dir \
    psycopg2-binary==2.9.9

# Copy configuration
COPY ../../superset_config.py /app/pythonpath/

# Set permissions
RUN chown -R superset:superset /app/pythonpath/

USER superset

# Default command for initialization
CMD ["bash", "-c", "superset db upgrade && superset fab create-admin --username admin --password admin --firstname Admin --lastname User --email admin@superset.local || true && superset load_examples || true"]
