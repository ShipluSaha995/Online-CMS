from auth import login, reset_password
from queries import run_query
from student import view_students
from course import view_courses
from enrollment import enroll
from payment import pay
from teacher import my_courses, earnings

role,user=login()

if role is None:
    if input("Reset? y/n: ")=='y':
        reset_password()
    role,user=login()

while True:
    print("\n===== MENU =====")

    if role=="admin":
        print("1 Students\n2 Courses\n3 Queries\n4 Exit")
        ch=int(input())
        if ch==1: view_students()
        elif ch==2: view_courses()
        elif ch==3: run_query()
        else: break

    elif role=="student":
        print("1 Courses\n2 Enroll\n3 Pay\n4 Exit")
        ch=int(input())
        if ch==1: view_courses()
        elif ch==2: enroll(1)
        elif ch==3: pay(1)
        else: break

    elif role=="teacher":
        print("1 My Courses\n2 Earnings\n3 Exit")
        ch=int(input())
        if ch==1: my_courses(1)
        elif ch==2: earnings(1)
        else: break