#Potholes.py
#!/usr/bin/python

import threading
import time
import logging
from accelerometer import accelerometer
from gps import gps 
from sense_hat import SenseHat
from datetime import datetime

import config

class potholes (threading.Thread):
	sense = SenseHat()
	
	#####All thread names go here in global#####
	global t_gps, t_accel
	t_gps = None
	t_accel = None
	
	curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
	
	logName = 'potholes_ ' + curDT + '.log'
	logging.basicConfig(filename=logName,level=logging.DEBUG)
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	
	while True:
		for event in sense.stick.get_events():
			direction = (event.direction )
			if direction == 'up':
				# direction = startCapture(direction)
				if t_gps == None:
					logging.debug('Creating GPS thread\n')
					t_gps=threading.Thread(target=gps)
					t_gps.daemon = True
					t_gps.start()
					t_gps.join()
					
				if t_accel == None:
					logging.debug('Creating accel thread\n')
					t_accel=threading.Thread(target=accelerometer)
					t_accel.daemon = True
					t_accel.start()
					t_accel.join()
				
			# This functionality should be relocated to accelerometer 
			# elif direction == 'down':
				# endCapture()
				# reset()
			elif direction == 'left':
				logging.debug('Closing potholes...\n')
				config.exitFlag = True
				logging.debug('Potholes closed nicely.\n')
				exit()
			else:
				time.sleep(.5)
		