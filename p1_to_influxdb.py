0#!/usr/bin/python3

from dsmr_parser import telegram_specifications, obis_references
from dsmr_parser.clients import SerialReader, SERIAL_SETTINGS_V5
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pprint
import config
import decimal
import time
import datetime
import logging
import sys

	
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',stream=sys.stdout, level=logging.INFO)

while True:
    try:
        #influx db settings
        db = influxdb_client.InfluxDBClient(url=config.url, token=config.token, org=config.org)
        write_api = db.write_api(write_options=SYNCHRONOUS)
        #serial port settings and version
        serial_reader = SerialReader(
            device=config.serial_port,
            serial_settings=SERIAL_SETTINGS_V5,
            telegram_specification=telegram_specifications.V5
        )

        #read telegrams
        logging.info("Waiting for P1 port measurement..")
        for telegram in serial_reader.read():
            #print(telegram)
            #report=[]
            #print(next_call)
            #create influx measurement record
            for key,value in telegram.items():
                name=key
                if hasattr(value, "value"):
                    #determine obis name
                    for obis_name in dir(obis_references):
                        if getattr(obis_references,obis_name)==key:
                            name=obis_name
                            break
                    #Filter out failure log entries
                    if name!="POWER_EVENT_FAILURE_LOG": 
                    #is it a number?
                        if isinstance(value.value, int) or isinstance(value.value, decimal.Decimal):
                           write_api.write("energy", "home",influxdb_client.Point("measurement").field(name,float(value.value)))
            #pprint.pprint(influx_measurement)
        time.sleep(15)
    except Exception as e:
        logging.error(str(e))
        logging.info("Pausing and restarting...")
        time.sleep(10)



