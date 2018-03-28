import urllib2
import config
import time
import MySQLdb as mdb
import logging
import threading
from datetime import datetime

###Requires MySQLdb to run.
###Install with "sudo apt-get install python-mysqldb"

class upload(threading.Thread):
	global logger, curDT
	logger = logging.getLogger()      

	def __init__(self):
		threading.Thread.__init__(self)
		logger.debug('Initialized Upload\n')
     		   
	def run(self):
		logger.debug('Running Upload\n')
		while (config.exitFlag == False):
			curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
			if (self.internet_access() == True):
				logger.debug('Uploader executing at ' + curDT)
				myConnection = pymysql.connect( host=config.databaseLocation, user=config.mySqlUsername, passwd=config.mySqlPassword, db=config.databaseName )
			else:
				pass
			time.sleep(config.uploadTimer)
		logger.debug('Upload closed nicely\n')
		exit(0)
		
	def internet_access(self):
		try:
			urllib2.urlopen(config.testAddress, timeout = 3)
			return True
		except urllib2.URLError as err:
			return False
			

	def run_sql_file(self, filename, connection):
		start = time.time()
    		file = open(filename, 'r')
    		sql = " ".join(file.readlines())
    		logger.debug("Start executing: " + filename + " at " + str(tdatetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql) 
		cursor = connection.cursor()
		cursor.execute(sql)    
		connection.commit()
    
		end = time.time()
		print "Time elapsed to run the query:	"
		print str((end - start)*1000) + ' ms'
