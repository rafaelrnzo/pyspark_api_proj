from fastapi import FastAPI
from pyspark.sql import SparkSession
import os
import sys
from pyspark.sql.functions import expr, regexp_replace, col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from fastapi.middleware.cors import CORSMiddleware

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

spark = SparkSession.builder \
    .appName("FastAPI Spark Job") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
    .getOrCreate()

@app.get("/spark-job")
def run_spark_job():
    try:
        # Read Kafka data
        kafka_df = spark \
            .read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
            .option("subscribe", "climate_data.temperature_data") \
            .load()

        kafka_json_df = kafka_df.withColumn("value", expr("cast(value as string)"))

        cleaned_kafka_df = kafka_json_df.withColumn(
            "clean_value",
            regexp_replace(col("value"), r"[^ -~]", "")  
        )

        schema = StructType([
            StructField("_id", StructType([
                StructField("$oid", StringType(), True)
            ]), True),
            StructField("operationType", StringType(), True),
            StructField("clusterTime", StructType([
                StructField("$timestamp", StructType([
                    StructField("t", DoubleType(), True),
                    StructField("i", DoubleType(), True)
                ]), True)
            ]), True),
            StructField("wallTime", StructType([
                StructField("$date", DoubleType(), True)
            ]), True),
            StructField("fullDocument", StructType([
                StructField("_id", StructType([
                    StructField("$oid", StringType(), True)
                ]), True),
                StructField("lat", StringType(), True),
                StructField("lon", StringType(), True),
                StructField("z", StringType(), True),
                StructField("time", StringType(), True),
                StructField("anom", StringType(), True)
            ]), True),
            StructField("ns", StructType([
                StructField("db", StringType(), True),
                StructField("coll", StringType(), True)
            ]), True),
            StructField("documentKey", StructType([
                StructField("_id", StructType([
                    StructField("$oid", StringType(), True)
                ]), True)
            ]), True)
        ])

        streaming_df = cleaned_kafka_df.withColumn(
            "values_json", 
            from_json(col("clean_value"), schema)  
        ).selectExpr("values_json.*")

        # Flatten the fullDocument column
        flattened_fullDocument_df = streaming_df.select(
            col("fullDocument._id.$oid").alias("document_id"),
            col("fullDocument.lat").alias("latitude"),
            col("fullDocument.lon").alias("longitude"),
            col("fullDocument.z").alias("altitude"),
            col("fullDocument.time").alias("timestamp"),
            col("fullDocument.anom").alias("anomaly")
        )

        # Convert to a list of dictionaries for the API response
        result_list = [{"document_id": row["document_id"], "latitude": row["latitude"], 
                        "longitude": row["longitude"], "altitude": row["altitude"],
                        "timestamp": row["timestamp"], "anomaly": row["anomaly"]} 
                       for row in flattened_fullDocument_df.collect()]

        return {"status": "Spark job completed", "data": result_list}

    except Exception as e:
        return {"status": "error", "message": str(e)}
