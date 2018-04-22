USE roadtest;

CREATE TABLE tempAcc(
X VARCHAR(15) NOT NULL,
Y VARCHAR(15) NOT NULL,
Z VARCHAR(15) NOT NULL,
time VARCHAR(15) NOT NULL);

CREATE TABLE tempGps(
datetime VARCHAR(30) NOT NULL,
num_sats VARCHAR(3) NOT NULL,
lat VARCHAR(25) NOT NULL,
lat_dir VARCHAR(4) NOT NULL,
longi VARCHAR(25) NOT NULL,
longi_dir VARCHAR(4) NOT NULL);

CREATE TABLE tempAnalyzed(
time VARCHAR(30) NOT NULL,
lat_1 VARCHAR(25) NOT NULL,
long_1 VARCHAR(25) NOT NULL,
lat_2 VARCHAR(25) NOT NULL,
long_2 VARCHAR(25)NOT NULL,
bumps VARCHAR(10) NOT NULL);


LOAD DATA LOCAL INFILE '/gaia/class/student/suj/190/SQL/acc.csv'
INTO TABLE tempAcc
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/gaia/class/student/suj/190/SQL/gps.csv'
INTO TABLE tempGps
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/gaia/class/student/suj/190/SQL/analyzed.csv'
INTO TABLE tempAnalyzed
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

INSERT INTO acc(X, Y, Z, time)
	SELECT * FROM tempAcc;
	
INSERT INTO gps(time, num_sats, latitude, latitude_dir, logitude, longitude_dir)
	SELECT * FROM tempGps;
	
INSERT INTO analyzed(time, latitude_1, longitude_1, latitude_2, longitude_2, bumps_between)
	SELECT * FROM tempAnalyzed;

DROP TABLE IF EXISTS tempAnalyzed;
DROP TABLE IF EXISTS tempAcc;
DROP TABLE IF EXISTS tempGps;

SELECT * FROM analyzed;
SELECT * FROM acc;
SELECT * FROM gps;
