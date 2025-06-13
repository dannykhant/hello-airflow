from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.standard.operators.empty import EmptyOperator

with DAG(
        "gcs_trans",
        default_args={"start_date": datetime.now() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    start = EmptyOperator(task_id="start")


    @task
    def trans():
        hook = GCSHook(gcp_conn_id="BQ")
        content = hook.download(
            bucket_name="newagent-90be1.appspot.com",
            object_name="input.txt").decode("utf-8")
        transformed_content = content.upper()
        hook.upload(data=transformed_content,
                    bucket_name="newagent-90be1.appspot.com",
                    object_name="output.txt")


    start >> trans()
