from flask import Flask, request, jsonify
import requests

def get_data():

    # Define the endpoint URL
    url = 'https://jsonplaceholder.typicode.com/posts'

    # Define the data to be sent in the POST request
    data = {
        'city': 'foo',
        'start_date': '2000-01-01',
        'end_date': '2024-01-01'
    }

    response = requests.post(url, json=data)
    if response.status_code == 201:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return f"Error: {response.status_code}"



app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is a Flask Microservice"
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)

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
    app.run(host='0.0.0.0', port=5000)
