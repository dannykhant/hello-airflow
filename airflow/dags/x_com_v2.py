from airflow.sdk import dag, task


@dag
def xcom_dag_v2():
    @task
    def task_a(ti):
        a_value = 31
        ti.xcom_push(key="my_key", value=a_value)

    @task
    def task_b(ti):
        output = ti.xcom_pull(task_ids="task_a", key="my_key")
        print(output)

    task_a() >> task_b()


xcom_dag_v2()
