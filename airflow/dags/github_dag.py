import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.github.operators.github import GithubOperator
from airflow.providers.standard.operators.empty import EmptyOperator

with DAG(
        "github_dag",
        default_args={"start_date": datetime.now() - timedelta(days=1)},
        schedule="0 23 * * *",
        catchup=False
) as dag:
    empty_task = EmptyOperator(task_id="start")

    github_task = GithubOperator(
        task_id="get_github_info",
        github_method="get_repo",
        github_method_args={"full_name_or_id": "dannykhant/hellospark"},
        result_processor=lambda repo: logging.info(list(repo.get_tags())),
    )

    empty_task >> github_task
