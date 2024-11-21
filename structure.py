

def get_data(start_date, end_date, stock_name):
    query1 = f"SELECT * FROM activity_fact WHERE timestamp >= '{start_date}' AND timestamp <= '{end_date}'"
    query2 = f"SELECT * FROM user_dim WHERE email = '{stock_name}'"
    query3 = f"SELECT * FROM role_dim"

    db_connection = client.connect()
    cursor = db_connection.cursor()
    cursor.execute(query1)
    data1 = cursor.fetchall()
    cursor.execute(query2)
    data2 = cursor.fetchall()
    cursor.execute(query3)
    data3 = cursor.fetchall()

    return data1, data2, data3

def analysis1(data1):
    return len(data1)

def analysis2(data2):
    return len(data2)

def analysis3(data3):
    return len(data3)

@app.route('/analysis', methods=['POST'])
def analysis1_endpoint():
    data = request.get_json()
    start_date, end_date, stock_name = data['start_date'], data['end_date'], data['stock_name']
    data1, data2, data3 = get_data(start_date, end_date, stock_name)
    result1 = analysis1(data1)
    result2 = analysis2(data2)
    result3 = analysis3(data3)
    return jsonify({'result1': result1, 'result2': result2, 'result3': result3})
