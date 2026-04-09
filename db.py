from config import CONTRASENA_DB, NOMBRE_DB, USUARIO_DB
from typing import Any
import mysql.connector

config_db: dict[str, str] = {
    "host": "localhost",
    "user": USUARIO_DB,
    "password": CONTRASENA_DB,
    "database": NOMBRE_DB,
    # "charset": "utf8mb4",
    # "collation": "utfmb4_0900_ai_ci"
}

def obtener_conexion() -> mysql.connector.MySQLConnection:
    return mysql.connector.connect(**config_db)

def inicializar_db(path: str) -> None:
    with open(path) as archivo:
        script_sql: str = archivo.read()

    with mysql.connector.connect(
        host = config_db["host"],
        user = config_db["user"],
        password = config_db["password"],
        # charset = "utf8mb4",
        # collation = "utfmb4_0900_ai_ci"
    ) as conexion:
        # conexion.set_charset_collation("utf8mb4", "utfmb4_0900_ai_ci")
        with conexion.cursor(dictionary = True) as cursor:
            for consulta in script_sql.split(';'):
                cursor.execute(consulta)
                print(consulta)
            conexion.commit()

def ejecutar_consulta(query: str) -> list[dict[str, Any]] | None:
    with obtener_conexion() as conexion:
        # conexion.set_charset_collation("utf8mb4", "utfmb4_0900_ai_ci")
        with conexion.cursor(dictionary = True) as cursor:
            cursor.execute(query)
            print(query)

            if cursor.description:
                return cursor.fetchall()
            
            conexion.commit()