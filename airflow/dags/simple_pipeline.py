from airflow.sdk import dag, task
from pendulum import datetime


@dag(
    schedule="@daily",
    start_date=datetime(2025, 7, 4),
    description="Simple Pipeline",
    tags=["date engineering"],
    max_consecutive_failed_dag_runs=1
)
def simple_pipeline():
    @task.bash
    def create_file():
        return "echo 'this is a file' >> /tmp/dummy"

    @task.bash
    def check_file():
        return "test -f /tmp/dummy"

    @task
    def read_file():
        print(open("/tmp/dummy", "rb").read())

    create_file() >> check_file() >> read_file()


simple_pipeline()
