from airflow.sdk import dag, task, chain
from airflow.providers.standard.operators.python import PythonOperator
from pendulum import datetime

default_args = {
    "retries": 1
}


@dag(
    schedule="@daily",
    start_date=datetime(2025, 7, 4),
    default_args=default_args,
    description="My Dag Template",
    tags=["s3", "BQ"],
    max_consecutive_failed_dag_runs=1
)
def dag_template():
    @task
    def task_one():
        print("this is task one...")

    task_one = task_one()

    task_two = PythonOperator(
        task_id="task_two",
        python_callable=lambda: print("this is task 2")
    )

    @task
    def task_three():
        print("this is task one...")

    task_three = task_three()

    @task
    def task_four():
        print("this is task one...")

    task_four = task_four()

    @task
    def task_five():
        print("this is task one...")

    task_five = task_five()

    # task_one >> task_two >> task_three
    # task_one >> task_four >> task_five
    chain(task_one, [task_two, task_four], [task_three, task_five])


dag_template()
