#Potholes.py
#!/usr/bin/python

import threading
import time
import accelerometer
import gps

exitFlag = 0

class potholes (threading.Thread):

	while True:
		for event in sense.stick.get_events():
			direction = ( event.direction )
			if direction == 'up':
				# direction = startCapture(direction)
				
				print "Creating GPS thread"
				t_gps = threading.Thread(target=run_gps(),name="gpsThread",args=())
				t_gps.daemon = False
				print "Creating accel thread"
				t_accel = threading.Thread(target=startCapture(),name="accelThread",args=())
				t_accel.daemon = False
			
				print "Starting..."
				t_gps.start()
				t_accel.start()
			elif direction == 'down':
				endCapture()
				reset()
			elif direction == 'left':
				sys.exit()
			else:
				time.sleep(.5)
				
				
		def __init__ (self, name):


		