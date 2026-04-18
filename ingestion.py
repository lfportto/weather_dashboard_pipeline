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
                "wind_direction": data["wind"].get("deg")
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
        INSERT INTO weather_data (
            city_name, country, latitude, longitude, timestamp_utc,
            temperature, feels_like, humidity, pressure, wind_speed, wind_direction
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            r["wind_direction"]
        )
    )

# Commit e fechar conexão
conn.commit()
cursor.close()
conn.close()

print("Ingestão concluída com sucesso!")