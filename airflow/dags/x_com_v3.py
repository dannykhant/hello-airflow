from airflow.sdk import dag, task


@dag
def xcom_dag_v3():
    @task
    def task_a():
        a_value = 31
        return a_value

    @task
    def task_b(value):
        print(value)

    task_a = task_a()
    task_b(task_a)


xcom_dag_v3()
