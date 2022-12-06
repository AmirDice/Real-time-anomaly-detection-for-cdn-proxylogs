from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from influxdb_client import InfluxDBClient

import os
import sys
import json
import numpy as np
import pandas as pd
from datetime import datetime

topic_name = 'cdn'
output_topic = 'pcdn'
if __name__=="__main__":
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0 pyspark-shell'

    # Spark Instance
    spark = SparkSession.builder.appName("CDN_STREAM").getOrCreate()
    # spark.sparkContext.setLogLevel('ERROR')

    # Define an input stream
    cols = ['protocol','contentlength','timefirstbyte','osfamily','uamajor','path','devicebrand','method','timestamp']

    fields = [StructField(col_name, StringType(), True) for col_name in cols]
    schema = StructType(fields)

    # Read stream from json and fit schema
    inputStream = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "cdn")\
        .option("startingOffsets", "earliest") \
        .load()
        

    inputStream = inputStream.select(col("value").cast("string").alias("data"))
    inputStream.printSchema()

    # write stream and process
    print(f"> Reading the stream and storing ...")
    query = (inputStream
        .writeStream
        .outputMode("append")\
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("topic", output_topic)\
        .option("checkpointLocation", "checkpoints")\
        .start())

    spark.streams.awaitAnyTermination()