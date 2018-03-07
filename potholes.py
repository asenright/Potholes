#Potholes.py
#!/usr/bin/python

import threading
import time
import accelerometer
import gps


exitFlag = 0

class potholes (threading.Thread):
	def __init__ (self, name):
		print "Creating GPS thread"
		t_gps = threading.Thread(target=run_gps(),name="gpsThread",args=())
		t_gps.daemon = False
		print "Creating accel thread"
		t_accel = threading.Thread(target=run_gps(),name="gpsThread",args=())
		t_accel.daemon = False
		
		print "Starting..."
		t_gps.start()
		t_accel.start()

		