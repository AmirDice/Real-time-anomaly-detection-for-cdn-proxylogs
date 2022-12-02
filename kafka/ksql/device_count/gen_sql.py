file = open("commands.sql","w") 

topic='cdn-input'

root_stream_name = 'cdn_stream'
create_stream = 'create stream {} (\"$table\" VARCHAR, type VARCHAR, timestamp VARCHAR, Status_code VARCHAR, protocol VARCHAR, contentlength VARCHAR, timefirstbyte VARCHAR, timetoserv VARCHAR, osfamily VARCHAR, uamajor VARCHAR, uafamily VARCHAR, devicefamily VARCHAR, path VARCHAR, live_channel VARCHAR, devicebrand VARCHAR, method VARCHAR) WITH (KAFKA_TOPIC=\'{}\', VALUE_FORMAT=\'JSON\', PARTITIONS=1, REPLICAS=1);\n'.format(root_stream_name, topic)
file.write(create_stream)

filer_stream_name='cdn_stream_filtered'
filter_stream='create stream {} as select timestamp, timetoserv, devicefamily, devicebrand, status_code, osfamily, timefirstbyte from {};\n'.format(filer_stream_name, root_stream_name)
file.write(filter_stream)

keyed_stream_name='cdn_stream_keyed'
keyed_stream='create stream {} as select * FROM {} PARTITION BY devicebrand;\n'.format(keyed_stream_name, filer_stream_name)
file.write(keyed_stream)

device_connect_name='cdn_stream_device_brand'
device_connect='create stream {} as select *, 1 as KEYCOL from {} where devicebrand=\'1\';\n'.format(device_connect_name, keyed_stream_name)
file.write(device_connect)

device_count_table_name='cdn_table_device_count'
device_count_table='create table {} as select DEVICEBRAND, TIMETOSERV, KEYCOL, COUNT(*) AS COUNT FROM {} window tumbling (size 30 seconds) group by DEVICEBRAND, TIMETOSERV, KEYCOL;\n'.format(device_count_table_name, device_connect_name)
file.write(device_count_table)

device_count_stream_name='cdn_stream_device_count'
device_count_stream='create stream {} (DEVICEBRAND varchar, TIMETOSERV varchar, KEYCOL int, COUNT BIGINT) with (kafka_topic=\'{}\', value_format=\'JSON\', partitions=1, replicas=1);\n'.format(device_count_stream_name, device_count_table_name.upper())
file.write(device_count_stream)

file.close() 