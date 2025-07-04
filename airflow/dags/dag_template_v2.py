from airflow.sdk import DAG, task
from pendulum import datetime

with DAG(
        dag_id="dag_template_v2",
        schedule="@daily",
        start_date=datetime(2025, 7, 4),
        description="My Dag Template",
        tags=set("s3"),
        max_consecutive_failed_dag_runs=1
) as dag:
    @task
    def task_one():
        print("this is task one...")
