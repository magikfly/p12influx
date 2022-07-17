FROM python:3
ADD p1_to_influxdb.py /
RUN pip install config
RUN pip install influxdb-client
RUN pip install dsmr-parser
RUN mkdir /app
WORKDIR /app
COPY . /app
CMD [ "python3","-u","./p1_to_influxdb.py" ]
