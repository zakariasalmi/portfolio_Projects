import uuid
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
 

# Default DAG arguments
default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2024, 10, 4, 10, 00)
}

# Fetch random user data from the API
def get_data():
    import requests
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]
    return res

# Format the random user data
def format_data(res):
    data = {}
    location = res['location']
    data['id'] = str(uuid.uuid4())
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data

# Stream formatted data to Kafka
def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Kafka producer setup
    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=10000)
    curr_time = time.time()

    try:
        # Run the streaming process for 60 seconds
        while time.time() < curr_time + 60:  # Stream for 1 minute
            try:
                # Fetch and format data
                res = get_data()
                res = format_data(res)

                # Send data to Kafka topic
                producer.send('users_created', json.dumps(res).encode('utf-8'))
                logger.info(f'Successfully sent data to Kafka: {res}')

            except Exception as e:
                logger.error(f'An error occurred while sending data to Kafka: {e}')
                continue
        logger.info("Data streaming complete.")
    finally:
        # Ensure producer is closed
        producer.close()
        logger.info("Kafka producer closed.")

# Define the DAG
with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
