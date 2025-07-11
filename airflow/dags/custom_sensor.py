from airflow.sdk import dag, task
from pendulum import datetime
import requests

from airflow.sensors.base import PokeReturnValue


@dag(
    schedule=None,
    start_date=datetime(2025, 7, 11),
    catchup=False
)
def custom_sensor():
    @task.sensor(
        poke_interval=60,
        timeout=60 * 60,
        mode="poke"
    )
    def check_api() -> PokeReturnValue:
        req = requests.get("http://forex.cbm.gov.mm/api/latest")

        if req.status_code == 200:
            return PokeReturnValue(is_done=True, xcom_value=req.json())
        else:
            return PokeReturnValue(is_done=False)

    @task
    def process_data(data):
        print(data)

    process_data(check_api())


custom_sensor()
