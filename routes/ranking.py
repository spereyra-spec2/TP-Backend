from flask import Flask, Blueprint, jsonify, request
from db import obtener_ranking
from mysql.connector import Error


ranking_bp = Blueprint("ranking",__name__)

@ranking_bp.route('', methods=['GET'])
def get_ranking():
    limit = request.args.get('_limit', default=10, type=int)
    offset = request.args.get('_offset', default=0, type=int)

    try:
        ranking = obtener_ranking(limit,offset)
        if ranking is None:
             return jsonify({"errors": [{"code": "500", "message": "Error al obtener el ranking"}]}), 500

        if len(ranking) == 0:
            return "", 204
        
        return jsonify(ranking),200

    except Error as e:
        error_payload = {
            "errors": [{
                "code": "400",
                "message": "Hubo un error inesperado en la base de datos",
                "level": "error",
                "description": str(e)
            }]
        }
        return jsonify(error_payload),400

    except Exception as e:
        error_payload = {
            "errors": [{
                "code": "500",
                "message": "Hubo un error inesperado en el código",
                "level": "error",
                "description": str(e)
            }]
        }
        return jsonify(error_payload),500
