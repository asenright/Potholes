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
import sense_hat
from datetime import datetime
import os


class potholes (threading.Thread):
	global t_gps, t_accel, t_upload, logName, startMsgShown, hasHat

	dirname = os.path.dirname(__file__)
	outputPath = os.path.realpath(os.path.join(dirname, 'out'))
	config.outputPath = outputPath
	
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
					if t_upload == None:
						try:
							logging.debug('Creating upload thread\n')					
							t_upload = upload()
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
					logging.debug('Closing potholes...\n')
					config.exitFlag = True
					logging.debug('Potholes closed nicely.\n')
					sense.show_message("Ended", text_colour=blue)
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
			if t_upload == None:
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
				
