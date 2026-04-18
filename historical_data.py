import psycopg2
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from meteostat import Point, Daily
import pandas as pd

# Carregar variáveis de ambiente
load_dotenv()

# Conexão com o banco de dados
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cursor = conn.cursor()

# Definir período de coleta (últimos 180 dias)
end_date = datetime.now()
start_date = end_date - timedelta(days=180)

# Limpar tabela antes do backfill (histórico)
cursor.execute("TRUNCATE TABLE weather_data RESTART IDENTITY;")
conn.commit()
print("Registros anteriores da tabela weather_data limpos para nova inserção.")

# Lista de cidades com coordenadas
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

# Lista final de registros
registros = []

# Coletar dados históricos
for cidade in cidades:
    try:
        print(f"Coletando histórico de {cidade['city']}...")

        location = Point(cidade["lat"], cidade["lon"])
        data = Daily(location, start_date, end_date)
        df = data.fetch()

        # Se não houver dados para tal cidade, pula
        if df.empty:
            print(f"Sem dados para {cidade['city']}")
            continue

        for index, row in df.iterrows():

            # Ignorar linhas sem temperatura (que é o dado essencial)
            if pd.isna(row["tavg"]):
                continue

            registros.append((
                cidade["city"],
                cidade["country"],
                cidade["lat"],
                cidade["lon"],
                index.to_pydatetime().replace(tzinfo=timezone.utc),
                float(row["tavg"]),
                None,  # feels_like
                None,  # humidity
                float(row["pres"]) if not pd.isna(row.get("pres")) else None,
                float(row["wspd"]) if not pd.isna(row.get("wspd")) else None,
                None   # wind_direction
            ))

    except Exception as e:
        print(f"Erro ao coletar dados de {cidade['city']}: {e}")

# Inserção em batch
cursor.executemany(
    """
    INSERT INTO weather_data (
        city_name, country, latitude, longitude, timestamp_utc,
        temperature, feels_like, humidity, pressure, wind_speed, wind_direction
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,
    registros
)

conn.commit()
cursor.close()
conn.close()

print(f"Ingestão concluída com sucesso! Total de registros inseridos: {len(registros)}")