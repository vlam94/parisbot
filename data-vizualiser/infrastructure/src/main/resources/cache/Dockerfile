FROM redis:7-alpine

LABEL description="Redis cache for Superset query results and sessions"

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD redis-cli ping

# Default Redis command
CMD ["redis-server"]
