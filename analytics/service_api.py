from flask import Flask, request, jsonify
import pandas as pd
import psycopg2, requests, duckdb, datetime 

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

app = Flask(__name__)

con = duckdb.connect("test.db", read_only=True)

predictors_weather = ('PRCP, TAVG, TMAX, TMIN')

# How the temperature has an influence on the revenues of company X in the year XXXX?
@app.route("/api/get-data-q1", methods=["POST"])
def get_data():
    try:
        filters = request.get_json()
        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)
        dependent_variable = filters.get("dependent_variable", None)
        predictors = filters.get("predictors", None)
        instruments = filters.get("instruments", [])

        if not start_year or not end_year or not dependent_variable or not predictors:
            return (
                jsonify({"success": False, "error": "Missing required parameters"}),
                400,
            )

        # type check the input parameters
        if not is_valid_date(start_year) or not is_valid_date(end_year):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "start_year and end_year must be integers",
                    }
                ),
                400,
            )

        if not isinstance(predictors, list):
            return (
                jsonify({"success": False, "error": "predictors must be a list"}),
                400,
            )

        if not all(isinstance(p, str) for p in predictors):
            return (
                jsonify(
                    {"success": False, "error": "predictors must be a list of strings"}
                ),
                400,
            )

        if not isinstance(instruments, list):
            return (
                jsonify({"success": False, "error": "instruments must be a list"}),
                400,
            )

        # build the query
        query = f"""
        SELECT  w.DATE,  w.TAVG,  b.REVENUES, bd.NAME 
        FROM weatherFACT w 
        JOIN CountyDIM c ON w.COUNTYFIPS = c.COUNTYFIPS 
        JOIN BusinessDIM bd ON c.COUNTYFIPS = bd.COUNTYFIPS 
        JOIN BusinessFACT b ON bd.ID = b.BUSINESSID 
        WHERE bd.NAME IN ({','.join(map(str, instruments))}) 
        AND w.DATE BETWEEN {start_year} AND {end_year} ORDER BY w.DATE;
        """

        result = pd.read_sql(query, con)  # get result from database
        return jsonify(result.to_dict(orient="records"))

    except Exception as e:
        return (
            jsonify({"success": False, "error": f"Error processing request: {str(e)}"}),
            500,
        )


@app.route("/api/get-data-q2", methods=["POST"])
def get_data():
    try:
        filters = request.get_json()
        # start_year = filters.get("start_year", None)
        # end_year = filters.get("end_year", None)
        dependent_variable = filters.get("dependent_variable", None)
        companies = filters.get("companies", [])

        if not dependent_variable or not companies:
            return (
                jsonify({"success": False, "error": "Missing required parameters"}),
                400,
            )

        if not isinstance(companies, list):
            return jsonify({"success": False, "error": "companies must be a list"}), 400

        if not all(isinstance(c, str) for c in companies):
            return (
                jsonify(
                    {"success": False, "error": "companies must be a list of strings"}
                ),
                400,
            )

        query = f"""
        SELECT b.revenue, b.name
        FROM BusinessFact b
        JOIN BusinessDIM db ON b.BUSINESSID = bd.ID
        WHERE bd.NAME IN ({','.join(map(str, companies))})
        ORDER BY bd.NAME;
        """  

        result = pd.read_sql(query, con)  # get result from database
        # process the data
        return jsonify(result.to_dict(orient="records"))

    except Exception as e:
        return (
            jsonify({"success": False, "error": f"Error processing request: {str(e)}"}),
            500,
        )


@app.route("/api/get-data-q3", methods=["POST"])
def get_data():
    try:
        filters = request.get_json()
        start_year = filters.get("start_year", None)
        end_year = filters.get("end_year", None)
        dependent_variable = filters.get("dependent_variable", None)
        instruments = filters.get("instruments", [])

        if not start_year or not end_year or not dependent_variable or not instruments:
            return (
                jsonify({"success": False, "error": "Missing required parameters"}),
                400,
            )

        # type check the input parameters

        if not isinstance(start_year, int) or not isinstance(end_year, int):
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "start_year and end_year must be integers",
                    }
                ),
                400,
            )

        if not isinstance(instruments, list):
            return (
                jsonify({"success": False, "error": "instruments must be a list"}),
                400,
            )

        if not all(isinstance(i, str) for i in instruments):
            return (
                jsonify(
                    {"success": False, "error": "instruments must be a list of strings"}
                ),
                400,
            )

        query = f"""
        SELECT b.revenue, b.country_fips
        FROM BusinessFact b
        WHERE b.date 
        BETWEEN 2017 AND 2017
        GROUP_BY b.country_fips
        """  # modify query based on the question
        result = pd.read_sql(query, conn)  # get result from database
        # process the data
        return jsonify(result.to_dict(orient="records"))

    except Exception as e:
        return (
            jsonify({"success": False, "error": f"Error processing request: {str(e)}"}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
