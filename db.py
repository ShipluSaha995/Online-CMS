import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="!@**Data**1621101##@!",
        database="course_portal"
    )