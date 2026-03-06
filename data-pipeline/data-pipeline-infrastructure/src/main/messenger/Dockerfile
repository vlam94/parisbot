FROM redis:7-alpine

# Install additional tools
RUN apk add --no-cache \
    curl \
    bash

# Note: Copy configuration if it exists in build context
# COPY conf/redis.conf /usr/local/etc/redis/redis.conf

# Expose Redis port
EXPOSE 6379

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD redis-cli ping

# Default command with config file
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
