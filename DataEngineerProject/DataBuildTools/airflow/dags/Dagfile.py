from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

# Définir les arguments par défaut du DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Définir le DAG
dag = DAG(
    'amazon_reviews_dag',
    default_args=default_args,
    description='DAG for processing Amazon reviews with Spark and transforming data with DBT',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 10, 12, 45),
    catchup=False,
)

# Définir la tâche pour exécuter le script Spark
run_spark_job = BashOperator(
    task_id='run_spark_job',
    bash_command='spark-submit --packages org.apache.hadoop:hadoop-aws:3.2.0 /opt/spark/jobs/spark_amazon_reviews.py',
    dag=dag,
)

# Définir la tâche pour exécuter DBT
run_dbt_task = BashOperator(
    task_id='run_dbt_task',
    bash_command='cd /dbt && dbt run',
    dag=dag,
)

# Ordonnancer les tâches
run_spark_job >> run_dbt_task
