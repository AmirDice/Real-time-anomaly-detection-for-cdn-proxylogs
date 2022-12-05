from kafka import KafkaConsumer, KafkaProducer
import json
from json import loads
from csv import DictReader
import time

print("Producer started")
# initialize KafkaProducer
bootstrap_servers = ['localhost:9092']
topicname = 'CDN'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers)
producer = KafkaProducer()
print("Producer initialized, reading data....")

# open csv data
with open('./kafka/data/sdata.csv','r') as new_obj:
    csv_dict_reader = DictReader(new_obj)
    index = 0
    # run throw row
    for row in csv_dict_reader:
        producer.send(topicname, json.dumps(row).encode('utf-8'))
        print("Data delivered",row)
        index += 1
        if (index % 20) == 0:
            time.sleep(10)
