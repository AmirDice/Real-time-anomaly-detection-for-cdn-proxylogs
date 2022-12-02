FROM python:3.8.6-alpine
WORKDIR /code
RUN apk add --no-cache gcc musl-dev linux-headers librdkafka-dev build-base
RUN apk add librdkafka-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
#CMD ["python", "cdncons.py"]

