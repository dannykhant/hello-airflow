# hello-airflow
###### Useful Airflow use-cases are listed here.
* To start Airflow, run below.
```bash
docker compose up --build -d
```
* To clean up, run below.
```bash
docker compose down
```
* Default username is "admin" and password in your Airflow's simple_auth_manager file.
* Write your own DAG in the dir: airflow/dags.
* To reference *Operators*: https://registry.astronomer.io/
* For a template, checkout [dag_template_v3.py](https://github.com/dannykhant/hello-airflow/blob/main/airflow/dags/dag_template_v3.py)