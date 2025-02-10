import json
import pandas as pd 

def process_weather_data():
    with open('/opt/airflow/data/weather_data.json', 'r') as f:
        data = json.load(f)
    
    processed_data = []
    
    for city_forecast in data:
        city_name = city_forecast['Ville']
        
        for daily_data in city_forecast['Previsions']:
            processed_data.append({
                'city': city_name,
                'date': daily_data['Date'],
                'temp_max': daily_data['Température Max (°C)'],
                'temp_min': daily_data['Température Min (°C)'],
                'humidity': daily_data['Humidité (%)'],
                'rain_probability': daily_data['Chance de Pluie (%)'],
            })
    
    df = pd.DataFrame(processed_data)
    df.to_csv('/opt/airflow/data/processed_weather_data.csv', index=False)

if __name__ == "__main__":
    process_weather_data()
