#!/usr/bin/env python

'''
This script is:
1) Spark is "grabbing" JSON all files in S3 created from API calls,
2) Spark converts JSON files to PARQUET files and dump into S3 bucket
'''

# Imports
from pyspark.sql import SparkSession
from pyspark import SparkContext

#
sc = SparkContext("local")
spark = SparkSession(sc)

# Reads JSON files from S3 bucket qpxexpress
flights = spark.read.json('s3a://qpxexpress/2017/*/*/*') # spark dataframe

# Dumps DF data into parquet file flights_parquet, dumps file in S3 bucket "qpxexpress_parquet"
flights.write.parquet('s3a://qpxexpressparquet/flights_parquet')
