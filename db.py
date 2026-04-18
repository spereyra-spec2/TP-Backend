import mysql.connector
import config


def get_connection(): #Establece conneción con la base de datos.
    return mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
    )

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
            
def partido_tiene_resultado(partido_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT resultado_local, resultado_visitante 
            FROM partidos 
            WHERE id = %s
        """, (partido_id,))
        partido = cur.fetchone()
        return partido and (partido.get('resultado_local') is not None or 
                           partido.get('resultado_visitante') is not None)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def existe_prediccion(usuario_id, partido_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            SELECT id FROM predicciones 
            WHERE usuario_id = %s AND partido_id = %s
        """, (usuario_id, partido_id))
        return cur.fetchone() is not None
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def guardar_prediccion(usuario_id, partido_id, goles_local, goles_visitante):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute("""
            INSERT INTO predicciones (usuario_id, partido_id, goles_local_pred, goles_visitante_pred, fecha_prediccion)
            VALUES (%s, %s, %s, %s, NOW())
        """, (usuario_id, partido_id, goles_local, goles_visitante))
        conn.commit()
        
        nuevo_id = cur.lastrowid
        cur.execute("""
            SELECT id, usuario_id, partido_id, goles_local_pred, goles_visitante_pred, fecha_prediccion
            FROM predicciones WHERE id = %s
        """, (nuevo_id,))
        return cur.fetchone()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
