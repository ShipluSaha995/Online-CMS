from db import get_connection
from datetime import date

def enroll(student_id):
    db = get_connection()
    cur = db.cursor()

    cur.execute("SELECT course_id,title FROM courses")
    for r in cur.fetchall():
        print(r)

    cid = int(input("Enter course ID: "))

    cur.execute(
        "INSERT INTO enrollments(student_id,course_id,enroll_date) VALUES(%s,%s,%s)",
        (student_id,cid,date.today())
    )

    db.commit()
    db.close()

    print("Enrolled successfully")