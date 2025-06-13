from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.providers.standard.operators.latest_only import LatestOnlyOperator
from airflow.utils.email import send_email
from airflow.utils.trigger_rule import TriggerRule
from airflow.sdk import Variable

with DAG(
        "latest_only",
        default_args={"start_date": datetime.utcnow() - timedelta(days=3)},
        schedule="0 23 * * *",
        catchup=True
) as dag:
    @task
    def task_a():
        print("Task A")


    @task
    def task_b():
        print("Task B")


    latest_only = LatestOnlyOperator(task_id="latest_only")


    @task
    def send_email_success():
        send_email(
            to=[Variable.get("support_email")],
            subject="Pipeline Success!",
            html_content="Pipeline has run successfully"
        )


    @task(trigger_rule=TriggerRule.ALL_FAILED)
    def send_email_fail():
        send_email(
            to=[Variable.get("support_email")],
            subject="Pipeline Fail!",
            html_content="Pipeline has failed"
        )


    task_1 = task_a()
    task_2 = task_b()

    task_1 >> task_2 >> send_email_fail()
    task_2 >> latest_only >> send_email_success()
