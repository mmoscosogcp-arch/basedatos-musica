from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime


with DAG(
    dag_id="pipeline_musica",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    cargar_datos = BashOperator(
        task_id="cargar_datos",
        bash_command="cd /opt/airflow/project && python src/main.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/project/music_dbt && dbt run",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/project/music_dbt && dbt test",
    )

    cargar_datos >> dbt_run >> dbt_test
