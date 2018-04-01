#Potholes.py
#!/usr/bin/python
import config
import threading
import time
import logging
import signal
from accelerometer import accelerometer
from gps import gps 
from upload import upload
from sense_hat import SenseHat
from datetime import datetime
import os
import sys


class potholes (threading.Thread):
	global t_gps, t_accel, t_upload, logName, startMsgShown, hasHat

	dirname = os.path.dirname(__file__)
	outputPath = os.path.realpath(os.path.join(dirname, 'out'))
	config.outputPath = outputPath
	if not os.path.exists(outputPath):
		os.makedirs(outputPath)
	
	#####All thread names go here in global#####
	
	t_gps = None
	t_accel = None
	t_upload = None
	
	curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
	
	logName = os.path.join(config.outputPath, 'potholes_ ' + curDT + '.log')
	logging.basicConfig(filename=logName,level=logging.DEBUG)
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	
	blue = [0, 125, 0]
	red = [125, 0, 0]
	startMsgShown = False

	#We want exactly 3 arguments: script name, username, and password.
	#One argument is fine too for now, this is just the script name.
	if len(sys.argv) != 3:
			print 'Expected usage: "potholes.py mySqlUsername mySqlPassword"'
			config.mySqlUsername = None
			config.mySqlPassword = None
	else:
		config.mySqlUsername = sys.argv[1]
		config.mySqlPassword = sys.argv[2]
		
	try:
            sense = SenseHat()
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
						try:
							logging.debug('Creating GPS thread\n')
							t_gps = gps()
							t_gps.daemon = True
							t_gps.start()
						except: 
							logging.error('Error starting GPS thread\n')
							pass
					if t_accel == None:
						try:
							logging.debug('Creating accel thread\n')					
							t_accel = accelerometer()
							t_accel.daemon = True
							t_accel.start()
						except:
							logging.error('Error starting accel thread\n')
							pass
					if config.mySqlUsername == None or config.mySqlPassword == None:
						logging.debug('Username or password has not been given for the database; skipping upload thread')	
					elif t_upload == None:
						try:
							logging.debug('Creating upload thread\n')					
							t_upload = upload(config)
							t_upload.daemon = True
							t_upload.start()	
						except:
							logging.error('Error starting accel thread\n')
							pass
					if startMsgShown == False: 
						sense.show_message("Starting", text_colour=blue)
						startMsgShown = True
					time.sleep(0.5)
				elif direction == 'left':
					config.exitFlag = True
					logging.debug('Potholes closed nicely.\n')
					time.sleep(0.1)
					exit(0)
				else:
					time.sleep(0.5)
	else:
		try:
			if t_gps == None:
				logging.debug('Creating GPS thread\n')
				t_gps = gps()
				t_gps.daemon = True
				t_gps.start()
			if config.mySqlUsername == None or config.mySqlPassword == None:
				logging.debug('Username or password has not been given for the database; skipping upload thread')	
			elif t_upload == None:
				logging.debug('Creating upload thread\n')					
				t_upload = upload()
				t_upload.daemon = True
				t_upload.start()	
			while (config.exitFlag == False):
				time.sleep(config.uploadTimer)
		except KeyboardInterrupt:
			config.exitFlag = True
			logging.debug('Potholes closed nicely.\n')
			time.sleep(0.1)
			exit(0)