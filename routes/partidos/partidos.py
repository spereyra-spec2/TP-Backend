from flask import Blueprint, jsonify, request
from db import get_connection
from routes.partidos.validaciones import validar_id


partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route("/<id>", methods=["GET"])
def get_partido(id):
    try:
        id = int(id)
        validar_id(id)
    except ValueError as e:
            return jsonify({
            "errors": [
                {
                    "code": "400",
                    "message": "BAD REQUEST",
                    "level": "error",
                    "description": str(e)
                }
            ]
        }), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM partido WHERE id = %s", (id,))
        partido = cursor.fetchone()
        cursor.close()
        conn.close()
    except Exception:
        return jsonify({  
        "errors": [
            {
                "code": "500",
                "message": "INTERNAL SERVER ERROR",
                "level": "error",
                "description": "Hubo un error al conectarse con la base de datos."
            }
    ]}), 500


    if not partido:
        return jsonify({
            "errors": [
                {
                    "code": "404",
                    "message": "NOT FOUND",
                    "level": "error",
                    "description": f"No se encontró el partido con id {id}."
                }
            ]
        }), 404


    partido["fecha"] = partido["fecha"].isoformat()
    return jsonify(partido), 200

@partidos_bp.route("/<id>", methods=["DELETE"])
def delete_partido(id):
    try:
        id = int(id)
        validar_id(id)
    except ValueError as e:
            return jsonify({
            "errors": [
                {
                    "code": "400",
                    "message": "BAD REQUEST",
                    "level": "error",
                    "description": str(e)
                }
            ]
        }), 400

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM partido WHERE id = %s", (id,))
        conn.commit()
        rowcount = cursor.rowcount 
        cursor.close()
        conn.close()
    except Exception:
        return jsonify({  
        "errors": [
            {
                "code": "500",
                "message": "INTERNAL SERVER ERROR",
                "level": "error",
                "description": "Hubo un error al conectarse con la base de datos."
            }
    ]}), 500
    
    if rowcount == 0:
        return jsonify({
        "errors": [
            {
                "code": "404",
                "message": "NOT FOUND",
                "level": "error",
                "description": f"No se encontró el partido con id {id}."
            }
        ]
    }), 404
    return ("", 204)