import json
from datetime import datetime, timedelta
import requests

from airflow import DAG, Dataset
from airflow.decorators import task
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

with DAG(
        "fx_producer",
        default_args={"start_date": datetime.now() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task
    def fetch():
        filename = "fx.json"
        response = requests.get("https://open.er-api.com/v6/latest/USD")
        data = response.json()
        rates = data.get("rates", {})

        with open(f"/tmp/{filename}", "w") as fi:
            json.dump(rates, fi)
        return filename


    fetch_task = fetch()

    load = LocalFilesystemToGCSOperator(
        task_id="load",
        src=f"/tmp/{fetch_task}",
        dst="{{ ti.xcom_pull(task_ids='fetch') }}",
        bucket="newagent-90be1.appspot.com",
        gcp_conn_id="BQ",
        outlets=[Dataset("gs://newagent-90be1.appspot.com/fx.json")]
    )

    fetch_task >> load
