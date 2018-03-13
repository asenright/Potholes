import time
import datetime
import csv
import sys
import threading
from sense_hat import SenseHat

class accelerometer(threading.Thread):
	sense = SenseHat()
	x = []
	y = []
	z = []
	timestamp = []
	sense.clear()
	blue = [0, 125, 0]
	red = [125, 0, 0]

	def __init__():
		print "Initialized Accel"
		global x, y, z, timestamp
		x[:] = []
		y[:] = []
		z[:] = []
		timestamp[:] = []
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
		global x,y,z, timestamp
		filename = '/home/pi/Desktop/190/data/acc'+datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S") +'.csv'
		file_writer = csv.writer(open(filename, 'w'), delimiter=',')
		file_writer.writerow(["X", "Y", "Z", "Time hour:minute:second:microsecond"])
		for i in range(len(x)):
			file_writer.writerow([x[i], y[i], z[i], timestamp[i]])
			
	def run(exitFlag):
		sense.show_message("Starting", text_colour=blue)
		while exitFlag == False:
			getAccelerometer()
			getTime()
		sense.show_message("Ended", text_colour=blue)
		buildAccelerometerCSV()
    