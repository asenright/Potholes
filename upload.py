import urllib2
import config
import time
import MySQLdb
import logging
import threading
from datetime import datetime

###Requires MySQLdb to run.
###Install with "sudo apt-get install python-mysqldb"

class upload(threading.Thread):
	global logger, curDT
	logger = logging.getLogger()      
	
	if __name__ == "__main__":
		main()

	def main(self):
		self.start()
		
	def __init__(self):
		threading.Thread.__init__(self)
		logging.debug('Initialized Upload')
     		   
	def run(self):
		logging.debug('Running Upload')
		while (config.exitFlag == False):
			curDT = datetime.utcnow().strftime("%Y-%m-%d %X")
			if (self.internet_access() == True):
				logging.debug('Uploader executing at ' + curDT)
				###Connect to DB
				with MySQLdb.connect(host=config.mySqlHostname, user=config.mySqlUsername, passwd=config.mySqlPassword,db=config.mySqlDbName) as db:			
					logging.debug('Connected to db')
					###Open script
					with open(config.mySqlUploadScriptName, 'r') as sqlScript:
						logging.debug('Read script' + config.mySqlUploadScriptName)
						sql = " ".join(file.readlines())
						###Get cursor and execute
						with db.cursor() as cursor:
							cur.execute(sql)
							logging.debug('Read script' + config.mySqlUploadScriptName)			
			else:
				pass
			logging.debug('Upload sleeping for ' + str(config.uploadTimer) + ' seconds')
			time.sleep(config.uploadTimer)
		logging.debug('Upload closed nicely')
		exit(0)
		
	def internet_access(self):
		try:
			logging.debug('Checking for internet access...')
			urllib2.urlopen(config.testAddress, timeout = 3)
			logging.debug('Unit has internet access.')
			return True
		except urllib2.URLError as err:
			return False
			

	# def run_sql_file(self, filename, connection):
		# start = time.time()
    		# file = open(filename, 'r')
    		# sql = " ".join(file.readlines())
    		# logging.debug("Start executing: " + filename + " at " + str(tdatetime.now().strftime("%Y-%m-%d %H:%M")) + "\n" + sql) 
		# with cursor = 
		# cursor.execute(sql)    
		# connection.commit()
    
		# end = time.time()
		# #print "Time elapsed to run the query:	"
		# #print str((end - start)*1000) + ' ms'
