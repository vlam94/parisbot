from time import sleep
from pandas import Timestamp
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

def print_hello():
    print("Running task...")  
    sleep(7)
    print("Hello, World!")

with DAG(
    dag_id="hello_world_dag",
    schedule="* * * * *",
    start_date=Timestamp("2020-04-16"),
    catchup=False,
) as dag:
    
    hello_task = PythonOperator(
        task_id="hello_task",
        python_callable=print_hello
    )