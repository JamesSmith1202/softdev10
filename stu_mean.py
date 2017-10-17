import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O

f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE

def populate(executable, fileName, tableName):
    with open(fileName, 'rb') as csvfile0:
        reader = csv.reader(csvfile0)#get a normal line reader
        headers = reader.next()#get a list of the headers
    with open(fileName) as csvfile1:
        reader = csv.DictReader(csvfile1)#swap to read as dict
        for row in reader:
            exestr = "INSERT INTO " + tableName + " VALUES ( \""+row[headers[0]]+"\", \""+row[headers[1]]+"\", \""+row[headers[2]]+"\");"
            executable.execute(exestr)

c.execute("CREATE TABLE courses ( code TEXT, mark INTEGER, id INTEGER);")
c.execute("CREATE TABLE peeps ( name TEXT, age INTEGER, id INTEGER);")

populate(c, "courses.csv", "courses")
populate(c, "peeps.csv", "peeps")

#==========================================================
db.commit() #save changes
db.close()  #close database


