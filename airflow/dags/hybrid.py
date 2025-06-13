from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator


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
    "hybrid",
    default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
    schedule="0 23 * * *",
    catchup=False
)

with dag:
    load_task = load(validate(transform(extract())))

    bq_task = BigQueryInsertJobOperator(
        task_id="run_query",
        configuration={
            "query": {
                "query": "SELECT 1",
                "useLegacySql": False,
            }
        },
        location="US",
        gcp_conn_id="BQ"
    )

    load_task >> bq_task
