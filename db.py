import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123789',
        database='Constantino',
        auth_plugin='mysql_native_password'
    )