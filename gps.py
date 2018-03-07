#gps.py
#A script to pull GPS data.
# Uses the pynmea2 library.
# Pynmea2 can be installed via "pip install pynmea2".
#
#

#! /usr/bin/env python
import serial
import csv
import pynmea2
import sys
from datetime import datetime
def run_gps():
	ser = serial.Serial(
		port='/dev/ttyS0',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=1
	)

	print "Is Serial Open? " + str(ser.isOpen())
	curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
	print "Current DT: "+curDT
	with open("test.csv", 'wb') as csvfile:
		csvWriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
		headers = ["datetime", "num_sats", "latitude", "latitude_dir", "longitude", "longitude_dir"]
		csvWriter.writerow(headers)
		while True:
			try: 
				line = ser.readline()
				print line	
				if '$GPGGA' in line:
					#print line
					msg = pynmea2.parse(line)
					print "---Number of satellites in comms range: " + msg.num_sats
					if msg.num_sats == "00":
						print "!!! Warning !!! No satellites in range, long and lat likely inaccurate"
					print "---Latitude: " + msg.lat + " " + msg.lat_dir
					print "---Longitude: " + msg.lon + " " + msg.lon_dir
					curRow = [curDT, msg.num_sats, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir]
					csvWriter.writerow(curRow)
			except (RuntimeError, TypeError, NameError):
				print "General exception. Closing down."
				raise SystemExit
