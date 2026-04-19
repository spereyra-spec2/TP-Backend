from typing import Any
import mysql.connector
import config


def get_connection(): #Establece conneción con la base de datos.
    return mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
    )

def ejecutar_consulta(query: str) -> list[dict[str, Any]] | None:
    with get_connection() as conexion:
        # conexion.set_charset_collation("utf8mb4", "utfmb4_0900_ai_ci")
        with conexion.cursor(dictionary = True) as cursor:
            cursor.execute(query)
            print(query)

            if cursor.description:
                return cursor.fetchall()
            
            conexion.commit()

def get_user(id): #Obtiene el usuario con el ID introducido en la base de datos.
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("SELECT id, nombre, email FROM usuarios WHERE id = %s", (id,))
        return cur.fetchone()  # Devuelve el usuario encontrado por su ID. Si no se encuentra, devuelve None.
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def put_user(data,id): #Actualiza los datos del usuario con el ID proporcionado para la base de datos.
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
                    UPDATE usuarios
                    SET nombre = %s,
                        email  = %s
                    WHERE id = %s""",
                    (data["nombre"], data["email"], id))
        conn.commit()
        if cur.rowcount > 0:
            return True

        return False
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def delete_user(id): # Elimina los datos del usuario con el ID proporcionado para la base de datos.
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        if cur.rowcount > 0:
            return True
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def obtener_ranking(limit, offset):
    con = get_connection()
    # x=1/0 #error intencional (500)
    cursor = con.cursor(dictionary=True)
    query = f"""
        SELECT prediccion.id_usuario, 
        SUM(
            CASE 
                WHEN prediccion.local = partidos.local AND prediccion.visitante = partidos.visitante THEN 3

                WHEN SIGN(prediccion.local - prediccion.visitante) = SIGN(partidos.local - partidos.visitante) THEN 1

                ELSE 0 
            END
        ) AS puntos
    FROM prediccion
    JOIN partidos ON prediccion.id_partido = partidos.id
    GROUP BY prediccion.id_usuario
    ORDER BY puntos DESC
    LIMIT {limit} OFFSET {offset}
    """
    cursor.execute(query)
    ranking = cursor.fetchall()
    cursor.close()
    con.close()
    return ranking

