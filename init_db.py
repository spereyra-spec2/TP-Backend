import mysql.connector

with open ("init_db.py") as f:
    sql = f.read()

conn = mysql.connector.connect(  #Nos conectamos con el motor de base de datos
    host="localhost",
    user="root",
    passwd="test"
)

cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Instrucción ejecutada")

cursor.close()
conn.close()