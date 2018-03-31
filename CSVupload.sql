
--COMMAND Line to run .sql Script at its file location: 
--SOURCE /gaia/student/suj/190/SQL/CSVupload.sql 

--selecting 'roadtest' as our database
USE roadtest;

--delete previous old data if exists
DROP TABLE IF EXISTS analyzed;
DROP TABLE IF EXISTS acc;
DROP TABLE IF EXISTS gps;

--Creating tables for each .csv
CREATE TABLE analyzed(
time VARCHAR(15) NOT NULL,
latitude_1 VARCHAR(15) NOT NULL,
longitude_1 VARCHAR(15) NOT NULL,
latitude_2 VARCHAR(15) NOT NULL,
longitude_2 VARCHAR(15) NOT NULL,
bumps_between VARCHAR(3) NOT NULL);

CREATE TABLE acc(
X VARCHAR(15) NOT NULL,
Y VARCHAR(15) NOT NULL,
Z VARCHAR(15) NOT NULL,
time VARCHAR(15) NOT NULL);

CREATE TABLE gps(
time VARCHAR(15) NOT NULL,
num_sats VARCHAR(2) NOT NULL,
latitude VARCHAR(13) NOT NULL,
latitude_dir VARCHAR(2) NOT NULL,
logitude VARCHAR(13) NOT NULL,
longitude_dir VARCHAR(2) NOT NULL);

/*importing each .csv onto Table*/
LOAD DATA LOCAL INFILE '/gaia/class/student/suj/190/SQL/analyzed.csv'
INTO TABLE analyzed
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/gaia/class/student/suj/190/SQL/acc.csv' --
INTO TABLE acc
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE '/gaia/class/student/suj/190/SQL/gps.csv'
INTO TABLE gps
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;

--shows the data of each table
SELECT * FROM analyzed;
SELECT * FROM acc;
SELECT * FROM gps;
