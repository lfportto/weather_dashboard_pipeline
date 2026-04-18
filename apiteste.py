import psycopg2
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from meteostat import Point, Daily

# Carregar variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

# Definir período de coleta (últimos 90 dias)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Lista de cidades com enriquecimento (nome + país + coordenadas)
cidades = [
    {"city": "Sao Paulo", "country": "BR", "lat": -23.55, "lon": -46.63},
    {"city": "New York", "country": "US", "lat": 40.71, "lon": -74.00},
    {"city": "London", "country": "GB", "lat": 51.50, "lon": -0.12},
    {"city": "Tokyo", "country": "JP", "lat": 35.68, "lon": 139.69},
    {"city": "Toronto", "country": "CA", "lat": 43.65, "lon": -79.38},
    {"city": "Paris", "country": "FR", "lat": 48.85, "lon": 2.35},
    {"city": "Berlin", "country": "DE", "lat": 52.52, "lon": 13.40},
    {"city": "Dubai", "country": "AE", "lat": 25.20, "lon": 55.27},
    {"city": "Sydney", "country": "AU", "lat": -33.86, "lon": 151.21},
    {"city": "Singapore", "country": "SG", "lat": 1.29, "lon": 103.85}
]

# Lista para armazenar resultados
resultados = []

# Coletar dados históricos usando Meteostat
for cidade in cidades:
    try:
        print(f"Coletando histórico de {cidade['city']}...")

        # Criar ponto geográfico
        location = Point(cidade["lat"], cidade["lon"])

        # Buscar dados diários
        data = Daily(location, start_date, end_date)
        df = data.fetch()                       

        # Iterar sobre o DataFrame
        for index, row in df.iterrows():
            resultados.append({
                "city": cidade["city"],
                "country": cidade["country"],
                "latitude": cidade["lat"],
                "longitude": cidade["lon"],
                "timestamp": index.to_pydatetime().replace(tzinfo=timezone.utc),
                "temperature": row["tavg"],
                "feels_like": None,  # Meteostat não fornece
                "humidity": None,    # não disponível nesse endpoint
                "pressure": row.get("pres"),
                "wind_speed": row.get("wspd"),
                "wind_direction": None  # não disponível
            })

    except Exception as e:
        print(f"Erro ao coletar dados de {cidade['city']}: {e}")

# Inserir dados no banco
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

print("Ingestão histórica concluída com sucesso!")