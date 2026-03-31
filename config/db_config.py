import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="quiz_db"
    )
    return connection
