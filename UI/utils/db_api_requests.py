import requests
import os

API_URL = os.getenv("API_URL", "http://analytics:5001")

class APIConnector:

    def __init__(self, api_url=API_URL):
        self.api_url = api_url

    def fetch_data(self, q_number, payload):
        response = requests.post(f"{self.api_url}/api/get-data-q{q_number}", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def fetch_data_get_request(self, q_number):
        response = requests.get(f"{self.api_url}/api/get-data-q{q_number}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def fetch_companies(self):
        response = requests.get(f"{self.api_url}/api/get/companies")
        if response.status_code == 200:
            return response.json()
        else:
            return None