from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

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