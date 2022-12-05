create stream cdn_stream ("$table" VARCHAR, type VARCHAR, timestamp VARCHAR, Status_code VARCHAR, protocol VARCHAR, contentlength VARCHAR, timefirstbyte VARCHAR, timetoserv VARCHAR, osfamily VARCHAR, uamajor VARCHAR, uafamily VARCHAR, devicefamily VARCHAR, path VARCHAR, live_channel VARCHAR, devicebrand VARCHAR, method VARCHAR) WITH (KAFKA_TOPIC='cdn-input', VALUE_FORMAT='JSON', PARTITIONS=1, REPLICAS=1);
create stream cdn_stream_filtered as select timestamp, timetoserv, devicefamily, devicebrand, status_code, osfamily, timefirstbyte from cdn_stream;
create stream cdn_stream_keyed as select * FROM cdn_stream_filtered PARTITION BY devicebrand;
create stream cdn_stream_device_brand as select *, 1 as KEYCOL from cdn_stream_keyed where devicebrand='1';
create table cdn_table_device_count as select DEVICEBRAND, TIMETOSERV, KEYCOL, COUNT(*) AS COUNT FROM cdn_stream_device_brand window tumbling (size 30 seconds) group by DEVICEBRAND, TIMETOSERV, KEYCOL;
create stream cdn_stream_device_count (DEVICEBRAND varchar, TIMETOSERV varchar, KEYCOL int, COUNT BIGINT) with (kafka_topic='CDN_TABLE_DEVICE_COUNT', value_format='JSON', partitions=1, replicas=1);
