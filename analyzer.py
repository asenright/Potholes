#analyzer.py
#looks at gps.csv and acc.csv to count bumps and make analyzed.csv

import csv

yaxis = []
threshold = 1.4000
longitude = []
latitude = []
gps_time = []
acc_time = []
bumpList = []

def fullParse():
    try:
        with open('out/gps.csv', 'r') as gpsfile:
            gps_file = csv.reader(gpsfile, delimiter = ',')
            next(gps_file)
            for row in gps_file:
                gps_time.append(row[0])
                latitude.append(float(row[2]))
                longitude.append(float(row[4]))
    except:
        print("error parsing gps.csv")
        exit()
    try:    
        with open('out/acc.csv', 'r') as accfile:
            acc_file = csv.reader(accfile, delimiter = ',')
            next(acc_file)
            for row in acc_file:
                yaxis.append(float(row[2]))
                acc_time.append(row[3])
    except:
        print("error parsing acc.csv")
        exit()
                
def bumpCounter(yaxis):
    in_bump = False
    bumpcount = 0
    for i, j in enumerate(yaxis[:-1]):
        if (abs(j-yaxis[i+1]) > threshold) and (in_bump==False):
            bumpcount+=1
            in_bump = True
        elif(in_bump):
            if ((j>yaxis[i-1]) and (j>yaxis[i+1])):
                in_bump= False
            if ((j<yaxis[i-1]) and (j<yaxis[i+1])):
                in_bump = False
    return bumpcount

def isBetween(acceltime, gpstime1, gpstime2):
    acc_split = list(map(int, acceltime.split(':')))
    gps1_split = list(map(int, gpstime1.split(':')))
    gps2_split = list(map(int, gpstime2.split(':')))
    
    totalacc = acc_split[0]*3600 + acc_split[1]*60 + acc_split[2] + float(acc_split[3]*0.000001)
    totalgps1 = gps1_split[0]*3600 + gps1_split[1]*60 + gps1_split[2] + float(gps1_split[3]*0.000001)
    totalgps2 = gps2_split[0]*3600 + gps2_split[1]*60 + gps2_split[2] + float(gps2_split[3]*0.000001)
    
    if((totalacc>= totalgps1) and (totalacc<=totalgps2)):
        return True
    else:
        return False
def outputCSV():
    file_writer = csv.writer(open('out/analyzed.csv', 'w'), delimiter = ',')
    file_writer.writerow(["time hh:mm:ss:microseconds", "latitude 1", "longitude 1", "latitude 2", "longitude 2", "bumps between"])
    for i, row in enumerate(gps_time[:-1]):
        file_writer.writerow([row, latitude[i], longitude[i], latitude[i+1], longitude[i+1], bumpList[i+1]])

def main():
    fullParse()
    acc_data = []
    global bumpList
    z = 0
    bumpList.append(0)
    for i, j in enumerate(gps_time[:-1]):
        acc_data[:] = []
        while (isBetween(acc_time[z], j, gps_time[i+1])== False):
            z=z+1
        while (isBetween(acc_time[z], j, gps_time[i+1])):
            acc_data.append(yaxis[z])
            z=z+1
        bumpList.append(bumpCounter(acc_data))
    outputCSV()

if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    