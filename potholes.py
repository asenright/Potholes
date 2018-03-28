#Potholes.py
#!/usr/bin/python
import config
import threading
import time
import logging
import signal
from accelerometer import accelerometer
from gps import gps 
import sense_hat
from datetime import datetime
import os


class potholes (threading.Thread):
	global t_gps, t_accel, logName, startMsgShown, hasHat

	dirname = os.path.dirname(__file__)
	outputPath = os.path.realpath(os.path.join(dirname, 'out'))
	config.outputPath = outputPath
	
	#####All thread names go here in global#####
	
	t_gps = None
	t_accel = None
	
	curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
	
	logName = os.path.join(config.outputPath, 'potholes_ ' + curDT + '.log')
	logging.basicConfig(filename=logName,level=logging.DEBUG)
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	
	blue = [0, 125, 0]
	red = [125, 0, 0]
	startMsgShown = False

	try:
		sense = sense_hat.SenseHat()
		hasHat = True
	except OSError:
		logging.error('potholes.py : No senseHat detected; accelerometer data unavailable for this session')
		hasHat = False
		
	if (hasHat == True):
		while True:
			for event in sense.stick.get_events():
				direction = (event.direction )
				if direction == 'up':
					# direction = startCapture(direction)
					if t_gps == None:
						logging.debug('Creating GPS thread\n')
						t_gps = gps()
						t_gps.daemon = True
						t_gps.start()
					if t_accel == None:
						logging.debug('Creating accel thread\n')					
						t_accel = accelerometer()
						t_accel.daemon = True
						t_accel.start()
					if startMsgShown == False: 
						sense.show_message("Starting", text_colour=blue)
						startMsgShown = True
					time.sleep(0.5)
				elif direction == 'left':
					logging.debug('Closing potholes...\n')
					config.exitFlag = True
					logging.debug('Potholes closed nicely.\n')
					sense.show_message("Ended", text_colour=blue)
					exit(0)
				else:
					time.sleep(0.5)
	else:
		try:
			while (config.exitFlag == False):
				if t_gps == None:
					logging.debug('Creating GPS thread\n')
					t_gps = gps()
					t_gps.daemon = True
					t_gps.start()
				time.sleep(.5)
		except KeyboardInterrupt:
			config.exitFlag = True
			logging.debug('Potholes closed nicely.\n')
			time.sleep(0.5)
			exit(0)
				
