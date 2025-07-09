from airflow.sdk import dag, task, Context


@dag
def xcom_dag_v1():
    @task
    def task_a(context: Context):
        a_value = 31
        context["ti"].xcom_push(key="my_key", value=a_value)

    @task
    def task_b(context: Context):
        output = context["ti"].xcom_pull(task_ids="task_a", key="my_key")
        print(output)

    task_a() >> task_b()


xcom_dag_v1()
