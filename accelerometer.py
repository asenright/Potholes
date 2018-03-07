import time
import datetime
import csv
import sys
from sense_hat import SenseHat

sense = SenseHat()
x = []
y = []
z = []
timestamp = []
sense.clear()
blue = [0, 125, 0]
red = [125, 0, 0]

def reset():
    global x, y, z, timestamp
    x[:] = []
    y[:] = []
    z[:] = []
    timestamp[:] = []
    sense.clear()

def getAccelerometer():
    global x,y,z
    accelerometer_data = sense.get_accelerometer_raw()
    x.append(accelerometer_data['x'])
    y.append(accelerometer_data['y'])
    z.append(accelerometer_data['z'])

def getTime():
    global timestamp
    timestamp.append(datetime.datetime.now().strftime("%H:%M:%S:%f"))

     
def buildAccelerometerCSV():
    global x,y,z, timestamp
    filename = '/home/pi/Desktop/190/data/acc'+datetime.datetime.now().strftime("%Y_%m_%d %H:%M:%S") +'.csv'
    file_writer = csv.writer(open(filename, 'w'), delimiter=',')
    file_writer.writerow(["X", "Y", "Z", "Time hour:minute:second:microsecond"])
    for i in range(len(x)):
        file_writer.writerow([x[i], y[i], z[i], timestamp[i]])
        
def startCapture(direction):
    sense.show_message("Starting", text_colour=blue)
    while direction != 'down':
        for event in sense.stick.get_events():
            direction = (event.direction)
        getAccelerometer()
        getTime()
    return 'down'

def endCapture():
    sense.show_message("Ended", text_colour=blue)
    buildAccelerometerCSV()
    
while True:
    for event in sense.stick.get_events():
        direction = ( event.direction )
        if direction == 'up':
            direction = startCapture(direction)
        elif direction == 'down':
            endCapture()
            reset()
        elif direction == 'left':
            sys.exit()
        else:
            time.sleep(.5)
    
    
    
"""for i in range(1,10):
    getAccelerometer()
    getTime()
buildAccelerometerCSV()
"""      
#for i in range(len(x)):
  #  print(x[i])