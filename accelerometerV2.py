import time
import csv
import config
import sys
import threading
import logging
from datetime import datetime
from sense_hat import SenseHat
import os

"""change import sense_hat to import sense_emu to use emulator"""

class accelerometer(threading.Thread):
	global x, y, z, timestamp, red, blue
	global sense
	
        global logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
		
	x = []
	y = []
	z = []
	timestamp = []
	
	x[:] = []
	y[:] = []
	z[:] = []
	timestamp[:] = []
	
	
	filename = os.path.join(config.outputPath, 'Acc_'+ datetime.now().strftime("%Y_%m_%d %H:%M:%S") +'.csv')
	config.AccelFilename = filename
	file_writer = csv.writer(open(filename, 'w'), delimiter=',')
	file_writer.writerow(["X", "Y", "Z", "Time hour:minute:second:microsecond"])
	

	def __init__(self):
                global sense
		threading.Thread.__init__(self)
		logging.debug('Initialized Accel\n')
		try:
        	        sense = SenseHat()
	        except:
                	logging.error('accelerometer.py: SenseHat not attached. No accelerometer data will be available for this session.')
			return(0)

		sense.clear()

	def getAccelerometer(self):
		global x,y,z,timestamp
		logger.debug('Running Accelerometer\n')
		accelerometer_data = sense.get_accelerometer_raw()
		file_writer.writerow([x.append(accelerometer_data['x']), y.append(accelerometer_data['y']),z.append(accelerometer_data['z']), timestamp.append(datetime.now().strftime("%H:%M:%S:%f"))])
		
	def run(self):
	
		while config.exitFlag == False:
			self.getAccelerometer()
			#self.getTime()
		logger.debug('Closing Accelerometer\n')
		self.buildAccelerometerCSV()
		exit(0)

		
	#def getTime(self):
	#	global timestamp
	#	timestamp.append(datetime.now().strftime("%H:%M:%S:%f"))

	#def buildAccelerometerCSV(self):
		#logging.debug('Building accel csv...')
		#global x,y,z, timestamp
		#filename = os.path.join(config.outputPath, 'Acc_'+ datetime.now().strftime("%Y_%m_%d %H:%M:%S") +'.csv')
		#config.AccelFilename = filename
		#file_writer = csv.writer(open(filename, 'w'), delimiter=',')
		#file_writer.writerow(["X", "Y", "Z", "Time hour:minute:second:microsecond"])
		#for i in range(len(x)):
		#	file_writer.writerow([x[i], y[i], z[i], timestamp[i]])
		#logging.debug('Accelerometer csv built\n')
