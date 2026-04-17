import mysql.connector

with open('init.sql', 'r') as file:
    sql_script = file.read()

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='root', )


cursor = conn.cursor()
for statement in sql_script.split(';'):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Ejecutado con éxito")
cursor.close()
conn.close()
