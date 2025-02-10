import pandas as pd 
from sqlalchemy import create_engine

def store_weather_data():
    engine = create_engine('postgresql+psycopg2://airflow:airflow@postgres/airflow')
    
    df = pd.read_csv('/opt/airflow/data/processed_weather_data.csv')

    df.to_sql('weather_forecast', engine, if_exists='append', index=False)
    
if __name__=="__main__":
    store_weather_data()
