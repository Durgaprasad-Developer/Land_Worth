import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

address = "Patamata, Vijayawada, Andhra Pradesh, India"

url = "https://maps.googleapis.com/maps/api/geocode/json"

params = {
    "address": address,
    "key": API_KEY
}

response = requests.get(url, params=params)
print(response.json())
