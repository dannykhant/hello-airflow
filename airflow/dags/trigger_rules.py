from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.utils.trigger_rule import TriggerRule

with DAG(
        "trigger_rules",
        default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task
    def task1():
        raise "Task 1"


    @task
    def task2():
        raise "Task 2"


    @task
    def task3():
        raise "Task 3"


    @task(trigger_rule=TriggerRule.ALL_FAILED)
    def task4():
        print("Task 4")


    @task
    def task5():
        print("Task 5")


    task_d = task4()

    task1() >> task_d
    task2() >> task_d
    task3() >> task_d
    task_d >> task5()
