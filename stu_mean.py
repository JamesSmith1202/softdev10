import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f="discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#==========================================================
#INSERT YOUR POPULATE CODE IN THIS ZONE
def populate():

    csv_with_students_info = csv.DictReader(open("peeps.csv"))
    csv_with_course_info= csv.DictReader(open("courses.csv"))

    c.execute('CREATE TABLE students (name str, age INTEGER, id INTEGER);')
    for row in csv_with_students_info:
        c.execute("INSERT INTO students VALUES (" + "'"+row["name"]+"'," + row["age"] + "," + row["id"] + ");")

    c.execute('CREATE TABLE courses (code str, mark NUMERIC, id INTEGER);')
    for row in csv_with_course_info:
        c.execute("INSERT INTO courses VALUES (" + "'"+row["code"]+"'," + row["mark"] + "," + row["id"] + ");")

    db.commit()


#===========================================================
def see_students_grades():
    display = c.execute("SELECT name,mark FROM STUDENTS,COURSES WHERE students.id = courses.id")
    for row in display:
        print row


def find_freqency(): #finds the freqency of a paticular id

    table = c.execute("SELECT students.id FROM STUDENTS,COURSES WHERE students.id = courses.id")
    list = []
    prevnum = 1
    counter = 0
    for iden in table:
        if prevnum == iden[0]:
            counter = counter + 1
        else:
            list.append(counter)
            counter = 1
            prevnum = iden[0]
    list.append(counter)
    return list

def calculate_avg(): # finds average of all students
    grade_list = c.execute("SELECT mark FROM STUDENTS,COURSES WHERE students.id = courses.id")
    list = []
    for row in grade_list:
        list.append(row[0])
    freq = find_freqency()
    avg = []
#    print freq
#    print list
#    print "#########################################"
    for i in freq:
        num = 0
        #print i
        for n in range(0,i):
        #    print "---- list n -----"
        #    print list[n]
             num = num + list.pop(0)
        #     print list
        #     print num
        #print "---final------"
        avg.append(num/i)
    return avg

def peeptable():
        c.execute('CREATE TABLE peeps_avg(id INTEGER, average INTEGER);')
        avg_list = calculate_avg()
    #    print avg_list
        for i in range(0,len(avg_list)):
            num = i + 1
            value = avg_list[i]
        #    print value
        #    print "-----------"
            c.execute("INSERT INTO peeps_avg VALUES (" + str(num) + "," + str(value) + ");")
            db.commit()
    #    print "INSERT INTO peeps_avg VALUES (" + str(num) + "," + str(value) + ";"

    #    c.execute("INSERT INTO students VALUES (" + "'"+row["name"]+"'," + row["age"] + "," + row["id"] + ");")

def display():
    table = c.execute("SELECT name,peeps_avg.id,average FROM STUDENTS,peeps_avg  WHERE peeps_avg.id = students.id;")
    print "NAME | ID | AVERAGE"
    for i in table:
        print i[0] + "|" + str(i[1]) + "|" + str(i[2]) + "\n"
    return table








#==========================================================
populate()
peeptable()
display()
db.close()
print "Donee"
