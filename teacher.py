from db import get_connection

def my_courses(id):
    db=get_connection()
    cur=db.cursor()
    cur.execute("SELECT * FROM courses WHERE instructor_id=%s",(id,))
    print(cur.fetchall())
    db.close()

def earnings(id):
    db=get_connection()
    cur=db.cursor()
    cur.execute("""SELECT SUM(p.amount)
    FROM courses c JOIN payments p ON c.course_id=p.course_id
    WHERE c.instructor_id=%s""",(id,))
    print(cur.fetchall())
    db.close()