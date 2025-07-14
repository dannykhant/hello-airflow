from airflow.sdk import dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor
from pendulum import datetime

# to limit concurrent tasks, set below in .env
# AIRFLOW__CORE__PARALLELISM=3

@dag(
    schedule=None,
    start_date=datetime(2025, 7, 11),
    tags=["sensor"],
    catchup=False
)
def parallel_sensor():
    wait_files = FileSensor.partial(
        task_id="wait_files",
        fs_conn_id="fs_default"
    ).expand(
        filepath=["f1.csv", "f2.csv", "f3.csv"]
    )

    @task
    def task_a():
        print("processing...")

    wait_files >> task_a()


parallel_sensor()
