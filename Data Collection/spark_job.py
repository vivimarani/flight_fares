#!/usr/bin/env python

'''
This script is:
1) "grabbing" files in S3 created from API calls,
2) spreading them over Spark Cluster in EMR,
3) "grabbing" data we are interested in from JSON file,
4) loading data into postgres database
'''

import pyspark
import numpy as np
# from pyspark.sql.types import FloatType
# from pyspark.sql.functions import UserDefinedFunction
# from pyspark.sql.types import IntegerType,StringType
# from pyspark.sql import SparkSession
import pandas as pd
import time
from pyspark import sparkcontext sparkconf
import yaml
import os
import ssl
# from psycopg2.extras import Json
import psycopg2
from boto.s3.connection import S3Connection
from boto.s3.key import Key

parquet_bucket_name = "qpxexpress_parquet"
credentials = yaml.load(open(os.path.expanduser(~/.ssh/'qpx_express_cred.yml')))
conn = psycopg2.connect(**credentials['qpx_express'])  # connect to API

flights = spark.read.json('s3a://qpxexpress/2017/*/*/*') # spark dataframe
# to convert RDD to DF, use .toDF()

s3_conn = S3Connection(**credentials['aws'])

try:
    bucket = conn.get_bucket(parquet_bucket_name)
except:
    bucket = conn.create_bucket(parquet_bucket_name)

flights.write.parquet('s3a://'+parquet_bucket_name)  #dumps DF to bucket as parquet
