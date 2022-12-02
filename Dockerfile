FROM python:3.9.5
ENV REFRESHED_AT 2021-08-15


WORKDIR /anomalydetectioncdn
ADD . /anomalydetectioncdn
RUN pip install -r requirements.txt

#docker run -it --rm kafkacsv python kafka/cdnprod.py -h

# docker run -it --rm \
#       -v $PWD:/anomalydetectioncdn \
#       kafkacsv python kafka/cdncons.py my-stream