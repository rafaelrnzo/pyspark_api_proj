from pyspark.sql.functions import from_json, col
from app.schemas.kafka_schema import schema

def parse_and_flatten_kafka_data(kafka_df):
    parsed_df = kafka_df.withColumn("values_json", from_json(col("clean_value"), schema)) \
                        .selectExpr("values_json.*")
    flattened_df = parsed_df.select(
        col("fullDocument._id.$oid").alias("document_id"),
        col("fullDocument.product").alias("product"),
        col("fullDocument.sales").alias("sales")
        # Add more fields as needed
    )
    return flattened_df.orderBy(col("clusterTime.$timestamp.t").desc()).limit(100).rdd.map(lambda row: row.asDict()).collect()

def run_analytics():
    # Placeholder for Spark analytics operations
    # Perform aggregations, joins, or other analysis here
    return {"summary": "Analytics results"}
