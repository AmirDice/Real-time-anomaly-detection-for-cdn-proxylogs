import os
import json 
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import time

if __name__ == '__main__':
    # Kafka Consumer 
    topic_name = "CDN"
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='cdn-group'
)
    # database visualization connection info
    token = "CC8zymsGh-0xRp_oMlLV2XL24sGF7mIRXugC9Hfu9FlariNPUmz7AnC_1vU-TUjPrE0RMwgodMMsyPdoJRlrFg=="
    org = "primary"
    bucket = "cdn"
    
    for message in consumer:
        #connect to influx db client
        client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        print(json.loads(message.value))
        print('Writing was successful to the Kafka topic');