import sys
import logging


###exitFlag is used by threads so they know when to shutdown gracefully.
global exitFlag
exitFlag = False

###These can be used to track the gps filename and accelerometer filename,
###as well as the output path.
global GPSFilename, AccelFilename
global outputPath

###How long the system should wait between checking if can upload.
global uploadTimer
uploadTimer = 10

###Name of the mySQL script that handles uploading data to DB.
global mySqlUploadScriptName, mySqlUsername, mySqlPassword, testAddress, databaseLocation, databaseName
mySqlUploadScriptName = ""
mySqlUsername = ""
mySqlPassword = ""
databaseLocation = ""
databaseName = ""
testAddress="http://8.8.8.8"