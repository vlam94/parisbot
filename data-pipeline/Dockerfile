FROM apache/airflow:3.1.8-python3.12

USER airflow
RUN pip install \
        psycopg[binary]==3.3.3\
        psycopg_pool==3.3.0\
        requests-cache==1.3.0

COPY pipeline/src/main/python /opt/airflow