from db import get_connection

def view_students():
    db=get_connection()
    cur=db.cursor()
    cur.execute("SELECT * FROM students")
    for r in cur.fetchall(): print(r)
    db.close()

def view_teachers():
    db=get_connection()
    cur=db.cursor()
    cur.execute("SELECT * FROM instructors")
    for r in cur.fetchall(): print(r)
    db.close()

def view_courses():
    db=get_connection()
    cur=db.cursor()
    cur.execute("SELECT * FROM courses")
    for r in cur.fetchall(): print(r)
    db.close()

def add_course():
    db=get_connection()
    cur=db.cursor()

    title=input("Title: ")
    credit=int(input("Credit: "))
    tid=int(input("Instructor ID: "))

    cur.execute(
        "INSERT INTO courses(title,credit,instructor_id) VALUES(%s,%s,%s)",
        (title,credit,tid)
    )

    db.commit()
    db.close()
    print("Course added")