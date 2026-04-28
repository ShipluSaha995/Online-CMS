from db import get_connection

def view_courses():
    db=get_connection()
    cur=db.cursor()
    cur.execute("SELECT * FROM courses")
    for r in cur.fetchall(): print(r)
    db.close()