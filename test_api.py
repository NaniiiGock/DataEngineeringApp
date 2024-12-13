import unittest
import json
from service_api.service_api import app  

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_hello_world(self):
        response = self.client.get("/")
        print("Hello world response:", response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "<p>Hello, World!</p>")

    def test_get_data_q1_success(self):
        payload = {
            "start_year": "2015-01-01",
            "end_year": "2018-01-01",
            "dependent_variable": "REVENUES",
            "predictors": "TAVG",
            "instruments": ["ALBERTSONS COS."]
        }
        response = self.client.post("/api/get-data-q1", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Data Q1:", data)
        self.assertIsInstance(data, list)  # Check if the response is a list

    def test_get_data_q1_missing_parameters(self):
        payload = {
            "start_year": "2015-01-01",
            "end_year": "2018-01-01",
            "predictors": "TAVG",
            "instruments": ["ALBERTSONS COS."]
        }
        response = self.client.post("/api/get-data-q1", json=payload)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        print("Data Q1 Missing Parameters:", data)
        self.assertIn("error", data)

    def test_get_data_q2_success(self):
        payload = {
            "dependent_variable": "REVENUES",
            "instruments": ["ALBERTSONS COS."]
        }
        response = self.client.post("/api/get-data-q2", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Data Q2:", data)
        self.assertIsInstance(data, list)

    def test_get_data_q3(self):
        response = self.client.get("/api/get-data-q3")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Data Q3:", data)
        self.assertIsInstance(data, list)

    def test_get_dependent_vars(self):
        response = self.client.get("/api/get/dependent_vars")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Dependent Vars:", data)
        self.assertIsInstance(data, list)

    def test_get_predictors(self):
        response = self.client.get("/api/get/predictors")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        print("Predictors:", data)
        self.assertIsInstance(data, list)

    def test_get_companies(self):
        response = self.client.get("/api/get/companies")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        # print("Companies:", data)
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
