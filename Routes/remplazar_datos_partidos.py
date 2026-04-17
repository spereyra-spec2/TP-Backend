from flask import Blueprint, jsonify, request
from db import get_db_connection


partidos_bp = Blueprint('partidos', __name__)


@partidos_bp.route('/Partidos/<int:id>/Resultados', methods=['PUT'])
def remplazar_datos_partido(id):
    #Abro conexión a la base de datos y creo un cursor para ejecutar consultas
    datos = request.get_json() 
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)    
    cursor.execute("SELECT id FROM partidos WHERE id = %s", (id,))
    #Tomo el primer valor consultado.
    partido = cursor.fetchone()
        
    if not partido:
            return jsonify({"code": 404, "description": f"El partido número {id} no existe"}), 404

    try:
        
        if not datos or 'goles_local' not in datos or 'goles_visitante' not in datos:
            return jsonify({"code": 400, "description": "Faltan campos obligatorios"}), 400
    
        if not isinstance(datos['goles_local'], int) or not isinstance(datos['goles_visitante'], int):
            return jsonify({"code": 400, "description": "Los datos a ingresar deben de ser un número"}), 400
        if(id < 0):
            return jsonify({"code": 400, "description": f"El id:{id} no es un número válido "}), 400

        query = "UPDATE partidos SET goles_local = %s, goles_visitante = %s WHERE id = %s"
        datos_ingresados = (datos['goles_local'], datos['goles_visitante'], id)
        
        cursor.execute(query, datos_ingresados)
        conexion.commit() #Guardo cambios en la base de datos

        return jsonify({"code": 204, "description": ''}), 204
    

    except mysql.connector.Error as error:
        print(f"Error de MySQL: {error}")
        return jsonify({"code": 500, "description": "Error interno al acceder a la base de datos"}), 500

    finally:
        cursor.close()
        conexion.close()