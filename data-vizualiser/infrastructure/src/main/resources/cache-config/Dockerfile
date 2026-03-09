FROM rediscommander/redis-commander:latest

LABEL description="Redis Commander for cache inspection and debugging (optional)"

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:8081 || exit 1

# Environment variables are passed at runtime
