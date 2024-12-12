import requests
import os

API_URL =  os.getenv("API_URL", "http://localhost:5000/api")

class APIConnector:

    def __init__(self):
        self.api_url = API_URL

    def fetch_data(self, endpoint, payload):
        try:
            response = requests.post(f"{self.api_url}/{endpoint}", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None