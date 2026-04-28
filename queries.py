from db import get_connection

queries = [

    # BASIC (10) 

    ("View all students",               "SELECT * FROM students"),
    ("View all instructors",            "SELECT * FROM instructors"),
    ("View all courses",                "SELECT * FROM courses"),
    ("View all enrollments",            "SELECT * FROM enrollments"),
    ("View all payments",               "SELECT * FROM payments"),
    ("Student names and emails",        "SELECT name, email FROM students"),
    ("Instructor names and departments","SELECT name, department FROM instructors"),
    ("Course titles and credits",       "SELECT title, credit FROM courses"),
    ("User roles",                      "SELECT username, role FROM users"),
    ("Student IDs and names",           "SELECT student_id, name FROM students"),

    # FILTER (10) 

    ("Students from CSE",           "SELECT * FROM students WHERE department='CSE'"),
    ("Students in semester 1",      "SELECT * FROM students WHERE semester=1"),
    ("Courses with credit >= 3",    "SELECT * FROM courses WHERE credit>=3"),
    ("Paid payments",               "SELECT * FROM payments WHERE status='Paid'"),
    ("CSE instructors",             "SELECT * FROM instructors WHERE department='CSE'"),
    ("Students starting with A",    "SELECT * FROM students WHERE name LIKE 'A%'"),
    ("Courses containing Data",     "SELECT * FROM courses WHERE title LIKE '%Data%'"),
    ("Students above semester 2",   "SELECT * FROM students WHERE semester>2"),
    ("Payments above 5000",         "SELECT * FROM payments WHERE amount>5000"),
    ("Student users",               "SELECT * FROM users WHERE role='student'"),

    #  JOIN (10) 

    ("Students with courses",
     """SELECT s.name, c.title
        FROM students s
        JOIN enrollments e ON s.student_id=e.student_id
        JOIN courses c ON e.course_id=c.course_id"""),

    ("Courses with instructors",
     """SELECT c.title, i.name
        FROM courses c
        JOIN instructors i ON c.instructor_id=i.instructor_id"""),

    ("Students with enrollment dates",
     """SELECT s.name, e.enroll_date
        FROM students s
        JOIN enrollments e ON s.student_id=e.student_id"""),

    ("Students with payments",
     """SELECT s.name, c.title, p.amount
        FROM students s
        JOIN payments p ON s.student_id=p.student_id
        JOIN courses c ON p.course_id=c.course_id"""),

    ("Instructor courses",
     """SELECT i.name, c.title
        FROM instructors i
        JOIN courses c ON i.instructor_id=c.instructor_id"""),

    ("Courses per student",
     """SELECT s.name, COUNT(e.course_id)
        FROM students s
        JOIN enrollments e ON s.student_id=e.student_id
        GROUP BY s.student_id"""),

    ("Students per course",
     """SELECT c.title, COUNT(e.student_id)
        FROM courses c
        JOIN enrollments e ON c.course_id=e.course_id
        GROUP BY c.course_id"""),

    ("Student-course inner join",
     """SELECT s.name, c.title
        FROM students s
        INNER JOIN enrollments e ON s.student_id=e.student_id
        INNER JOIN courses c ON e.course_id=c.course_id"""),

    ("Courses with instructor (left join)",
     """SELECT c.title, i.name
        FROM courses c
        LEFT JOIN instructors i ON c.instructor_id=i.instructor_id"""),

    ("Cross join example",
     "SELECT s.name, c.title FROM students s, courses c LIMIT 10"),

    # AGGREGATE (10) 

    ("Total students",          "SELECT COUNT(*) FROM students"),
    ("Total courses",           "SELECT COUNT(*) FROM courses"),
    ("Total enrollments",       "SELECT COUNT(*) FROM enrollments"),
    ("Total payments",          "SELECT COUNT(*) FROM payments"),
    ("Average course credit",   "SELECT AVG(credit) FROM courses"),
    ("Maximum payment",         "SELECT MAX(amount) FROM payments"),
    ("Minimum payment",         "SELECT MIN(amount) FROM payments"),
    ("Students by department",  "SELECT department, COUNT(*) FROM students GROUP BY department"),
    ("Payments by status",      "SELECT status, COUNT(*) FROM payments GROUP BY status"),
    ("Enrollments per course",  "SELECT course_id, COUNT(*) FROM enrollments GROUP BY course_id"),

    #  ADVANCED (10) 

    ("Top courses by students",
     """SELECT c.title, COUNT(e.student_id)
        FROM courses c
        LEFT JOIN enrollments e ON c.course_id=e.course_id
        GROUP BY c.course_id
        ORDER BY COUNT(e.student_id) DESC"""),

    ("Top students by courses",
     """SELECT s.name, COUNT(e.course_id)
        FROM students s
        JOIN enrollments e ON s.student_id=e.student_id
        GROUP BY s.student_id
        ORDER BY COUNT(e.course_id) DESC"""),

    ("Students without enrollment",
     "SELECT name FROM students WHERE student_id NOT IN (SELECT student_id FROM enrollments)"),

    ("Courses without students",
     "SELECT title FROM courses WHERE course_id NOT IN (SELECT course_id FROM enrollments)"),

    ("Unique departments",  "SELECT DISTINCT department FROM students"),
    ("Unique roles",        "SELECT DISTINCT role FROM users"),

    ("Recent enrollments",
     """SELECT s.name, c.title
        FROM students s
        JOIN enrollments e ON s.student_id=e.student_id
        JOIN courses c ON e.course_id=c.course_id
        WHERE e.enroll_date >= '2025-01-01'"""),

    ("Courses earning above 1000",
     """SELECT c.title, SUM(p.amount)
        FROM courses c
        JOIN payments p ON c.course_id=p.course_id
        GROUP BY c.course_id
        HAVING SUM(p.amount) > 1000"""),

    ("Payments sorted descending",
     """SELECT s.name, c.title, p.amount
        FROM students s
        JOIN payments p ON s.student_id=p.student_id
        JOIN courses c ON p.course_id=c.course_id
        ORDER BY p.amount DESC"""),

    ("Instructor earnings",
     """SELECT i.name, SUM(p.amount)
        FROM instructors i
        JOIN courses c ON i.instructor_id=c.instructor_id
        JOIN payments p ON c.course_id=p.course_id
        GROUP BY i.instructor_id"""),

    #  TRIGGER TESTS (8) 

    ("Trigger: Insert student (log)",
     "INSERT INTO students(name,email,department,semester) VALUES ('TriggerTest','t@mail.com','CSE',1)"),

    ("Trigger: Negative payment error",
     "INSERT INTO payments(student_id,course_id,amount,status,payment_date) VALUES (1,1,-100,'',CURDATE())"),

    ("Trigger: Auto payment status",
     "INSERT INTO payments(student_id,course_id,amount,status,payment_date) VALUES (1,1,2000,'',CURDATE())"),

    ("Trigger: Duplicate enrollment",
     "INSERT INTO enrollments(student_id,course_id,enroll_date) VALUES (1,1,CURDATE())"),

    ("Trigger: Auto enroll date",
     "INSERT INTO enrollments(student_id,course_id,enroll_date) VALUES (2,1,NULL)"),

    ("Trigger: Delete instructor blocked",
     "DELETE FROM instructors WHERE instructor_id=1"),

    ("View student logs",   "SELECT * FROM student_log"),
    ("View payment logs",   "SELECT * FROM payment_log"),

    # REGISTRATION & NEW TABLES (10) 

    ("View all registrations",
     "SELECT * FROM registrations"),

    ("Pending registrations",
     "SELECT reg_id, full_name, email, role, IFNULL(department, specialization) AS dept_or_spec, reg_date FROM registrations WHERE status='pending'"),

    ("Approved registrations",
     "SELECT * FROM registrations WHERE status='approved'"),

    ("Rejected registrations",
     "SELECT * FROM registrations WHERE status='rejected'"),

    ("Registration log",
     "SELECT * FROM registration_log ORDER BY log_time DESC"),

    ("Pending student registrations",
     "SELECT reg_id, full_name, email, department, semester, reg_date FROM registrations WHERE role='student' AND status='pending'"),

    ("Pending teacher registrations",
     "SELECT reg_id, full_name, email, specialization, reg_date FROM registrations WHERE role='teacher' AND status='pending'"),

    ("View enrolled students (view)",
     "SELECT * FROM v_enrolled_students"),

    ("View payment summary (view)",
     "SELECT * FROM v_payment_summary"),

    ("View pending registrations (view)",
     "SELECT * FROM v_pending_registrations"),
]


def run_query():
    db = get_connection()
    cur = db.cursor()

    print("\n===== QUERY MENU =====")
    for i, (desc, _) in enumerate(queries):
        print(f"{i+1}. {desc}")

    choice = int(input("Select query: "))
    if 1 <= choice <= len(queries):
        query = queries[choice - 1][1]
        try:
            cur.execute(query)
            if query.strip().upper().startswith("SELECT"):
                rows = cur.fetchall()
                for row in rows:
                    print(row)
            else:
                db.commit()
                print("Operation successful (trigger executed if defined)")
        except Exception as e:
            print("Error:", e)
    else:
        print("Invalid choice")

    db.close()
