import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")
url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": "São Paulo",
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(url, params=params)
data = response.json()

print(json.dumps(data, indent=4, ensure_ascii=False))