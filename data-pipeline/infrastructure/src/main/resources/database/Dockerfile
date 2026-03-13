FROM postgres:18.3-bookworm

COPY conf/*.conf /tmp/
RUN chown -R postgres:postgres /tmp/

CMD ["postgres", "-c", "config_file=/tmp/postgresql.conf"]