import mysql.connector
import config

def get_connection(): #Establece conneción con la base de datos.
    return mysql.connector.connect(
        host=config.host,
        user=config.user,
        password=config.password,
        database=config.database
    )---

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
