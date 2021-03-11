#!/usr/bin/env python3
import logging
import logging.handlers
import sqlite3
import time
from w1thermsensor import W1ThermSensor

# Initialise logger
# create logger with "temperature_read"
logger = logging.getLogger("temperature_read")
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
rfh = logging.handlers.RotatingFileHandler("temperature_read.log", "a",
                                           2560000, 3)
rfh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter(
   "%(asctime)s - %(name)s - %(levelname)s - %(lineno)d: %(message)s")
rfh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(rfh)
logger.addHandler(ch)
# Define data.db directory
data_db = '/home/pi/growPiProject/data.db'

# Initialise sqlite
con = sqlite3.connect(data_db)
cur = con.cursor()

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS temperature
            (timestamp REAL, temperature1 REAL, temperature2 REAL, 
            temperature3 REAL, temperature4 REAL, temperature5 REAL)''')

# Setup sensor address
try:
    sensor1 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "800000265db7")
except Exception as e:
    logger.exception(e)
try:
    sensor2 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "041662e87fff")
except Exception as e:
    logger.exception(e)
try:
    sensor3 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "80000026d9bf")
except Exception as e:
    logger.exception(e)
try:
    sensor4 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "04166084f8ff")
except Exception as e:
    logger.exception(e)
try:
    sensor5 = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "041662af5bff")
except Exception as e:
    logger.exception(e)

# Initialise temperatures:
temp1 = 0
temp2 = 0
temp3 = 0
temp4 = 0
temp5 = 0

# Make timestamp
now = time.time()

# Read temperature
try:
    temp1 = sensor1.get_temperature()
except Exception as e:
    logger.exception(e)
try:
    temp2 = sensor2.get_temperature()
except Exception as e:
    logger.exception(e)
try:
    temp3 = sensor3.get_temperature()
except Exception as e:
    logger.exception(e)
try:
    temp4 = sensor4.get_temperature()
except Exception as e:
    logger.exception(e)
try:
    temp5 = sensor5.get_temperature()
except Exception as e:
    logger.exception(e)

# Insert a row of data
cur.execute("INSERT INTO temperature VALUES (?, ?, ?, ?, ?, ?)",
            (now, temp1, temp2, temp3, temp4, temp5))

# Save (commit) the changes
con.commit()

# Close connection
con.close()

# TODO raise SystemExit()
