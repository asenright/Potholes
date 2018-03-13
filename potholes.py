#Potholes.py
#!/usr/bin/python

import threading
import time
import accelerometer
import gps
from sense_hat import SenseHat

sense = SenseHat()
exitFlag = False

class potholes (threading.Thread):
	while True:
		for event in sense.stick.get_events():
			direction = (event.direction )
			if direction == 'up':
				# direction = startCapture(direction)
				t_gps = threading.Thread(target=gps)
				t_accel = threading.Thread(target=accelerometer)
				print "Creating GPS thread"
				
				t_gps.daemon = True
				print "Creating accel thread"
				t_accel.daemon = True
			
				print "Starting..."
				t_gps.start()
				t_accel.start()
			elif direction == 'down':
				endCapture()
				reset()
			elif direction == 'left':
				endCapture()
				exitFlag = True
				exit()
			else:
				time.sleep(.5)
		