Steps:

-Create KSQL commands file (commands.sql)
	cd ksql/device_count; python gen_sql.py

-Bring up all services: 
	cd docker; docker-compose up -d --force-recreate --build

-Set up grafana dashboard (first time or if not using persistent storage to local volume)

-Use producer program to generate data
	cd producer; python producer_confluent.py -i data_all.json -t time

-Bring down all services (Make sure to do this)
	cd docker; docker-compose down