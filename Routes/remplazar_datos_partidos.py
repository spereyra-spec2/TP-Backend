from flask import Blueprint, jsonify, request
from db import get_connection


partidos_bp = Blueprint('partidos', __name__)


@partidos_bp.route('/<int:id>/Resultados', methods=['PUT'])
def remplazar_datos_partido(id):
    datos = request.get_json() 
    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)    
    cursor.execute("SELECT resultado FROM partido WHERE = %s", (id,))
    #Tomo el primer valor consultado.
    partido = cursor.fetchone()
        
    if not partido:
            return jsonify({"code": 404, "message": "No encontrado", "level":"error", "description": f"El partido número {id} no existe"}), 404

    try:
        
        if not datos or 'goles_local' not in datos or 'goles_visitante' not in datos:
            return jsonify({"code": 400, "message": "Petición inválida.", "level": "error", "description": "Faltan campos obligatorios",}), 400
    
        if not isinstance(datos['goles_local'], int) or not isinstance(datos['goles_visitante'], int):
            return jsonify({"code": 400, "message": "Petición inválida", "level": "error", "description": "Los datos a ingresar deben de ser un número"}), 400
        if(id < 0):
            return jsonify({"code": 400, "message": "Petición inválida", "level": "error", "description": f"El id:{id} no es un número válido"}), 400

        query = "UPDATE resultado SET local = %s, visitante = %s WHERE id = %s"
        datos_ingresados = (datos['goles_local'], datos['goles_visitante'], id)
        
        cursor.execute(query, datos_ingresados)
        conexion.commit() #Guardo cambios en la base de datos

        return '', 204
    

    except Exception as error:
        print(f"Error de MySQL: {error}")
        return jsonify({"code": 500, "message": f"{error}", "level": "error", "description": "Error interno al acceder a la base de datos"}), 500

    finally:
        cursor.close()
        conexion.close()
