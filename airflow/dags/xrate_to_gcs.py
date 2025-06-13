from datetime import datetime, timedelta
import subprocess

from airflow import DAG
from airflow.decorators import task
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

with DAG(
        "xrate_to_gcs",
        default_args={"start_date": datetime.now() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task
    def fetch():
        filename = f"xrate_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
        cmd = ["curl",
               "https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=jsondata",
               "-o", f"/tmp/{filename}"]
        subprocess.run(cmd)
        return filename


    srcfile = fetch()

    load = LocalFilesystemToGCSOperator(
        task_id="load",
        src=f"/tmp/{srcfile}",
        dst="oms/{{ ti.xcom_pull(task_ids='fetch') }}",
        bucket="newagent-90be1.appspot.com",
        gcp_conn_id="BQ"
    )

    srcfile >> load
