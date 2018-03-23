import csv

yaxis = []
threshold = .7000

def basicParse():
    with open('data1.csv', 'r') as csvfile:
            datafilereader = csv.reader(csvfile, delimiter=',')
        
        
            #skip first line of .csv
            next(datafilereader)
        
            #get all y axis data
            for row in datafilereader:
                yaxis.append(float(row[2]))
                
def bumpCounter(yaxis):
    in_bump = False
    bumpcount = 0
    for i, j in enumerate(yaxis[:-1]):
        if (abs(j-yaxis[i+1]) > threshold) and (in_bump==False):
            bumpcount+=1
            in_bump = False
        elif(in_bump):
            if ((j>yaxis[i-1]) and (j>yaxis[i+1])):
                in_bump= False
            if ((j<yaxis[i-1]) and (j<yaxis[i+1])):
                in_bump = False
    return bumpcount

def main():
    basicParse()
    print(bumpCounter(yaxis))
    
if __name__ == "__main__":
    main()