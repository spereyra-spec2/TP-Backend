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
    except mysql.connector.Error as error:
        if error.errno == 1062:
            return "conflict"
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

def partido_tiene_resultado(partido_id):
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT resultado_local, resultado_visitante 
            FROM partidos 
            WHERE id = %s
        """, (partido_id,))
        partido = cursor.fetchone()
        
        return partido and (
            partido.get('resultado_local') is not None or 
            partido.get('resultado_visitante') is not None
        )
    except Exception as e:
        print(f"Error en partido_tiene_resultado: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def existe_prediccion(usuario_id, partido_id):
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("""
            SELECT id FROM predicciones 
            WHERE usuario_id = %s AND partido_id = %s
        """, (usuario_id, partido_id))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error en existe_prediccion: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def guardar_prediccion(usuario_id, partido_id, goles_local, goles_visitante):
    conexion = None
    cursor = None
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        
        cursor.execute("""
            INSERT INTO predicciones (usuario_id, partido_id, goles_local_pred, goles_visitante_pred, fecha_prediccion)
            VALUES (%s, %s, %s, %s, NOW())
        """, (usuario_id, partido_id, goles_local, goles_visitante))
        
        conexion.commit()
        
        nuevo_id = cursor.lastrowid
        cursor.execute("""
            SELECT id, usuario_id, partido_id, goles_local_pred, goles_visitante_pred, fecha_prediccion
            FROM predicciones WHERE id = %s
        """, (nuevo_id,))
        
        return cursor.fetchone()
    except Exception as e:
        print(f"Error en guardar_prediccion: {e}")
        if conexion:
            conexion.rollback()
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def reemplazar_partido(id, data): 
    try:
        con = get_connection()
        cursor = con.cursor()

        query= 'UPDATE partido SET equipo_local = %s, equipo_visitante = %s, fecha = %s, fase = %s WHERE id = %s'
    
        new_values= (
            data['equipo_local'],
            data['equipo_visitante'],
            data['fecha'],
            data['fase'],
            id
        )
 
        cursor.execute(query,new_values)
        con.commit()

        filas_afectadas = cursor.rowcount
    
        cursor.close()

    except Exception as e:
        print(f"Error en la base de datos: {e}")
        return False
    
    finally:
        if con and con.is_connected():
            con.close()
    
    return filas_afectadas > 0