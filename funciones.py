import mysql.connector

def get_conection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="test",
        database="IDS"
    )

def obtener_ranking(limit,offset):
    con = get_conection()
    #x=1/0 #error intencional (500)
    cursor = con.cursor(dictionary=True)
    query =f"""
        SELECT prediccion.id_usuario, 
        SUM(
            CASE 
                WHEN prediccion.local = partidos.local AND prediccion.visitante = partidos.visitante THEN 3
                
                WHEN SIGN(prediccion.local - prediccion.visitante) = SIGN(partidos.local - partidos.visitante) THEN 1
                
                ELSE 0 
            END
        ) AS puntos
    FROM prediccion
    JOIN partidos ON prediccion.id_partido = partidos.id_partido
    GROUP BY prediccion.id_usuario
    ORDER BY puntos DESC ASC
    LIMIT {limit} OFFSET {offset}
    """
    cursor.execute(query)
    ranking = cursor.fetchall()
    cursor.close()
    con.close()
    return ranking