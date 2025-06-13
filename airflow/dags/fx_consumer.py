from datetime import datetime, timedelta

from airflow import DAG, Dataset
from airflow.decorators import task
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook

with DAG(
        "fx_consumer",
        default_args={"start_date": datetime.now() - timedelta(days=1)},
        schedule=[Dataset("gs://newagent-90be1.appspot.com/fx.json")]
) as dag:
    start = EmptyOperator(task_id="start")


    @task
    def load():
        hook = BigQueryHook(gcp_conn_id="BQ")

        job_config = {
            "load": {
                "sourceUris": ["gs://newagent-90be1.appspot.com/fx.json"],
                "destinationTable": {
                    "projectId": "newagent-90be1",
                    "datasetId": "staging",
                    "tableId": "forex"
                },
                "sourceFormat": "NEWLINE_DELIMITED_JSON",
                "writeDisposition": "WRITE_TRUNCATE",
                "autodetect": True
            }
        }

        hook.insert_job(configuration=job_config, location="US")


    start >> load()
