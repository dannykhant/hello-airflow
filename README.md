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

##### Best practices with Sensors
* Always define a meaningful timeout parameter for your sensor. The default for this parameter is seven days, which is a long time for your sensor to be running. When you implement a sensor, consider your use case and how long you expect the sensor to wait and then define the sensor's timeout accurately.
* Whenever possible and especially for long-running sensors, use the reschedule mode so your sensor is not constantly occupying a worker slot. This helps avoid deadlocks in Airflow where sensors take all of the available worker slots.
* If your poke_interval is very short (less than about 5 minutes), use the poke mode. Using reschedule mode in this case can overload your scheduler.
* Define a meaningful poke_interval based on your use case. There is no need for a task to check a condition every 60 seconds (the default) if you know the total amount of wait time will be 30 minutes.

##### Cli
* To test a task, run below. airflow tasks test <dag_id> <task_id> <logical_date>
```
airflow tasks test cli task_a 2025-07-14
```