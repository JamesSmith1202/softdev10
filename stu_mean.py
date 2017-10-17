import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE
csv_with_students_info = csv.DictReader(open("peeps.csv"))
csv_with_course_info= csv.DictReader(open("courses.csv"))
#===========================================================
c.execute('CREATE TABLE students (name str, age INTEGER, id INTEGER);')
for row in csv_with_students_info:
    c.execute("INSERT INTO students VALUES (" + "'"+row["name"]+"'," + row["age"] + "," + row["id"] + ");")

c.execute('CREATE TABLE courses (code str, mark NUMERIC, id INTEGER);')
for row in csv_with_course_info:
    code = row['code']
    mark = row['mark']
    ida = row['id']
    string = "'" +code+"'" + ',' + str(mark) + ',' +  str(ida)
    c.execute('INSERT INTO students VALUES ('+ string +');')

#command = ""          #put SQL statement in this string
#c.execute(command)    #run SQL statement

#==========================================================
db.commit() #save changes
db.close()  #close database
print "Done"

#GRAVE
'''
c.execute('CREATE TABLE students (name TEXT, age INTEGER, id NUMERIC );')
for row in csv_with_students_info:
    #print int(row["age"]) + 100
    age = str(row["age"])
    name = str(row["name"])
    id = str(row["id"])
#    c.execute('INSERT INTO students VALUES ('+ age +','+ name +','+ id +');')
    c.execute('INSERT INTO students VALUES ('+ 'name'+',7,8);') #% (name)

#===========================================================
c.execute('CREATE TABLE courses (code TEXT, mark NUMERIC, id NUMERIC );')'''
