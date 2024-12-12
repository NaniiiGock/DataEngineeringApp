from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Query Iceberg Table") \
    .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.local.type", "hadoop") \
    .config("spark.sql.catalog.local.warehouse", "etl/iceberg/iceberg_warehouse") \
    .config("spark.jars", "etl/iceberg/jars/iceberg-spark-runtime-3.5_2.12-1.7.1.jar") \
    .getOrCreate()

spark.sql("SELECT * FROM local.default.weather_data").show()

spark.stop()
