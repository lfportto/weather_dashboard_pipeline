"""
Filename: current_ingestion.py
Author: Luis Felipe Porto
Date: 20-04-2026
Version: 1.0
Description: This script collects current weather data from the OpenWeatherMap API for a predefined list of cities.
It captures real-time atmospheric conditions such as temperature, humidity, pressure, and wind metrics,
then loads the processed data into a PostgreSQL database. This script is designed to run periodically
to maintain up-to-date observations.
Contact: luisfelipeporto.lfp@gmail.com
"""

def current_ingestion(): # Transformar em função para ser chamado pelo Prefect Cloud
    import psycopg2
    import requests
    import time
    import os
    from datetime import datetime, timezone
    from dotenv import load_dotenv

    # Carregar variáveis de ambiente
    load_dotenv()

    # Conexão com o banco de dados
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()

    API_KEY = os.getenv("API_KEY")
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Lista de cidades para coletar dados
    cidades = [
        "Sao Paulo",
        "New York",
        "London",
        "Tokyo",
        "Toronto",
        "Paris",
        "Berlin",
        "Dubai",
        "Sydney",
        "Singapore"
    ]

    # Função para coletar dados de clima
    def coletar_clima(cidade):
        params = {
            "q": cidade,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()

                # Extrair dados de clima
                weather = data["weather"][0]

                return {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "latitude": data["coord"]["lat"],
                    "longitude": data["coord"]["lon"],
                    "timestamp": datetime.now(timezone.utc),
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "pressure": data["main"]["pressure"],
                    "wind_speed": data["wind"]["speed"],
                    "wind_direction": data["wind"].get("deg"),
                    "weather_main": weather.get("main"),
                    "weather_description": weather.get("description"),
                    "weather_icon": weather.get("icon"),
                    "source_api": "openweather"
                }

            else:
                print(f"Erro para {cidade}: {response.status_code}")
                return None

        except Exception as e:
            print(f"Erro na requisição para {cidade}: {e}")
            return None

    # Coletar dados
    resultados = []

    for cidade in cidades:
        resultado = coletar_clima(cidade)

        if resultado:
            resultados.append(resultado)

        time.sleep(1)

    # Inserir no banco de dados na nuvem
    for r in resultados:
        cursor.execute(
            """
            INSERT INTO weather_current (
                city_name, country, latitude, longitude, timestamp_utc,
                temperature, feels_like, humidity, pressure, wind_speed, wind_direction,
                weather_main, weather_description, weather_icon, source_api
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                r["city"],
                r["country"],
                r["latitude"],
                r["longitude"],
                r["timestamp"],
                r["temperature"],
                r["feels_like"],
                r["humidity"],
                r["pressure"],
                r["wind_speed"],
                r["wind_direction"],
                r["weather_main"],
                r["weather_description"],
                r["weather_icon"],
                r["source_api"]
            )
        )

    # Commit e fechar conexão
    conn.commit()
    cursor.close()
    conn.close()

    print("Ingestão concluída com sucesso!")

# Permite que o script seja executado localmente
if __name__ == "__main__":
    current_ingestion()