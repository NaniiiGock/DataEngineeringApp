from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col

# Initialize the Spark session
spark = SparkSession.builder \
    .appName("Iceberg JSON Folder Example") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "./iceberg_warehouse") \
    .config("spark.jars", "jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar") \
    .getOrCreate()

# Path to the folder containing JSON files
json_folder_path = "/Users/lilianahotsko/Desktop/DataEngineeringApp/Jsons"  # Replace with your folder path

# Read all JSON files from the folder
df = spark.read.json(f"{json_folder_path}/*.json")

# Flatten the nested structure by extracting the "results" field
flattened_df = df.select(explode(col("results")).alias("result")).select("result.*")

# Create the Iceberg table explicitly
spark.sql("""
    CREATE TABLE IF NOT EXISTS local.default.weather_data (
        date STRING,
        datatype STRING,
        station STRING,
        attributes STRING,
        value DOUBLE
    )
    USING iceberg
""")

flattened_df.write.format("iceberg").mode("overwrite").save("local.default.weather_data")

iceberg_df = spark.read.format("iceberg").load("local.default.weather_data")
iceberg_df.show()

# Stop the Spark session
spark.stop()
