from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, regexp_replace, col
import os 
import sys

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

spark = SparkSession.builder \
    .appName("FastAPI Spark Job") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
    .getOrCreate()


def get_kafka_data():
    kafka_df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
        .option("subscribe", "csv_data.adv_works") \
        .load()
    return kafka_df.withColumn("value", expr("CAST(value AS STRING)")) \
                   .withColumn("clean_value", regexp_replace(col("value"), r"[^ -~]", ""))
