from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task

with DAG(
        "setup_teardown",
        default_args={"start_date": datetime.utcnow() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    @task
    def create_cluster():
        print("Creating cluster..")


    @task
    def query_1():
        print("Query 1 is running..")


    @task
    def query_2():
        raise "Query 2 failed.."


    @task
    def query_3():
        print("Query 3 is running..")


    @task
    def destroy_cluster():
        print("Cluster is stopped..")


    create_cluster_task = create_cluster()
    qtask1 = query_1()
    qtask2 = query_2()
    qtask3 = query_3()

    create_cluster_task >> [qtask1, qtask2]
    [qtask1, qtask2] >> qtask3
    qtask3 >> destroy_cluster().as_teardown(setups=create_cluster_task)
