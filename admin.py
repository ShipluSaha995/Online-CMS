from db import get_connection



def view_students():
    db = get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM students")
    for r in cur.fetchall():
        print(r)
    db.close()

def view_teachers():
    db = get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM instructors")
    for r in cur.fetchall():
        print(r)
    db.close()

def view_courses():
    db = get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM courses")
    for r in cur.fetchall():
        print(r)
    db.close()

def add_course():
    db  = get_connection()
    cur = db.cursor()

    title  = input("Title: ")
    credit = int(input("Credit: "))
    tid    = int(input("Instructor ID: "))

    cur.execute(
        "INSERT INTO courses(title,credit,instructor_id) VALUES(%s,%s,%s)",
        (title, credit, tid)
    )
    db.commit()
    db.close()
    print("Course added")



def view_pending_registrations():
    db  = get_connection()
    cur = db.cursor()
    cur.execute(
        """SELECT reg_id, full_name, email, role,
                  IFNULL(department, specialization) AS dept_or_spec,
                  semester, reg_date
           FROM registrations
           WHERE status = 'pending'"""
    )
    rows = cur.fetchall()
    if not rows:
        print("No pending registrations.")
    else:
        print(f"\n{'ID':<5} {'Name':<20} {'Email':<25} {'Role':<8} {'Dept/Spec':<20} {'Sem':<5} {'Date'}")
        print("-" * 90)
        for r in rows:
            print(f"{r[0]:<5} {r[1]:<20} {r[2]:<25} {r[3]:<8} {str(r[4]):<20} {str(r[5]):<5} {r[6]}")
    db.close()


def approve_registration(admin_user_id):
    db  = get_connection()
    cur = db.cursor()

    view_pending_registrations()
    try:
        reg_id = int(input("\nEnter reg_id to APPROVE (0 to cancel): "))
    except ValueError:
        print("Invalid input.")
        db.close()
        return

    if reg_id == 0:
        db.close()
        return

    
    cur.execute("SELECT * FROM registrations WHERE reg_id=%s AND status='pending'", (reg_id,))
    reg = cur.fetchone()
    if not reg:
        print("Registration not found or already reviewed.")
        db.close()
        return

    
    _, full_name, email, username, password, role, department, semester, specialization, *_ = reg

    try:
        if role == 'student':
            
            cur.execute(
                "INSERT INTO students(name, email, department, semester) VALUES(%s,%s,%s,%s)",
                (full_name, email, department, semester)
            )
            sid = cur.lastrowid
            
            cur.execute(
                "INSERT INTO users(username, password, role, student_id) VALUES(%s,%s,'student',%s)",
                (username, password, sid)
            )
        else:  
            
            cur.execute(
                "INSERT INTO instructors(name, email, department) VALUES(%s,%s,%s)",
                (full_name, email, specialization)
            )
            tid = cur.lastrowid
            cur.execute(
                "INSERT INTO users(username, password, role, instructor_id) VALUES(%s,%s,'teacher',%s)",
                (username, password, tid)
            )

        
        cur.execute(
            """UPDATE registrations
               SET status='approved', reviewed_by=%s, reviewed_at=NOW()
               WHERE reg_id=%s""",
            (admin_user_id, reg_id)
        )
        db.commit()
        print(f"Registration #{reg_id} APPROVED. User account created for '{username}'.")

    except Exception as e:
        db.rollback()
        print("Error during approval:", e)
    finally:
        db.close()


def reject_registration(admin_user_id):
    db  = get_connection()
    cur = db.cursor()

    view_pending_registrations()
    try:
        reg_id = int(input("\nEnter reg_id to REJECT (0 to cancel): "))
    except ValueError:
        print("Invalid input.")
        db.close()
        return

    if reg_id == 0:
        db.close()
        return

    cur.execute("SELECT reg_id FROM registrations WHERE reg_id=%s AND status='pending'", (reg_id,))
    if not cur.fetchone():
        print("Registration not found or already reviewed.")
        db.close()
        return

    try:
        cur.execute(
            """UPDATE registrations
               SET status='rejected', reviewed_by=%s, reviewed_at=NOW()
               WHERE reg_id=%s""",
            (admin_user_id, reg_id)
        )
        db.commit()
        print(f"Registration #{reg_id} REJECTED.")
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()


def view_registration_log():
    db  = get_connection()
    cur = db.cursor()
    cur.execute("SELECT * FROM registration_log ORDER BY log_time DESC")
    rows = cur.fetchall()
    if not rows:
        print("No registration log entries.")
    else:
        print(f"\n{'LogID':<7} {'RegID':<7} {'Action':<12} {'Time'}")
        print("-" * 45)
        for r in rows:
            print(f"{r[0]:<7} {r[1]:<7} {r[2]:<12} {r[3]}")
    db.close()
