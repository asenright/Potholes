#Potholes.py
#!/usr/bin/python
import config
import threading
import time
import logging
import signal
from accelerometer import accelerometer
from gps import gps 
from sense_hat import SenseHat
from datetime import datetime
import os


class potholes (threading.Thread):
	sense = SenseHat()
	
	#####All thread names go here in global#####
	global t_gps, t_accel
	t_gps = None
	t_accel = None
	
	curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
	
	logName = 'out/potholes_ ' + curDT + '.log'
	logging.basicConfig(filename=logName,level=logging.DEBUG)
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	
	blue = [0, 125, 0]
	red = [125, 0, 0]
	startMsgShown = False
	
	while True:
		for event in sense.stick.get_events():
			direction = (event.direction )
			if direction == 'up':
				# direction = startCapture(direction)
				if t_gps == None:
					logging.debug('Creating GPS thread\n')
					#t_gps=threading.Thread(target=gps)
					t_gps = gps()
					t_gps.daemon = True
					t_gps.start()
					
				if t_accel == None:
					logging.debug('Creating accel thread\n')
					# t_accel=threading.Thread(target=accelerometer)
					t_accel = accelerometer()
					t_accel.daemon = True
					t_accel.start()
				if startMsgShown == False: 
					sense.show_message("Starting", text_colour=blue)
					startMsgShown = True
				time.sleep(0.5)
			# This functionality should be relocated to accelerometer 
			# elif direction == 'down':
				# endCapture()
				# reset()
			elif direction == 'left':
				logging.debug('Closing potholes...\n')
				config.exitFlag = True
				logging.debug('Potholes closed nicely.\n')
				sense.show_message("Ended", text_colour=blue)
				exit(0)
			else:
				time.sleep(.5)
