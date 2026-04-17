import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='test', #Password correcta
        database='test' #Luego CORREGIR DATABASE
    )

#Nos CONECTAMOS con la BASE DE DATOS