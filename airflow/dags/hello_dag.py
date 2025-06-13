from datetime import date, datetime, timedelta
import requests

from airflow import DAG
from airflow.decorators import task

with DAG(
        "hello_dag",
        default_args={"start_date": datetime.now() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task
    def print_hello():
        print("Hello Airflow")


    @task
    def print_date():
        print("Today: ", date)


    @task
    def print_quote():
        response = requests.get("https://random-quotes-freeapi.vercel.app/api/random")
        quote = response.json()["quote"]
        print("Today quote: ", quote)


    print_hello_task = print_hello()
    print_date_task = print_date()
    print_quote_task = print_quote()

    print_hello_task >> print_date_task >> print_quote_task
