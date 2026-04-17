import mysql.connector


def get_con():
    return mysql.connector.connect(
        host="localhost",
        user="desarrollador",      
        password="batman",
        database="mundial_db"
    )

def reemplazar_partido(id, data): 
    try:
        con = get_con()
        cursor = con.cursor()

        query= 'UPDATE partidos SET equipo_local = %s, equipo_visitante = %s, fecha = %s, fase = %s WHERE id = %s'
    
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