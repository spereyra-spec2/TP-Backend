from flask import Blueprint, jsonify, request, url_for
from db import get_user, get_partido, guardar_prediccion, existe_prediccion, partido_tiene_resultado
from errors import not_found, server_error, bad_request
from datetime import datetime

predicciones_bp = Blueprint("predicciones", __name__, url_prefix="/partidos")


@predicciones_bp.route("/<int:id>/prediccion", methods=["POST"])
def agregar_prediccion(id):
    try:
        data = request.json

        if not data:
         return jsonify(bad_request("El cuerpo está vacío")), 400
        
        id_usuario = data.get("id_usuario")
        goles_local = data.get("local")
        goles_visitante = data.get("visitante")

        
        if not id_usuario:
            return jsonify(bad_request("Falta el campo id usuario")), 400
        
        if goles_local is None:
            return jsonify(bad_request("Falta el campo goles del local")), 400
        
        if goles_visitante is None:
            return jsonify(bad_request("Falta el campo goles del visitante")), 400
        
        try:
            goles_local = int(goles_local)
            goles_visitante = int(goles_visitante)
            
            if goles_local < 0 or goles_visitante < 0:
                return jsonify(bad_request("Formato de goles invalido")), 400
        except (ValueError, TypeError):
            return jsonify(bad_request("Goles inválidos")), 400
        
        partido_id = id 
        partido = get_partido(partido_id)

        if not partido:
            return jsonify(not_found), 404
        

        usuario = get_user(id_usuario)
        if not usuario:
            return jsonify(not_found), 404
        
        if partido_tiene_resultado(partido_id):
            return jsonify(bad_request("el partido ya tiene resultado")), 400
        
        if partido.get('fecha'):
            try:
                fecha_partido = datetime.fromisoformat(str(partido['fecha']))
                if fecha_partido < datetime.now():
                    return jsonify(bad_request("no se pueden agregar predicciones a este partido")), 400
            except (ValueError, TypeError):
                pass
        
        if existe_prediccion(id_usuario, partido_id):
            return jsonify(bad_request("ya hiciste una predicción")), 409
        
        prediccion = guardar_prediccion(
            usuario_id=id_usuario,
            partido_id=partido_id,
            goles_local=goles_local,
            goles_visitante=goles_visitante
        )

        if not prediccion:
            return jsonify(server_error(500)), 500
        
        
        return jsonify({
            "mensaje": "Predicción creada exitosamente",
            "prediccion": {
                "id": prediccion['id'],
                "partido_id": prediccion['id_partido'],
                "usuario_id": prediccion['id_usuario'],
                "goles_local": prediccion['local'],
                "goles_visitante": prediccion['visitante']
            }
        }), 201
        
    except Exception as e:
        print(f"Error en crear_prediccion: {e}")
        return jsonify(server_error(500)), 500