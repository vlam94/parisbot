FROM postgres:18.3-bookworm

RUN apt-get update && apt-get install -y locales \
    && rm -rf /var/lib/apt/lists/*

RUN sed -i '/pt_BR.UTF-8/s/^# //g' /etc/locale.gen && locale-gen

COPY conf/*.conf /tmp/
RUN chown -R postgres:postgres /tmp/

CMD ["postgres", "-c", "config_file=/tmp/postgresql.conf"]