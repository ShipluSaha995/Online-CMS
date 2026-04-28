from db import get_connection
import random


def register_student():
    db = get_connection()
    cur = db.cursor()

    name  = input("Full Name: ")
    email = input("Email: ")
    dept  = input("Department: ")
    sem   = int(input("Semester: "))
    u     = input("Username: ")
    p     = input("Password: ")

    try:
        cur.execute(
            """INSERT INTO registrations
               (full_name, email, username, password, role, department, semester)
               VALUES (%s, %s, %s, %s, 'student', %s, %s)""",
            (name, email, u, p, dept, sem)
        )
        db.commit()
        print("Registration submitted! Please wait for admin approval.")
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()



def register_teacher():
    db = get_connection()
    cur = db.cursor()

    name  = input("Full Name: ")
    email = input("Email: ")
    spec  = input("Specialization: ")
    u     = input("Username: ")
    p     = input("Password: ")

    try:
        cur.execute(
            """INSERT INTO registrations
               (full_name, email, username, password, role, specialization)
               VALUES (%s, %s, %s, %s, 'teacher', %s)""",
            (name, email, u, p, spec)
        )
        db.commit()
        print("Registration submitted! Please wait for admin approval.")
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()


def login():
    db  = get_connection()
    cur = db.cursor()

    u = input("Username: ")
    p = input("Password: ")

    cur.execute(
        "SELECT role, student_id, instructor_id FROM users WHERE username=%s AND password=%s",
        (u, p)
    )
    res = cur.fetchone()
    db.close()
    return res



def reset_password():
    db  = get_connection()
    cur = db.cursor()

    u   = input("Username: ")
    otp = str(random.randint(1000, 9999))
    print("OTP:", otp)

    if input("Enter OTP: ") == otp:
        new = input("New password: ")
        cur.execute("UPDATE users SET password=%s WHERE username=%s", (new, u))
        db.commit()
        print("Password updated!")

    db.close()
