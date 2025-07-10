from airflow.sdk import dag, task
from custom_packages.package_a.time_settings import TimeSettings


@dag
def access_package_dag():
    @task
    def task_a():
        TimeSettings.current_time()


access_package_dag()
