from flask import Flask, request, jsonify, Response
import requests
import pandas as pd

app = Flask(__name__)

con = duckdb.connect("thunderfinance.db", read_only=True)

@app.route('/')
def home():
    return "Hello, this is a Flask Microservice"
if __name__ == "__main__":
    app.run(debug=True, host="localhost", port='5001')

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    if 'start_date' not in data or 'end_date' not in data or 'city' not in data:
        return jsonify({'error': 'necessary data is missing'}), 400

    data = get_data()
    # Perform correlation calculation here
    correlation = 0.8  # Placeholder correlation result
    return jsonify({'status': 'received', 'correlation': correlation})

BASE_URL = "http://localhost:5001/"
@app.route('/correlation', methods=['GET'])
def get_correlation():
    # Return the calculated correlation result
    return jsonify({'correlation': 0.8})

if __name__ == '__main__':
    app.run(host='localhost', port=5001)

@app.route('/analysis', methods=['POST'])
def analysis1_endpoint():
    """
    Example of a request body:
    {
        "index": "fortune500",
        "variables": ["profit", "weather"],
        "aggregate": "mean"
    }
    :return:
    """
    body = request.get_json()
    subset_profit_weather = ['profit', 'weather']
    if (body['index'] == 'fortune500'
            and all(elem in body['variables'] for elem in subset))\
            and body['aggregate'] == 'mean':
        
        query = f"""SELECT * from profit_weather"""
        data = con.execute(query).fetchdf()
        return Response(data.to_csv(),
                        mimetype='text/csv')

    subset_profit_industry = ['profit', 'industry']
    if (body['index'] == 'fortune500'
            and all(elem in body['variables'] for elem in subset)) \
            and body['aggregate'] == 'mean':
        query = f"""SELECT * from profit_industry"""
        data = con.execute(query).fetchdf()
        return Response(data.to_csv(),
                        mimetype='text/csv')
