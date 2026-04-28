from db import get_connection
import random

# -------- STUDENT REGISTER --------
def register_student():
    db = get_connection()
    cur = db.cursor()

    name = input("Name: ")
    email = input("Email: ")
    dept = input("Department: ")
    sem = int(input("Semester: "))

    cur.execute(
        "INSERT INTO students(name,email,department,semester) VALUES(%s,%s,%s,%s)",
        (name,email,dept,sem)
    )
    sid = cur.lastrowid

    u = input("Username: ")
    p = input("Password: ")

    cur.execute(
        "INSERT INTO users(username,password,role,student_id) VALUES(%s,%s,'student',%s)",
        (u,p,sid)
    )

    db.commit()
    db.close()
    print("Student registered!")


# -------- TEACHER REGISTER --------
def register_teacher():
    db = get_connection()
    cur = db.cursor()

    name = input("Name: ")
    email = input("Email: ")
    dept = input("Department: ")

    cur.execute(
        "INSERT INTO instructors(name,email,department) VALUES(%s,%s,%s)",
        (name,email,dept)
    )
    tid = cur.lastrowid

    u = input("Username: ")
    p = input("Password: ")

    cur.execute(
        "INSERT INTO users(username,password,role,instructor_id) VALUES(%s,%s,'teacher',%s)",
        (u,p,tid)
    )

    db.commit()
    db.close()
    print("Teacher registered!")


# -------- LOGIN --------
def login():
    db = get_connection()
    cur = db.cursor()

    u = input("Username: ")
    p = input("Password: ")

    cur.execute(
        "SELECT role, student_id, instructor_id FROM users WHERE username=%s AND password=%s",
        (u,p)
    )
    res = cur.fetchone()
    db.close()

    return res


# -------- RESET PASSWORD --------
def reset_password():
    db = get_connection()
    cur = db.cursor()

    u = input("Username: ")
    otp = str(random.randint(1000,9999))
    print("OTP:", otp)

    if input("Enter OTP: ") == otp:
        new = input("New password: ")
        cur.execute("UPDATE users SET password=%s WHERE username=%s",(new,u))
        db.commit()
        print("Updated!")

    db.close()