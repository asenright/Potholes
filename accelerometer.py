import time
import csv
import sys
import threading
import logging
from datetime import datetime
from sense_hat import SenseHat

class accelerometer(threading.Thread):
	global exitFlag
	exitFlag = False
	
	global x, y, z, timestamp
	global sense
	
	sense = SenseHat()
	x = []
	y = []
	z = []
	timestamp = []
	sense.clear()
	blue = [0, 125, 0]
	red = [125, 0, 0]
	
	global logger
	logger = logging.getLogger('potholes')
	logger.setLevel(logging.DEBUG)
	
	x[:] = []
	y[:] = []
	z[:] = []
	timestamp[:] = []

	def __init__(self):
		logging.debug('Initialized Accel')
		sense.clear()

	def getAccelerometer():
		global x,y,z
		accelerometer_data = sense.get_accelerometer_raw()
		x.append(accelerometer_data['x'])
		y.append(accelerometer_data['y'])
		z.append(accelerometer_data['z'])
		
	def getTime():
		global timestamp
		timestamp.append(datetime.datetime.now().strftime("%H:%M:%S:%f"))

	def buildAccelerometerCSV():
		logging.debug('Building accel csv...')
		global x,y,z, timestamp
		filename = '/home/pi/Desktop/190/data/acc'+datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S") +'.csv'
		file_writer = csv.writer(open(filename, 'w'), delimiter=',')
		file_writer.writerow(["X", "Y", "Z", "Time hour:minute:second:microsecond"])
		for i in range(len(x)):
			file_writer.writerow([x[i], y[i], z[i], timestamp[i]])
		logging.debug('Accelerometer csv built')
			
	def run(self):
		logger.debug('Running Accel')
		sense.show_message("Starting", text_colour=blue)
		while exitFlag == False:
			getAccelerometer()
			getTime()
		buildAccelerometerCSV()
		sense.show_message("Ended", text_colour=blue)
		
    