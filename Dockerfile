# FROM python:3.8.6-alpine
# WORKDIR /code
# RUN apk add --no-cache gcc musl-dev linux-headers librdkafka-dev build-base
# RUN apk add librdkafka-dev
# RUN apk add --update gcc
# RUN apk update && apk add git
# RUN apk update && apk add bash
FROM python:3.7
ADD entrypoint.sh ./kafka/newprod.py ./kafka/newcons.py ./kafka/data/* ./ 
COPY entrypoint.sh ./kafka/newprod.py ./kafka/newcons.py ./kafka/data/* ./
RUN pip install kafka-python
RUN pip install influxdb-client
# ENTRYPOINT ["bash", ".env", "entrypoint.sh"]

# RUN git clone https://github.com/edenhill/librdkafka
# RUN cd librdkafka && ./configure && make && make install && ldconfig
COPY requirements.txt ./
RUN pip install -r requirements.txt
# RUN pip install confluent-kafka
COPY . .
# CMD ["python", "./newprod.py", "./newcons.py"]
# CMD ["python", "./producer_confluent.py", "./cdncons.py"]

# ENTRYPOINT ["python", "./producer_confluent.py", "./cdncons.py"]


