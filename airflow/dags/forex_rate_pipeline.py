from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.utils.email import send_email
from airflow.sdk import Variable

from clean_xrate import clean_xrate

with DAG(
        "forex_rate_pipeline",
        default_args={"start_date": datetime.now() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task.bash
    def extract_data():
        return """
        cd /tmp
        curl -o xrate.csv https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata
        """


    @task
    def clean_data():
        clean_xrate()


    @task
    def notify():
        send_email(
            to=[Variable.get("support_email")],
            subject="Success! Forex Rate Download..",
            html_content="The Exchange Rate data has been successfully downloaded, cleaned, and loaded."
        )


    extract_data() >> clean_data() >> notify()
