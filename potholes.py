#Potholes.py
#!/usr/bin/python

import threading
import time
import logging
from accelerometer import accelerometer
from gps import gps 
from sense_hat import SenseHat
from datetime import datetime

class potholes (threading.Thread):
	sense = SenseHat()
	global exitFlag
	exitFlag = False
	
	#####All thread names go here in global#####
	global t_gps, t_accel
	t_gps = None
	t_accel = None
	
	curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
	logName = 'potholes_ ' + curDT + '.log'
	logging.basicConfig(filename=logName,level=logging.DEBUG)
	
	while True:
		for event in sense.stick.get_events():
			direction = (event.direction )
			if direction == 'up':
				# direction = startCapture(direction)
				if t_gps == None:
					logging.debug('Creating GPS thread')
					t_gps = threading.Thread(target=gps)
					t_gps.daemon = True
					t_gps.start()
					
				if t_accel == None:
					logging.debug('Creating accel thread')
					t_accel = threading.Thread(target=accelerometer)
					t_accel.daemon = True
					t_accel.start()
					
				
			# This functionality should be relocated to accelerometer 
			# elif direction == 'down':
				# endCapture()
				# reset()
			elif direction == 'left':
				logging.debug('Closing potholes nicely.')
				t_gps.exitFlag = True
				t_accel.exitFlag = True
				exitFlag = True
				exit()
			else:
				time.sleep(.5)
		