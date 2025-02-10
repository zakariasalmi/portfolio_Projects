import requests
import json
import os
from datetime import datetime

def fetch_weather_data():
    api_key = ''  # Remplace avec ta clé API
    file_path = '/opt/airflow/data/weather_data.json'
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    cities = {
        'Agadir': (30.42, -9.60),
        'Casablanca': (33.57, -7.59),
        'Marrakech': (31.63, -8.00),
        'Fès': (34.03, -5.00),
        'Tanger': (35.76, -5.83)
    }

    weather_data = []

    for city, (lat, lon) in cities.items():
        url = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=fr'
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Erreur API pour {city} : {response.status_code}, {response.text}")
                continue

            data = response.json()
            forecast = {
                "Ville": city,
                "Previsions": []
            }

            for entry in data.get("list", []):
                date = datetime.utcfromtimestamp(entry["dt"]).strftime('%Y-%m-%d %H:%M:%S')
                forecast["Previsions"].append({
                    "Date": date,
                    "Température (°C)": entry["main"]["temp"],
                    "Température Max (°C)": entry["main"]["temp_max"],
                    "Température Min (°C)": entry["main"]["temp_min"],
                    "Humidité (%)": entry["main"]["humidity"],
                    "Chance de Pluie (%)": entry.get("pop", 0) * 100
                })

            weather_data.append(forecast)

        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des données pour {city}: {e}")

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=4, ensure_ascii=False)
    
    print("Mise à jour des prévisions météo réussie.")

if __name__ == "__main__":
    fetch_weather_data()
