import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="V@123456",
    database="company"
)

if connection.is_connected():
    print("Connected to MySQL successfully!")

connection.close()