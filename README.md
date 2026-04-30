# 🎓 Online Course Management System (CMS)

**Author:** Shiplu Saha  
 
**Language:** Python 🐍 | **Database:** MySQL

---

## 📌 About

The **Online Course Management System** is a Python + MySQL console-based application that manages students, teachers, courses, enrollments, payments, and user registrations through a role-based portal. Three types of users — **Admin**, **Student**, and **Teacher** — each have their own set of actions within the system.

---

## 🗂️ Project Structure

Online-CMS/
├── main.py           # Entry point — login & role routing
├── auth.py           # Authentication logic
├── admin.py          # Admin panel actions
├── student.py        # Student panel actions
├── teacher.py        # Teacher panel actions
├── course.py         # Course management
├── enrollment.py     # Enrollment management
├── payment.py        # Payment processing
├── queries.py        # Reusable SQL query helpers
├── db.py             # MySQL database connection
└── README.md


---

## 🗃️ Database Schema

| Table               | Description                                      |
|---------------------|--------------------------------------------------|
| `users`             | Login credentials and role assignments           |
| `students`          | Student profile data                             |
| `instructors`       | Instructor profile data                          |
| `courses`           | Course catalogue linked to instructors           |
| `enrollments`       | Student–course enrollment records                |
| `payments`          | Payment records per student per course           |
| `registrations`     | Pending/approved/rejected signup requests        |
| `student_log`       | Audit log for student actions                    |
| `payment_log`       | Audit log for payment events                     |
| `registration_log`  | Audit log for registration status changes        |

### 👁️ Views

| View                       | Purpose                                               |
|----------------------------|-------------------------------------------------------|
| `v_enrolled_students`      | Joined view of enrollments with student & course info |
| `v_payment_summary`        | Payment records with student and course names         |
| `v_pending_registrations`  | All registrations awaiting admin review               |

---

## ⚙️ Database Triggers

| # | Trigger Name              | Event                     | Action                                     |
|---|---------------------------|---------------------------|--------------------------------------------|
| 1 | `student_insert`          | AFTER INSERT students     | Logs every new student added               |
| 2 | `payment_check`           | BEFORE INSERT payments    | Blocks negative payment amounts            |
| 3 | `payment_status`          | BEFORE INSERT payments    | Auto-sets status to `Paid` or `Pending`    |
| 4 | `enroll_duplicate`        | BEFORE INSERT enrollments | Prevents duplicate course enrollments      |
| 5 | `enroll_date`             | BEFORE INSERT enrollments | Auto-fills enrollment date if not provided |
| 6 | `instructor_delete`       | BEFORE DELETE instructors | Blocks deletion if instructor has courses  |
| 7 | `payment_log_tr`          | AFTER INSERT payments     | Logs every payment to `payment_log`        |
| 8 | `enroll_log`              | AFTER INSERT enrollments  | Logs every enrollment to `student_log`     |
| 9 | `registration_submit_log` | AFTER INSERT registrations| Logs new registration submissions          |
| 10| `registration_review_log` | AFTER UPDATE registrations| Logs approval/rejection status changes     |

---

## 👤 Default Login Credentials

### Admin
| Username | Password  |
|----------|-----------|
| `admin`  | `admin123`|

### Students
| Username | Password |
|----------|----------|
| `alice`  | `pass123`|
| `bob`    | `pass123`|
| `carla`  | `pass123`|
| `david`  | `pass123`|
| `eva`    | `pass123`|
| `farhan` | `pass123`|

### Teachers
| Username   | Password   |
|------------|------------|
| `rahman`   | `teach123` |
| `sultana`  | `teach123` |
| `hossain`  | `teach123` |
| `mithila`  | `teach123` |

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+
- MySQL Workbench (optional, for GUI)
- `mysql-connector-python` package

### Step 1 — Install Python dependency
```bash
pip install mysql-connector-python
```

### Step 2 — Set up the database
1. Open **MySQL Workbench** and connect to your local MySQL server.
2. Open a new SQL tab via **File → New Query Tab**.
3. Paste the full SQL script from this repository into the tab.
4. Click **Execute (⚡)** to run the entire script.

### Step 3 — Configure the database connection
Open `db.py` and update your credentials:
```python
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",           # your MySQL username
        password="yourpass",   # your MySQL password
        database="course_portal"
    )
```

### Step 4 — Run the application

Write this queries in my sql workbench
```sql
CREATE DATABASE IF NOT EXISTS course_portal;
USE course_portal;
drop database course_portal;


CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)  NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('admin','student','teacher') NOT NULL,
    student_id INT NULL,
    instructor_id INT NULL
);

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(50),
    semester INT
);

CREATE TABLE instructors (
    instructor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department VARCHAR(50)
);

CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    credit INT,
    instructor_id INT,
    FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
);

CREATE TABLE enrollments (
    enroll_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enroll_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);

CREATE TABLE payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    amount INT,
    status VARCHAR(20),
    payment_date DATE,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);



CREATE TABLE registrations (
    reg_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    username VARCHAR(50)  NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role ENUM('student','teacher') NOT NULL,
    -- student-specific fields
    department VARCHAR(50)  NULL,
    semester INT NULL,
    -- teacher-specific fields
    specialization VARCHAR(100) NULL,
    -- status & audit
    status ENUM('pending','approved','rejected') NOT NULL DEFAULT 'pending',
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_by INT NULL,          -- admin user_id who acted on this
    reviewed_at TIMESTAMP NULL,
    FOREIGN KEY (reviewed_by) REFERENCES users(user_id)
);



CREATE TABLE student_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT, 
    action VARCHAR(50),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE payment_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    amount INT,
    action VARCHAR(50),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- NEW: Registration audit log
CREATE TABLE registration_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    reg_id INT,
    action VARCHAR(50),   -- 'Submitted', 'Approved', 'Rejected'
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



DELIMITER $$

-- 1. Log every new student insert
CREATE TRIGGER student_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_log(student_id, action) VALUES (NEW.student_id, 'Added');
END$$

-- 2. Block negative payment amounts
CREATE TRIGGER payment_check
BEFORE INSERT ON payments
FOR EACH ROW
BEGIN
    IF NEW.amount < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Payment amount cannot be negative';
    END IF;
END$$

-- 3. Auto-set payment status
CREATE TRIGGER payment_status
BEFORE INSERT ON payments
FOR EACH ROW
BEGIN
    IF NEW.amount > 0 THEN
        SET NEW.status = 'Paid';
    ELSE
        SET NEW.status = 'Pending';
    END IF;
END$$

-- 4. Block duplicate enrollments
CREATE TRIGGER enroll_duplicate
BEFORE INSERT ON enrollments
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = NEW.student_id AND course_id = NEW.course_id
    ) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Student already enrolled in this course';
    END IF;
END$$

-- 5. Auto-fill enrollment date
CREATE TRIGGER enroll_date
BEFORE INSERT ON enrollments
FOR EACH ROW
BEGIN
    IF NEW.enroll_date IS NULL THEN
        SET NEW.enroll_date = CURDATE();
    END IF;
END$$

-- 6. Prevent deleting an instructor who has courses
CREATE TRIGGER instructor_delete
BEFORE DELETE ON instructors
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM courses WHERE instructor_id = OLD.instructor_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot delete instructor with assigned courses';
    END IF;
END$$

-- 7. Log every payment
CREATE TRIGGER payment_log_tr
AFTER INSERT ON payments
FOR EACH ROW
BEGIN
    INSERT INTO payment_log(student_id, amount, action)
    VALUES (NEW.student_id, NEW.amount, 'Paid');
END$$

-- 8. Log every enrollment
CREATE TRIGGER enroll_log
AFTER INSERT ON enrollments
FOR EACH ROW
BEGIN
    INSERT INTO student_log(student_id, action)
    VALUES (NEW.student_id, 'Enrolled');
END$$

-- 9. NEW: Log every new registration submission
CREATE TRIGGER registration_submit_log
AFTER INSERT ON registrations
FOR EACH ROW
BEGIN
    INSERT INTO registration_log(reg_id, action) VALUES (NEW.reg_id, 'Submitted');
END$$

-- 10. NEW: Log approval / rejection of registrations
CREATE TRIGGER registration_review_log
AFTER UPDATE ON registrations
FOR EACH ROW
BEGIN
    IF NEW.status != OLD.status THEN
        INSERT INTO registration_log(reg_id, action)
        VALUES (NEW.reg_id, IF(NEW.status = 'approved', 'Approved', 'Rejected'));
    END IF;
END$$

DELIMITER ;



-- Admin user (no student_id / instructor_id)
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'admin');

-- Instructors
INSERT INTO instructors (name, email, department) VALUES
('Dr. Rahman',   'rahman@cms.edu',   'CSE'),
('Dr. Sultana',  'sultana@cms.edu',  'EEE'),
('Dr. Hossain',  'hossain@cms.edu',  'BBA'),
('Dr. Mithila',  'mithila@cms.edu',  'CSE');

-- Courses
INSERT INTO courses (title, credit, instructor_id) VALUES
('Database Management Systems',   3, 1),
('Data Structures & Algorithms',  3, 4),
('Circuit Analysis',              3, 2),
('Business Communication',        2, 3),
('Operating Systems',             3, 1),
('Digital Marketing',             2, 3);

-- Students
INSERT INTO students (name, email, department, semester) VALUES
('Alice Haque',    'alice@mail.com',   'CSE', 1),
('Bob Mia',        'bob@mail.com',     'CSE', 2),
('Carla Ahmed',    'carla@mail.com',   'EEE', 1),
('David Islam',    'david@mail.com',   'BBA', 3),
('Eva Khanam',     'eva@mail.com',     'CSE', 4),
('Farhan Uddin',   'farhan@mail.com',  'EEE', 2);

-- Users for students (student_id links to students table)
INSERT INTO users (username, password, role, student_id) VALUES
('alice',   'pass123', 'student', 1),
('bob',     'pass123', 'student', 2),
('carla',   'pass123', 'student', 3),
('david',   'pass123', 'student', 4),
('eva',     'pass123', 'student', 5),
('farhan',  'pass123', 'student', 6);

-- Users for teachers (instructor_id links to instructors table)
INSERT INTO users (username, password, role, instructor_id) VALUES
('rahman',   'teach123', 'teacher', 1),
('sultana',  'teach123', 'teacher', 2),
('hossain',  'teach123', 'teacher', 3),
('mithila',  'teach123', 'teacher', 4);

-- Enrollments (triggers will auto-log and auto-fill date)
INSERT INTO enrollments (student_id, course_id, enroll_date) VALUES
(1, 1, '2025-01-10'),
(1, 2, '2025-01-10'),
(2, 1, '2025-01-11'),
(2, 5, '2025-01-11'),
(3, 3, '2025-01-12'),
(4, 4, '2025-01-13'),
(4, 6, '2025-01-13'),
(5, 1, '2025-01-14'),
(5, 2, '2025-01-14'),
(6, 3, '2025-01-15');

-- Payments (trigger auto-sets status to 'Paid')
INSERT INTO payments (student_id, course_id, amount, payment_date) VALUES
    (1, 1, 5000, '2025-01-10'),
    (1, 2, 5000, '2025-01-10'),
    (2, 1, 5000, '2025-01-11'),
    (2, 5, 5000, '2025-01-11'),
    (3, 3, 4500, '2025-01-12'),
    (4, 4, 3000, '2025-01-13'),
    (4, 6, 3000, '2025-01-13'),
    (5, 1, 5000, '2025-01-14'),
    (6, 3, 4500, '2025-01-15');

-- Registrations (pending / approved / rejected examples)
INSERT INTO registrations (full_name, email, username, password, role, department, semester, status) VALUES
    ('Gazi Rahim',    'gazi@mail.com',   'gazi',   'reg123', 'student', 'CSE', 1, 'pending'),
    ('Hena Begum',    'hena@mail.com',   'hena',   'reg123', 'student', 'EEE', 2, 'approved'),
    ('Imran Sikder',  'imran@mail.com',  'imran',  'reg123', 'student', 'BBA', 1, 'rejected');

INSERT INTO registrations (full_name, email, username, password, role, specialization, status) VALUES
    ('Dr. Nahar',     'nahar@cms.edu',   'nahar',  'teach456', 'teacher', 'Machine Learning', 'pending'),
    ('Dr. Karim',     'karim@cms.edu',   'karim',  'teach456', 'teacher', 'Power Systems',    'approved');



CREATE OR REPLACE VIEW v_enrolled_students AS
SELECT
    s.student_id,
    s.name AS student_name,
    s.department,
    c.title AS course_title,
    i.name AS instructor_name,
    e.enroll_date
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
JOIN instructors i ON c.instructor_id = i.instructor_id;

CREATE OR REPLACE VIEW v_payment_summary AS
SELECT
    s.name AS student_name,
    c.title AS course_title,
    p.amount,
    p.status,
    p.payment_date
FROM payments p
JOIN students s ON p.student_id = s.student_id
JOIN courses c ON p.course_id = c.course_id;

CREATE OR REPLACE VIEW v_pending_registrations AS
SELECT
    reg_id, full_name, email, role,
    IFNULL(department, specialization) AS dept_or_spec,
    semester, reg_date
FROM registrations
WHERE status = 'pending';


```


### Step 5 — Run the application
```bash
python main.py
```

---

## 🛠️ MySQL Workbench Queries

### 📂 Basic Table Queries

```sql
-- View all users
SELECT * FROM users;

-- View all students
SELECT * FROM students;

-- View all instructors
SELECT * FROM instructors;

-- View all courses
SELECT * FROM courses;

-- View all enrollments
SELECT * FROM enrollments;

-- View all payments
SELECT * FROM payments;

-- View all registrations
SELECT * FROM registrations;
```

---

### 📊 Joined / Reporting Queries

```sql
-- All courses with instructor names
SELECT c.course_id, c.title, c.credit, i.name AS instructor, i.department
FROM courses c
JOIN instructors i ON c.instructor_id = i.instructor_id;

-- All enrollments with student and course details
SELECT e.enroll_id, s.name AS student, s.department,
       c.title AS course, e.enroll_date
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id;

-- All payments with student and course details
SELECT p.payment_id, s.name AS student, c.title AS course,
       p.amount, p.status, p.payment_date
FROM payments p
JOIN students s ON p.student_id = s.student_id
JOIN courses c ON p.course_id = c.course_id;

-- Count of courses each instructor teaches
SELECT i.name AS instructor, COUNT(c.course_id) AS total_courses
FROM instructors i
LEFT JOIN courses c ON i.instructor_id = c.instructor_id
GROUP BY i.name;

-- Count of enrollments per course
SELECT c.title AS course, COUNT(e.enroll_id) AS total_students
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.title;

-- Total payment collected per student
SELECT s.name AS student, SUM(p.amount) AS total_paid
FROM payments p
JOIN students s ON p.student_id = s.student_id
GROUP BY s.name;

-- Students who have NOT made any payment
SELECT s.name, s.email
FROM students s
LEFT JOIN payments p ON s.student_id = p.student_id
WHERE p.payment_id IS NULL;

-- Find all courses a specific student is enrolled in
SELECT s.name, c.title, i.name AS instructor, e.enroll_date
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
JOIN instructors i ON c.instructor_id = i.instructor_id
WHERE s.name = 'Alice Haque';

-- Find all students enrolled under a specific instructor
SELECT DISTINCT s.name AS student, s.department, c.title AS course
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN courses c ON e.course_id = c.course_id
JOIN instructors i ON c.instructor_id = i.instructor_id
WHERE i.name = 'Dr. Rahman';
```

---

### 👁️ Using the Views

```sql
-- All enrolled students with full details
SELECT * FROM v_enrolled_students;

-- Filter view by department
SELECT * FROM v_enrolled_students WHERE department = 'CSE';

-- Full payment summary
SELECT * FROM v_payment_summary;

-- Only paid records from payment summary
SELECT * FROM v_payment_summary WHERE status = 'Paid';

-- All pending registrations
SELECT * FROM v_pending_registrations;
```

---

### 📋 Registration Management (Admin)

```sql
-- View all registrations with their status
SELECT reg_id, full_name, email, role,
       IFNULL(department, specialization) AS dept_or_spec,
       status, reg_date
FROM registrations;

-- View only pending registrations
SELECT * FROM registrations WHERE status = 'pending';

-- View only approved registrations
SELECT * FROM registrations WHERE status = 'approved';

-- Approve a pending registration
UPDATE registrations
SET status = 'approved', reviewed_at = NOW()
WHERE username = 'gazi';

-- Reject a pending registration
UPDATE registrations
SET status = 'rejected', reviewed_at = NOW()
WHERE username = 'imran';
```

---

### 📜 Audit Log Queries

```sql
-- View student activity log with names
SELECT sl.log_id, s.name AS student, sl.action, sl.log_time
FROM student_log sl
JOIN students s ON sl.student_id = s.student_id
ORDER BY sl.log_time DESC;

-- View payment log with student names
SELECT pl.log_id, s.name AS student, pl.amount, pl.action, pl.log_time
FROM payment_log pl
JOIN students s ON pl.student_id = s.student_id
ORDER BY pl.log_time DESC;

-- View registration audit log with applicant names
SELECT rl.log_id, r.full_name, r.role, rl.action, rl.log_time
FROM registration_log rl
JOIN registrations r ON rl.reg_id = r.reg_id
ORDER BY rl.log_time DESC;
```

---

### 🧪 Trigger Test Queries

```sql
-- TEST 1: Duplicate enrollment — should raise trigger error
-- (Student 1 is already enrolled in Course 1)
INSERT INTO enrollments (student_id, course_id) VALUES (1, 1);

-- TEST 2: Negative payment — should raise trigger error
INSERT INTO payments (student_id, course_id, amount, payment_date)
VALUES (1, 1, -500, CURDATE());

-- TEST 3: Delete instructor with courses — should raise trigger error
-- (Instructor 1 has assigned courses)
DELETE FROM instructors WHERE instructor_id = 1;

-- TEST 4: Valid new enrollment (auto-fills date via trigger)
INSERT INTO enrollments (student_id, course_id) VALUES (6, 2);

-- TEST 5: Valid payment (trigger auto-sets status to 'Paid')
INSERT INTO payments (student_id, course_id, amount, payment_date)
VALUES (5, 2, 5000, CURDATE());
-- Verify the auto-status:
SELECT * FROM payments ORDER BY payment_id DESC LIMIT 1;
```

---

## 🧩 Role-Based Features

### 🔑 Admin
- Manage all students, teachers, and courses
- Approve or reject pending registration requests
- View all payment and enrollment records
- Access full audit logs

### 🧑‍🎓 Student
- Browse and enroll in available courses
- Make course payments
- View personal enrollment and payment history

### 👨‍🏫 Teacher
- View assigned courses
- View students enrolled in their courses

---

## 📄 License

This project is open-source and free to use for educational purposes.

---

*Made with ❤️ by [Shiplu Saha](https://github.com/ShipluSaha995)*