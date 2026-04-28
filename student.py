from db import get_connection

def view_students():
    db=get_connection()
    cur=db.cursor()
    cur.execute("SELECT * FROM students")
    for r in cur.fetchall(): print(r)
    db.close()