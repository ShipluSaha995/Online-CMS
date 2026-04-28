from db import get_connection
from datetime import date

def enroll(student_id):
    db=get_connection()
    cur=db.cursor()

    cid=int(input("Course ID: "))
    cur.execute("INSERT INTO enrollments(student_id,course_id,enroll_date) VALUES(%s,%s,%s)",
                (student_id,cid,date.today()))

    db.commit()
    db.close()