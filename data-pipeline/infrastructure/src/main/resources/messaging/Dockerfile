FROM redis:8.2-bookworm

USER root

COPY redis.conf /usr/local/etc/redis/redis.conf

RUN chown redis:redis /usr/local/etc/redis/redis.conf

EXPOSE 6379

USER redis

CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]