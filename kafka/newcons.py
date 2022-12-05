import os
import json 
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from datetime import datetime

    # Kafka Consumer 
topic_name = "cdn"
consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='cdn-group'
)
    # database visualization connection info
token = "hX641N2prnezgaopCHbeXFRQHMIL7OXcisZBYB5Vb4CbZsQSHz5OLSZiR87Wo8DhHApQ1kmNOkReq88FW-6e4w=="
org = "cdn"
bucket = "cdn"
    
for message in consumer:
        mvalue = json.loads(message.value.decode('utf-8'))
        mkey = message.key
        mpart = message.partition
        moffset = message.offset

        client = InfluxDBClient(url="http://localhost:8086", username="admin", password="password123", token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        print(message)
        
        dataPoint = Point("cdnproxyData")\
        .field('protocol', float(mvalue['protocol'])) \
        .field('contentlength', float(mvalue['contentlength'])) \
        .field('timefirstbyte', float(mvalue['timefirstbyte'])) \
        .field('osfamily', float(mvalue['osfamily'])) \
        .field('uamajor', float(mvalue['uamajor'])) \
        .field('path', float(mvalue['path'])) \
        .field('devicebrand', float(mvalue['devicebrand'])) \
        .field('method', float(mvalue['method'])) \
        .time(datetime.strptime(mvalue['timestamp'], '%Y-%m-%d %H:%M:%S') )


        print(dataPoint)

        write_api.write(bucket=bucket, record=dataPoint)
        
        print('Writing was successful to Kafka topic');
