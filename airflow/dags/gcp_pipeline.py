from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

with DAG(
        "gcp_pipeline",
        default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    bucket = "newagent-90be1.appspot.com"
    file = "BankData.csv"
    waiting = GCSObjectExistenceSensor(
        task_id="waiting",
        bucket=bucket,
        object=file,
        google_cloud_conn_id="BQ",
        mode="reschedule",
        poke_interval=60,
        timeout=60 * 60 * 3,
        soft_fail=True,
        deferrable=True
    )

    load_table = GCSToBigQueryOperator(
        task_id="load_gcs_to_bq",
        bucket=bucket,
        source_objects=[file],
        destination_project_dataset_table="newagent-90be1.staging.bank_data",
        source_format="CSV",
        skip_leading_rows=1,
        autodetect=True,
        write_disposition="WRITE_TRUNCATE",
        gcp_conn_id="BQ"
    )

    waiting >> load_table
