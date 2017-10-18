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
    try:
        c.execute('CREATE TABLE students (name str, age INTEGER, id INTEGER);')
        for row in csv_with_students_info:
            c.execute("INSERT INTO students VALUES (" + "'"+row["name"]+"'," + row["age"] + "," + row["id"] + ");")
    except:
        pass
    try:
        c.execute('CREATE TABLE courses (code str, mark NUMERIC, id INTEGER);')
        for row in csv_with_course_info:
            c.execute("INSERT INTO courses VALUES (" + "'"+row["code"]+"'," + row["mark"] + "," + row["id"] + ");")
    except:
        pass
    db.commit()


#===========================================================
def get_grades():
    grades = {}
    c.execute("SELECT id FROM students")
    ids = c.fetchall()
    for id in ids:
        c.execute("SELECT mark FROM courses WHERE id = ?", id)
        grades[id[0]] = c.fetchall()
    return grades

def calculate_avg(): # finds average for each students
    id_grades = get_grades()
    student_averages = {} #dictionary for id:average
    for student in id_grades:
        sum = 0
        count = 0
        for i in id_grades[student]:
            sum += i[0]
            count += 1
        student_averages[student] = sum/float(count)
    return student_averages

def peeptable():#creates the peeps_avg table
    try:
        c.execute('CREATE TABLE peeps_avg(id INTEGER, average INTEGER);')
        avg_dict = calculate_avg()
        for i in avg_dict:
            c.execute("INSERT INTO peeps_avg VALUES (" + str(i) + "," + str(avg_dict[i]) + ");")
            db.commit()
    except:
        print("Failed to create peeps_avg table")

def display(): #displays the peeps_avg table
    print "NAME | ID | AVERAGE"
    for i in c.execute("SELECT name,peeps_avg.id,average FROM STUDENTS,peeps_avg  WHERE peeps_avg.id = students.id;"):
        print i[0] + "|" + str(i[1]) + "|" + str(i[2])

def update_avg():#updates everyone's grades according to their current grades
    avg_dict = calculate_avg()
    for i in avg_dict:
        c.execute("UPDATE peeps_avg SET average = "+ str(avg_dict[i]) + " WHERE id = "+str(i))
    db.commit()

def update_grade(code, mark, id):
    c.execute("UPDATE courses SET mark = "+str(mark)+" WHERE id = "+str(id)+" and code = \""+code+"\"")
    db.commit()

def add_grade(code, mark, id):#adds a row to the courses table
    c.execute("INSERT INTO courses VALUES (\""+code+"\", "+str(mark)+", "+str(id)+")")
    db.commit()

#==========================================================
populate()
print("Testing calculate_avg():")
print(calculate_avg())
print("\nCreating and Displaying Peep_avg table:")
peeptable()
display()
print("\nAdding a new class with a mark of 1000 to id 10...")
add_grade("free juan thousand", 1000, 10)
print("Updating the peeps_avg table...")
update_avg()
display()
print("\nUpdating id 5's greatbooks grade to 200...")
update_grade("greatbooks", 200, 5)
print("Updating the peeps_avg table...")
update_avg()
display()
db.close()
print "\nProgram Terminated"
