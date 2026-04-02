#!/bin/bash
# File: airflow-init.sh

# Run Airflow init job
cd /home/vlam94/repos/parisbot/data-pipeline
docker run --rm --name airflow-db-migrate --network parisbot-net --env-file .env apache/airflow:3.1.8-python3.12 bash -c "airflow db migrate"