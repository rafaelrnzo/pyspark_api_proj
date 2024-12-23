from pyspark.sql.types import StructType, StructField, StringType, DoubleType

schema = StructType([
    StructField("fullDocument", StructType([
        StructField("_id", StructType([
            StructField("$oid", StringType(), True)
        ])),
        StructField("product", StringType(), True),
        StructField("sales", DoubleType(), True),
    ])),
    StructField("clusterTime", StructType([
        StructField("$timestamp", StructType([
            StructField("t", StringType(), True)
        ]))
    ]))
])
