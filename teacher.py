from db import get_connection

def my_courses(tid):
    db = get_connection()
    cur = db.cursor()

    cur.execute("SELECT course_id,title FROM courses WHERE instructor_id=%s",(tid,))
    for r in cur.fetchall():
        print(r)

    db.close()


def students_in_courses(tid):
    db = get_connection()
    cur = db.cursor()

    cur.execute("""
    SELECT c.title, COUNT(e.student_id)
    FROM courses c
    LEFT JOIN enrollments e ON c.course_id=e.course_id
    WHERE c.instructor_id=%s
    GROUP BY c.course_id
    """,(tid,))

    for r in cur.fetchall():
        print(r)

    db.close()


def earnings(tid):
    db = get_connection()
    cur = db.cursor()

    cur.execute("""
    SELECT c.title, SUM(p.amount)
    FROM courses c
    LEFT JOIN payments p ON c.course_id=p.course_id
    WHERE c.instructor_id=%s
    GROUP BY c.course_id
    """,(tid,))

    for r in cur.fetchall():
        print(r)

    db.close()