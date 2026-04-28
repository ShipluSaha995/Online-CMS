from db import get_connection
from datetime import date

def pay(student_id):
    db=get_connection()
    cur=db.cursor()

    cid=int(input("Course ID: "))
    amt=int(input("Amount: "))

    cur.execute("INSERT INTO payments(student_id,course_id,amount,status,payment_date) VALUES(%s,%s,%s,'',%s)",
                (student_id,cid,amt,date.today()))

    db.commit()
    db.close()