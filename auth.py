from db import get_connection
import random

def login():
    db = get_connection()
    cur = db.cursor()

    u = input("Username: ")
    p = input("Password: ")

    cur.execute("SELECT role FROM users WHERE username=%s AND password=%s",(u,p))
    res = cur.fetchone()

    db.close()
    return res[0], u if res else (None, None)

def reset_password():
    db = get_connection()
    cur = db.cursor()

    u = input("Username: ")
    otp = str(random.randint(1000,9999))
    print("OTP:",otp)

    if input("Enter OTP: ")==otp:
        new = input("New password: ")
        cur.execute("UPDATE users SET password=%s WHERE username=%s",(new,u))
        db.commit()

    db.close()