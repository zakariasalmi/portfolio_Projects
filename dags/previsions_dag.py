from airflow import DAG # type: ignore
from airflow.operators.python_operator import PythonOperator # type: ignore
from datetime import datetime, timedelta
import sys

sys.path.insert(0, '/opt/airflow/scripts')
from fetch_weather import fetch_weather_data # type: ignore
from process_weather import process_weather_data # type: ignore
from store_weather import store_weather_data # type: ignore

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 2, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_pipeline',
    default_args=default_args,
    description='Pipeline des prévisions météo',
    schedule_interval=timedelta(days=1), 
)

fetch_weather = PythonOperator(
    task_id='fetch_weather',
    python_callable=fetch_weather_data,
    dag=dag,
)

process_data = PythonOperator(
    task_id='process_data',
    python_callable=process_weather_data,
    dag=dag
)

store_data = PythonOperator(
    task_id='store_data',
    python_callable=store_weather_data,
    dag=dag,
)

fetch_weather >> process_data >> store_data
