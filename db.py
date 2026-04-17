import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="P!assW0rd33",
        database="basedatos"
    )
