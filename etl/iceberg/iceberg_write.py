from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col
import os
import json

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
warehouse_path = os.path.join(current_dir, "iceberg_warehouse")
json_folder_path = "/app/data"  # JSON files are mounted here

# Initialize Spark session with Iceberg configuration
spark = SparkSession.builder \
    .appName("Iceberg Weather JSON Loader") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "/app/etl/iceberg/warehouse") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.jars", "/opt/spark/jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar") \
    .getOrCreate()


# Read all JSON files in the folder
json_files = [f"{json_folder_path}/{file}" for file in os.listdir(json_folder_path) if file.startswith("noaa_") and file.endswith(".json")]

# Process each JSON file
all_data = []
for file in json_files:
    with open(file, 'r') as f:
        content = json.load(f)
        if "results" in content:  # Check if results field exists
            all_data.extend(content["results"])

# Convert the aggregated data to a Spark DataFrame
weather_df = spark.createDataFrame(all_data)

# Show schema for debugging
print("Weather data schema:")
weather_df.printSchema()

# Create Iceberg table if it doesn't exist
spark.sql(f"""
    CREATE TABLE IF NOT EXISTS local.default.weather_data (
        date STRING,
        datatype STRING,
        station STRING,
        attributes STRING,
        value DOUBLE
    )
    USING iceberg
""")

# Write data to the Iceberg table
weather_df.write.format("iceberg").mode("append").save("local.default.weather_data")

# Validate by reading back the data
print("Weather data loaded into Iceberg:")
spark.read.format("iceberg").load("local.default.weather_data").show()

spark.sql("SHOW TABLES IN local.default").show()

spark.stop()
