from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
import duckdb

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

app = Flask(__name__)

con = duckdb.connect("my_duckdb_file.db", read_only=True)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/get-data-q1", methods=["POST"])
def get_data_q1():
    try:
        filters = request.get_json()
        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)
        dependent_variable = filters.get("dependent_variable", None)
        predictor = filters.get("predictors", None)
        instruments = filters.get("instruments", [])

        if not start_year or not end_year or not dependent_variable or not predictor:
            return (
                jsonify({"success": False, "error": "Missing required parameters"}),
                400,
            )
        
        if not is_valid_date(start_year) or not is_valid_date(end_year):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "start_year and end_year must be string",
                    }
                ),
                400,
            )

        if not isinstance(predictor, str):
            return (
                jsonify({"success": False, "error": "predictors must be a list"}),
                400,
            )

        if not isinstance(instruments, list):
            return (
                jsonify({"success": False, "error": "instruments must be a list"}),
                400,
            )

        query = f"""
        SELECT  w.DATE,  w.{predictor},  b.REVENUES, bd.NAME 
        FROM weatherFACT w 
        JOIN CountyDIM c ON w.COUNTYFIPS = c.COUNTYFIPS 
        JOIN BusinessDIM bd ON c.COUNTYFIPS = bd.COUNTYFIPS 
        JOIN BusinessFACT b ON bd.ID = b.BUSINESSID 
        WHERE bd.NAME IN ({','.join(map(lambda x: f"'{x}'", instruments))})
        AND w.DATE BETWEEN '{start_year}' AND '{end_year}'
        ORDER BY w.DATE;
       """

        result = pd.read_sql(query, con)
        return jsonify(result.to_dict(orient="records"))

    except Exception as e:
        return (
            jsonify({"success": False, "error": f"Error processing request: {str(e)}"}),
            500,
        )

@app.route("/api/get-data-q2", methods=["POST"])
def get_data_q2():
    try:
        filters = request.get_json()
        dependent_variable = filters.get("dependent_variable", None)
        instruments = filters.get("instruments", [])

        if not dependent_variable or not instruments:
            return (
                jsonify({"success": False, "error": "Missing required parameters"}),
                400,
            )

        if not isinstance(instruments, list):
            return jsonify({"success": False, "error": "instruments must be a list"}), 400

        if not all(isinstance(c, str) for c in instruments):
            return (
                jsonify(
                    {"success": False, "error": "instruments must be a list of strings"}
                ),
                400,
            )

        query = f"""
        SELECT b.revenues, bd.name
        FROM BusinessFACT b
        JOIN BusinessDIM bd ON b.BUSINESSID = bd.ID
        WHERE bd.NAME IN ({','.join(map(lambda x: f"'{x}'", instruments))})
        ORDER BY bd.NAME;
        """  

        result = pd.read_sql(query, con) 
        return jsonify(result.to_dict(orient="records"))

    except Exception as e:
        return (
            jsonify({"success": False, "error": f"Error processing request: {str(e)}"}),
            500,
        )


@app.route("/api/get-data-q3", methods=["GET"])
def get_data_q3():
    query = f"""
    SELECT SUM(b.EMPLOYEES), bd.countyfips, cd.latitude, cd.longtitude
    FROM BusinessFACT b
    JOIN BusinessDIM bd ON b.BUSINESSID = bd.ID
    JOIN CountyDIM cd ON bd.COUNTYFIPS = cd.COUNTYFIPS
    GROUP BY bd.countyfips
    """
    result = pd.read_sql(query, con) 
    return jsonify(result.to_dict(orient="records"))


@app.route("/api/get/dependent_vars", methods=["GET"])
def get_data_dependent_vars():
    return jsonify('EMPLOYEES', 'REVENUES', 'PROFIT')

@app.route("/api/get/predictors", methods=["GET"])
def get_data_predictors():
    return jsonify('EMPLOYEES', 'TMIN', 'TMAX', 'TAV', 'PRCP')

@app.route("/api/get/companies", methods=["GET"])
def get_data_companies():
    query = """
    SELECT NAME
    FROM BusinessDIM
    """
    result = pd.read_sql(query, con) 
    return jsonify(result.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
