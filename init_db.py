import mysql.connector

from config import user, password, database, host
import mysql.connector

def init_db():
    with open("init_db.sql") as f:
        sql = f.read()

    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
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

