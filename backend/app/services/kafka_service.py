from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, regexp_replace, col

spark = SparkSession.builder \
    .appName("KafkaService") \
    .master("local[*]") \
    .getOrCreate()

def get_kafka_data():
    kafka_df = spark.read.format("kafka") \
        .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
        .option("subscribe", "csv_data.adv_works") \
        .load()
    return kafka_df.withColumn("value", expr("CAST(value AS STRING)")) \
                   .withColumn("clean_value", regexp_replace(col("value"), r"[^ -~]", ""))
