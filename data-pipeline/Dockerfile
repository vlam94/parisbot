FROM apache/airflow:3.1.7-python3.11

USER root:root
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils curl libgomp1

USER airflow
RUN pip install \
		apache-airflow[statsd]==3.1.7\ 
        psycopg[binary]==3.1.9\
        requests-cache==1.3.0

COPY pipeline/src/main/python /opt/airflow