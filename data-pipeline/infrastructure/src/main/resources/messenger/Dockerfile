FROM redis:7-alpine

LABEL description="Redis message broker for Celery task queue"

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD redis-cli ping

# Default Redis command
CMD ["redis-server"]
