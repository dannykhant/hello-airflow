from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task


@task
def extract():
    return "This is RAW data."


@task
def transform(raw_data):
    return f"Transformed: {raw_data}"


@task
def validate(processed_data):
    return f"Validated: {processed_data}"


@task
def load(validated_data):
    return f"Data loaded successfully: {validated_data}"


dag = DAG(
    "taskflow_api",
    default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
    schedule="0 23 * * *",
    catchup=False
)

with dag:
    load_task = load(validate(transform(extract())))
