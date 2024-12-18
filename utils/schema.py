from pyspark.sql.types import StructType, StructField, StringType, DoubleType

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