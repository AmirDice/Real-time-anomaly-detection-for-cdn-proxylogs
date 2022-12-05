Steps:


-Bring up all services: 
	cd docker; docker-compose up -d --force-recreate --build

-Set up grafana dashboard (first time or if not using persistent storage to local volume)

-Use producer program to generate data
	 python ./kafka/prod.py

- Consume data
         Python ./kafka/newcons.py

Make sure you create your personal api token from influx then stop the service
And start again with your new apitoken

- influxdb host - localhost:8086
- grafana - localhost:3000
- spark - localhost:8080

-Bring down all services (Make sure to do this)
docker-compose down
