import csv
import matplotlib
from matplotlib import pyplot

f = open('Data1.csv')
csv_f = csv.reader(f)
yaxis = []
time = []
for row in csv_f:
    yaxis.append(float(row[2]))
    time_split = list(map(int, row[3].split(':')))
    time.append(time_split[0]*3600 + time_split[1]*60 + time_split[2] + float(time_split[3]*0.000001))
pyplot.plot(time,yaxis)
pyplot.xlabel('Time')
pyplot.ylabel('Y-axis')
pyplot.show()

f.close()
    
    
