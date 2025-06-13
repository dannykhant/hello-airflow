from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

dag = DAG(
    "traditional",
    default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
    schedule="0 23 * * *",
    catchup=False
)


def extract(ti):
    raw_data = "This is RAW data."
    ti.xcom_push(key="raw", value=raw_data)


def transform(ti):
    raw_data = ti.xcom_pull(task_ids="extract", key="raw")
    processed_data = f"Processed: {raw_data}"
    ti.xcom_push(key="processed", value=processed_data)


def validate(ti):
    process_data = ti.xcom_pull(task_ids="transform", key="processed")
    validated_data = f"Validated: {process_data}"
    ti.xcom_push(key="validated", value=validated_data)


def load(ti):
    validated_data = ti.xcom_pull(task_ids="validate", key="validated")
    print(f"Data loaded successfully: {validated_data}")


extract_task = PythonOperator(
    task_id="extract",
    python_callable=extract,
    dag=dag
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=transform,
    dag=dag
)

validate_task = PythonOperator(
    task_id="validate",
    python_callable=validate,
    dag=dag
)

load_task = PythonOperator(
    task_id="load",
    python_callable=load,
    dag=dag
)

extract_task >> transform_task >> validate_task >> load_task
