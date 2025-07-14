from airflow.sdk import dag, task
# from airflow.exceptions import AirflowException
from pendulum import datetime


@dag(
    schedule=None,
    start_date=datetime(2025, 7, 14),
    catchup=False
)
def cli():
    @task
    def task_a(val):
        # raise AirflowException()
        print(val)
        return 31

    task_a(77)


cli()
