from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

with DAG(
        "depends_on_past",
        default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task
    def task_a():
        print("Task A")


    @task(depends_on_past=True)
    def task_b():
        print("Task B")


    task_a() >> task_b()
