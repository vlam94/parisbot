#!/bin/bash
# File: airflow-init.sh

# Run Airflow init job
docker run --rm \
  --name airflow-init \
  --network=parisbot-net \
  -e AIRFLOW__CORE__EXECUTOR=LocalExecutor \
  -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@airflow-database:5432/airflow \
  apache/airflow:3.1.7-python3.11 \
  bash -c "airflow db migrate"