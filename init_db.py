from config import PATH_SEED
from db import ejecutar_consulta, inicializar_db
import mysql.connector

if __name__ == "__main__":
    try:
        inicializar_db("./scripts/prode.sql")

        if ejecutar_consulta("SELECT COUNT(*) AS total FROM `prode`.`partido`")[0]["total"] == 0:
            with open(PATH_SEED) as archivo:
                seed: str = archivo.read()
            ejecutar_consulta(seed)
            print(seed)

        print("Base de datos inicializada exitosamente.")
    except FileNotFoundError:
        print("Error al inicializar la base de datos: No se encontró el archivo SQL.")
    except mysql.connector.Error as error:
        print(f"Error al inicializar la base de datos: {error}")