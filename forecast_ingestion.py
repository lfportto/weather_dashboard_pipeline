"""
Filename: forecast_ingestion.py
Author: Luis Felipe Porto
Date: 20-04-2026
Version: 1.0
Description: This script retrieves weather forecast data from the OpenWeatherMap API for multiple global cities.
It processes forecast entries at 3-hour intervals (up to 5 days ahead), structures the data,
and stores it in a PostgreSQL database. The script also records the timestamp of data collection,
enabling versioning and comparison of forecast updates over time.
Contact: luisfelipeporto.lfp@gmail.com
"""

def forecast_ingestion(): # Transformar em função para ser chamado pelo Prefect Cloud
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
    url = "https://api.openweathermap.org/data/2.5/forecast"

    # Limpar tabela antes da nova ingestão
    cursor.execute("TRUNCATE TABLE weather_forecast RESTART IDENTITY;")
    conn.commit()
    print("Registros anteriores da tabela weather_forecast limpos para nova inserção.")

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

    # Momento da coleta
    forecast_generated_at = datetime.now(timezone.utc)

    # Função para coletar dados de forecast
    def coletar_forecast(cidade):
        params = {
            "q": cidade,
            "appid": API_KEY,
            "units": "metric"
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                registros = []

                city_info = data["city"]

                for item in data["list"]:
                    main = item["main"]
                    wind = item["wind"]
                    weather = item["weather"][0]

                    registros.append({
                        "city": city_info["name"],
                        "country": city_info["country"],
                        "latitude": city_info["coord"]["lat"],
                        "longitude": city_info["coord"]["lon"],
                        "timestamp": datetime.fromtimestamp(item["dt"], tz=timezone.utc),
                        "forecast_generated_at": forecast_generated_at,
                        "temperature": main["temp"],
                        "feels_like": main["feels_like"],
                        "humidity": main["humidity"],
                        "pressure": main["pressure"],
                        "wind_speed": wind["speed"],
                        "wind_direction": wind.get("deg"),
                        "weather_main": weather["main"],
                        "weather_description": weather["description"],
                        "weather_icon": weather["icon"]
                    })

                return registros

            else:
                print(f"Erro para {cidade}: {response.status_code}")
                return []

        except Exception as e:
            print(f"Erro na requisição para {cidade}: {e}")
            return []

    # Coletar dados
    resultados = []

    for cidade in cidades:
        registros = coletar_forecast(cidade)
        resultados.extend(registros)
        time.sleep(1)

    # Inserção em batch
    cursor.executemany(
        """
        INSERT INTO weather_forecast (
            city_name, country, latitude, longitude, timestamp_utc, forecast_generated_at,
            temperature, feels_like, humidity, pressure, wind_speed, wind_direction,
            weather_main, weather_description, weather_icon
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        [
            (
                r["city"],
                r["country"],
                r["latitude"],
                r["longitude"],
                r["timestamp"],
                r["forecast_generated_at"],
                r["temperature"],
                r["feels_like"],
                r["humidity"],
                r["pressure"],
                r["wind_speed"],
                r["wind_direction"],
                r["weather_main"],
                r["weather_description"],
                r["weather_icon"]
            )
            for r in resultados
        ]
    )

    # Commit e fechar conexão
    conn.commit()
    cursor.close()
    conn.close()

    print(f"Ingestão de forecast concluída! Total de registros: {len(resultados)}")

# Permite que o script seja executado localmente
if __name__ == "__main__":
    forecast_ingestion()