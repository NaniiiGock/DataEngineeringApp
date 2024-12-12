from pyspark.sql import SparkSession

# Initialize the Spark session
spark = SparkSession.builder \
    .appName("Query Iceberg Table") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "./iceberg_warehouse") \
    .config("spark.jars", "jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar") \
    .getOrCreate()

# Run an SQL query
spark.sql("SELECT * FROM local.default.weather_data").show()

# Stop the Spark session
spark.stop()
