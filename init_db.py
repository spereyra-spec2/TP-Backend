from config import user, password, database, host
import mysql.connector

with open("init_db.sql") as f:
    sql = f.read()

conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
)

cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("statement executed")

cursor.close()
conn.close()
