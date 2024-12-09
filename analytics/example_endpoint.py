from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
app = Flask(__name__)


db_config = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "password",
    "database": "mydatabase",
}

conn = psycopg2.connect(
    host=db_config["host"],
    port=db_config["port"],
    user=db_config["user"],
    password=db_config["password"],
    database=db_config["database"]
)

@app.route('/api/get-data-q1', methods=['POST'])
def get_data():
    try:
        filters = request.get_json()
        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)
        dependent_variable = filters.get("dependent_variable", None)
        predictors = filters.get("predictors", None)
        instruments = filters.get("instruments", [])

        if not start_year or not end_year or not dependent_variable or not predictors:
            return jsonify({
                "success": False,
                "error": "Missing required parameters"
            }), 400
        
        # type check the input parameters
        if not isinstance(start_year, int) or not isinstance(end_year, int):
            return jsonify({
                "success": False,
                "error": "start_year and end_year must be integers"
            }), 400
        
        if not isinstance(predictors, list):
            return jsonify({
                "success": False,
                "error": "predictors must be a list"
            }), 400
        
        if not all(isinstance(p, str) for p in predictors):
            return jsonify({
                "success": False,
                "error": "predictors must be a list of strings"
            }), 400
        
        if not isinstance(instruments, list):
            return jsonify({
                "success": False,
                "error": "instruments must be a list"
            }), 400
        

        # build the query
        query1 = """SELECT c.country_fips, c.revenue
FROM businessFact AS c
WHERE c.date BETWEEN(2017, 2017)
ORDER BY c.revenue
"""
        query2 = """SELECT AVG(w.tavg)
FROM weather AS w, company AS c
WHERE year = 2017 AND 
w.country_fips = c.country_fips
GROUP BY c.country_fips" # modify query based on the question
        """

        
        result1 = pd.read_sql(query1, conn) # get result from database
        result2 = pd.read_sql(query2, conn)
        # process the data
        result = pd.merge(result1, result2, on='country_fips') # just an example

        return jsonify(result.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error processing request: {str(e)}"
        }), 500
    
@app.route('/api/get-data-q2', methods=['POST'])
def get_data():
    try:
        filters = request.get_json()
        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)
        dependent_variable = filters.get("dependent_variable", None)
        companies = filters.get("companies", [])

        if not start_year or not end_year or not dependent_variable or not companies:
            return jsonify({
                "success": False,
                "error": "Missing required parameters"
            }), 400
        
        # type check the input parameters
        if not isinstance(start_year, int) or not isinstance(end_year, int):
            return jsonify({
                "success": False,
                "error": "start_year and end_year must be integers"
            }), 400

        if not isinstance(companies, list):
            return jsonify({
                "success": False,
                "error": "companies must be a list"
            }), 400
        
        if not all(isinstance(c, str) for c in companies):
            return jsonify({
                "success": False,
                "error": "companies must be a list of strings"
            }), 400
        

        query = """SELECT b.revenue, b.name, b.year
FROM BusinessFact 
AS b
WHERE predictors 
IN b.name
AND b.year 
BETWEEN 2010 AND 2024  """ # modify query based on received parameters
        
        result = pd.read_sql(query, conn) # get result from database
        # process the data
        return jsonify(result.to_dict(orient='records'))


    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error processing request: {str(e)}"
        }), 500
    

@app.route('/api/get-data-q3', methods=['POST'])
def get_data():
    try:
        filters = request.get_json()
        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)
        dependent_variable = filters.get("dependent_variable", None)
        instruments = filters.get("instruments", [])

        if not start_year or not end_year or not dependent_variable or not instruments:
            return jsonify({
                "success": False,
                "error": "Missing required parameters"
            }), 400
        
        # type check the input parameters

        if not isinstance(start_year, int) or not isinstance(end_year, int):
            return jsonify({
                "success": False,
                "error": "start_year and end_year must be integers"
            }), 400
        
        if not isinstance(instruments, list):
            return jsonify({
                "success": False,
                "error": "instruments must be a list"
            }), 400
        
        if not all(isinstance(i, str) for i in instruments):
            return jsonify({
                "success": False,
                "error": "instruments must be a list of strings"
            }), 400


        query = """SELECT b.revenue, b.country_fips
        FROM BusinessFact 
        AS b
        WHERE b.date 
        BETWEEN 2017 AND 2017
        GROUP_BY b.country_fips""" # modify query based on the question
        result = pd.read_sql(query, conn) # get result from database
        # process the data
        return jsonify(result.to_dict(orient='records'))
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Error processing request: {str(e)}"
        }), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
