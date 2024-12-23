from pyspark.sql.functions import from_json, col
from app.schemas.kafka_schema import schema

def parse_and_flatten_kafka_data(kafka_df):
    parsed_df = kafka_df.withColumn("values_json", from_json(col("clean_value"), schema)) \
                        .selectExpr("values_json.*")
    flattened_df = parsed_df.select(
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
    return flattened_df.orderBy(col("clusterTime.$timestamp.t").desc()).limit(100).rdd.map(lambda row: row.asDict()).collect()

def run_analytics():
    # Placeholder for Spark analytics operations
    # Perform aggregations, joins, or other analysis here
    return {"summary": "Analytics results"}
