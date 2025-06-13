import subprocess
from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

with DAG(
        "conditional_branching",
        default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task(task_id="get_file_size")
    def get_file_size():
        filename = "xrate.csv"
        cmd = ["curl",
               "https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=jsondata",
               "-o", f"/tmp/{filename}"]
        subprocess.run(cmd)
        with open(f"/tmp/{filename}", "rb") as fi:
            size = len(fi.read()) / (1024 ** 3)
        return size


    @task
    def branch1_transform():
        print("Branching 1 is transforming..")


    @task
    def branch2_transform():
        print("branch 2 is transforming..")


    @task
    def branch1_load():
        print("Branching 1 is loading..")


    @task
    def branch2_load():
        print("branch 2 is loading..")


    @task.branch
    def decide_branch(ti):
        size = ti.xcom_pull(task_ids="get_file_size")
        return "branch1_transform" if size > 10 else "branch2_transform"


    decide_branch_task = decide_branch()

    get_file_size() >> decide_branch_task

    decide_branch_task >> branch1_transform() >> branch1_load()

    decide_branch_task >> branch2_transform() >> branch2_load()
