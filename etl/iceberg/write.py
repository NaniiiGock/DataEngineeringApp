from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col
import os

# Get absolute path for the Iceberg warehouse
current_dir = os.path.dirname(os.path.abspath(__file__))
warehouse_path = os.path.join(current_dir, "iceberg_warehouse")

# Initialize SparkSession
spark = SparkSession.builder \
    .appName("Iceberg JSON Folder Example") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", warehouse_path) \
    .config("spark.jars", "etl/iceberg/jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar") \
    .getOrCreate()

# Paths
json_folder_path = os.path.join(current_dir, "../data")

# Debugging: Confirm paths
print("JSON folder path:", json_folder_path)
print("Spark warehouse path:", warehouse_path)

try:
    # Read JSON files
    df = spark.read.json(f"{json_folder_path}/*.json")
    print("Original JSON schema:")
    df.printSchema()

    # Flatten the DataFrame
    flattened_df = df.select(explode(col("results")).alias("result")).select("result.*")
    print("Flattened DataFrame schema:")
    flattened_df.printSchema()

    # Create Iceberg table if not exists
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

    # Write to Iceberg table
    flattened_df.write.format("iceberg").mode("overwrite").save("local.default.weather_data")

    # Read back and show the data
    iceberg_df = spark.read.format("iceberg").load("local.default.weather_data")
    iceberg_df.show()

except Exception as e:
    print("Error during Iceberg processing:", str(e))

finally:
    spark.stop()
