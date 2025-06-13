from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.email import send_email
from airflow.sdk import Variable

with DAG(
        "bq_exec",
        default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    query_task = BigQueryInsertJobOperator(
        task_id="query",
        configuration={
            "query": {
                "query": """
                    SELECT
                      *
                    FROM
                      `bigquery-public-data.bbc_news.fulltext`
                    WHERE
                      category = 'tech'
                    LIMIT
                      10""",
                "useLegacySql": False
            },
        },
        location="US",
        gcp_conn_id="BQ"
    )


    @task
    def notify():
        send_email(
            to=[Variable.get("support_email")],
            subject="BQ Query Report",
            html_content="Success! BQ query has run.."
        )


    query_task >> notify()
