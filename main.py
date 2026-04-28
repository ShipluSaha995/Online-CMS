from auth import login, reset_password, register_student, register_teacher
from enrollment import enroll
from payment import pay
from queries import run_query
from admin import (
    view_students, view_teachers, view_courses, add_course,
    view_pending_registrations, approve_registration,
    reject_registration, view_registration_log
)
from teacher import my_courses, students_in_courses, earnings

while True:
    print("\n===== ONLINE CMS =====")
    print("1 Login")
    print("2 Register Student")
    print("3 Register Teacher")
    print("4 Reset Password")
    print("5 Exit")

    ch = int(input())

    if ch == 1:
        res = login()
        if not res:
            print("Invalid login")
            continue

        role, sid, tid = res

        if role == "admin":
            from db import get_connection
            db  = get_connection()
            cur = db.cursor()
            cur.execute("SELECT user_id FROM users WHERE role='admin' LIMIT 1")
            admin_row = cur.fetchone()
            admin_user_id = admin_row[0] if admin_row else None
            db.close()

            while True:
                print("\nADMIN MENU")
                print("1  View Students")
                print("2  View Teachers")
                print("3  View Courses")
                print("4  Add Course")
                print("5  Run Queries")
                print("6  Pending Registrations")
                print("7  Approve Registration")
                print("8  Reject Registration")
                print("9  Registration Log")
                print("10 Exit")

                c = int(input())
                if   c == 1:  view_students()
                elif c == 2:  view_teachers()
                elif c == 3:  view_courses()
                elif c == 4:  add_course()
                elif c == 5:  run_query()
                elif c == 6:  view_pending_registrations()
                elif c == 7:  approve_registration(admin_user_id)
                elif c == 8:  reject_registration(admin_user_id)
                elif c == 9:  view_registration_log()
                else:         break

        elif role == "student":
            while True:
                print("\nSTUDENT MENU")
                print("1 Enroll")
                print("2 Payment")
                print("3 Exit")

                c = int(input())
                if   c == 1: enroll(sid)
                elif c == 2: pay(sid)
                else:        break

        
        elif role == "teacher":
            while True:
                print("\nTEACHER MENU")
                print("1 My Courses")
                print("2 Students Count")
                print("3 Earnings")
                print("4 Exit")

                c = int(input())
                if   c == 1: my_courses(tid)
                elif c == 2: students_in_courses(tid)
                elif c == 3: earnings(tid)
                else:        break

    elif ch == 2:
        register_student()

    elif ch == 3:
        register_teacher()

    elif ch == 4:
        reset_password()

    else:
        break
