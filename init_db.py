import mysql.connector

with open('DB.sql', 'r') as file:
    sql_script = file.read()

conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='123789', # La que pusiste en VS Code
    database='Constantino' # El nombre de tu base de datos
)


cursor = conn.cursor()
for statement in sql_script.split(';'):
    if statement.strip():
        print(statement)  # Para que veas qué se está ejecutando
        cursor.execute(statement)
        conn.commit()
        print("Ejecutado con éxito")
cursor.close()
conn.close()