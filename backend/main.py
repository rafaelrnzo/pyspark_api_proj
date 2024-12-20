import os
import sys
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, regexp_replace, col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

# Set PySpark environment variables
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# Initialize FastAPI app
app = FastAPI()

# Add middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Spark session
spark = SparkSession.builder \
    .appName("FastAPI Spark Job") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1") \
    .getOrCreate()

# Define schema for parsing JSON data
schema = StructType([
    StructField('_id', StructType([StructField('_data', StringType(), True)]), True),
    StructField('operationType', StringType(), True),
    StructField('clusterTime', StructType([StructField('$timestamp', StructType([StructField('t', IntegerType(), True), StructField('i', IntegerType(), True)]), True)]), True),
    StructField('fullDocument', StructType([
        StructField('_id', StructType([StructField('$oid', StringType(), True)]), True),
        StructField('productcategory', StringType(), True),
        StructField('productsubcategory', StringType(), True),
        StructField('product', StringType(), True),
        StructField('saleterritory', StringType(), True),
        StructField('Country', StringType(), True),
        StructField('City', StringType(), True),
        StructField('Sate', StringType(), True),
        StructField('Customer', StringType(), True),
        StructField('Employee', StringType(), True),
        StructField('OrderCount', DoubleType(), True),
        StructField('OrderDate', StringType(), True),
        StructField('StandardCost', DoubleType(), True),
        StructField('UnitPrice', DoubleType(), True),
        StructField('NetSales', DoubleType(), True),
        StructField('OrderQuantity', DoubleType(), True),
        StructField('Sales', DoubleType(), True)
    ]), True)
])

# Function to read and process Kafka data
def get_kafka_data():
    kafka_df = spark \
        .read \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
        .option("subscribe", "csv_data.adv_works") \
        .load()

    kafka_json_df = kafka_df.withColumn("value", expr("CAST(value AS STRING)"))
    cleaned_kafka_df = kafka_json_df.withColumn(
        "clean_value", regexp_replace(col("value"), r"[^ -~]", "")
    )

    return cleaned_kafka_df

# API to fetch all data from Kafka
@app.get("/all-data")
def run_spark_job():
    try:
        cleaned_kafka_df = get_kafka_data()

        # Parse the cleaned Kafka data
        streaming_df = cleaned_kafka_df.withColumn(
            "values_json", from_json(col("clean_value"), schema)
        ).selectExpr("values_json.*")

        # Flatten and select required fields
        flattened_df = streaming_df.select(
            col("fullDocument._id.$oid").alias("document_id"),
            col("fullDocument.productcategory").alias("product_category"),
            col("fullDocument.productsubcategory").alias("product_subcategory"),
            col("fullDocument.product").alias("product"),
            col("fullDocument.saleterritory").alias("sale_territory"),
            col("fullDocument.Country").alias("country"),
            col("fullDocument.City").alias("city"),
            col("fullDocument.Sate").alias("state"),
            col("fullDocument.Customer").alias("customer"),
            col("fullDocument.Employee").alias("employee"),
            col("fullDocument.OrderCount").alias("order_count"),
            col("fullDocument.OrderDate").alias("order_date"),
            col("fullDocument.StandardCost").alias("standard_cost"),
            col("fullDocument.UnitPrice").alias("unit_price"),
            col("fullDocument.NetSales").alias("net_sales"),
            col("fullDocument.OrderQuantity").alias("order_quantity"),
            col("fullDocument.Sales").alias("sales"),
            col("clusterTime.$timestamp.t").alias("timestamp")
        )

        # Order by timestamp and return the top 100 records
        result_list = flattened_df.orderBy(col("timestamp").desc()).limit(100).rdd.map(lambda row: row.asDict()).collect()
        return {"status": "Spark job completed", "data": result_list}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# WebSocket for real-time data streaming
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            cleaned_kafka_df = get_kafka_data()

            # Parse the cleaned Kafka data
            streaming_df = cleaned_kafka_df.withColumn(
                "values_json", from_json(col("clean_value"), schema)
            ).selectExpr("values_json.*")

            # Flatten the DataFrame
            flattened_df = streaming_df.select(
                col("fullDocument._id.$oid").alias("document_id"),
                col("fullDocument.productcategory").alias("product_category"),
                col("fullDocument.productsubcategory").alias("product_subcategory"),
                col("fullDocument.product").alias("product"),
                col("fullDocument.saleterritory").alias("sale_territory"),
                col("fullDocument.Country").alias("country"),
                col("fullDocument.City").alias("city"),
                col("fullDocument.Sate").alias("state"),
                col("fullDocument.Customer").alias("customer"),
                col("fullDocument.Employee").alias("employee"),
                col("fullDocument.OrderCount").alias("order_count"),
                col("fullDocument.OrderDate").alias("order_date"),
                col("fullDocument.StandardCost").alias("standard_cost"),
                col("fullDocument.UnitPrice").alias("unit_price"),
                col("fullDocument.NetSales").alias("net_sales"),
                col("fullDocument.OrderQuantity").alias("order_quantity"),
                col("fullDocument.Sales").alias("sales")
            )

            # Send real-time data to the WebSocket client
            result_list = flattened_df.rdd.map(lambda row: row.asDict()).take(10)
            await websocket.send_json(result_list)

            await asyncio.sleep(5)  # Delay for streaming

    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})
    finally:
        await websocket.close()

# API to count order data
@app.get("/count-data")
def count_data():
    try:
        cleaned_kafka_df = get_kafka_data()

        # Parse the cleaned Kafka data
        streaming_df = cleaned_kafka_df.withColumn(
            "values_json", from_json(col("clean_value"), schema)
        ).selectExpr("values_json.*")

        # Calculate the total order count
        flattened_df = streaming_df.select(col("fullDocument.OrderCount").alias("order_count"))
        total_count = flattened_df.groupBy().sum("order_count").collect()[0][0] or 0

        return {"status": "Spark job completed", "total_order_count": total_count}

    except Exception as e:
        return {"status": "error", "message": str(e)}

# WebSocket for real-time order count
@app.websocket("/ws/count-data")
async def websocket_count_data(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            cleaned_kafka_df = get_kafka_data()

            # Parse and calculate total order count
            streaming_df = cleaned_kafka_df.withColumn(
                "values_json", from_json(col("clean_value"), schema)
            ).selectExpr("values_json.*")
            flattened_df = streaming_df.select(col("fullDocument.OrderCount").alias("order_count"))
            total_count = flattened_df.groupBy().sum("order_count").collect()[0][0] or 0

            # Send the total count to the client
            await websocket.send_json({"status": "success", "total_order_count": total_count})

            await asyncio.sleep(5)  # Delay for streaming

    except Exception as e:
        await websocket.send_json({"status": "error", "message": str(e)})
    finally:
        await websocket.close()
