from app import URL_BASE
from db import ejecutar_consulta
from flask import Blueprint, jsonify, request, Response, url_for
from typing import Any
from routes.validaciones_partidos import validaciones_partidos
import mysql.connector

partidos_bp: Blueprint = Blueprint(f"{URL_BASE}/partidos", __name__)
DEFAULT_OFFSET: int = 0
DEFAULT_LIMIT: int = 10

@partidos_bp.route("", methods = ["GET"])
def obtener_partidos() -> Response:
    equipo: str = request.args.get("equipo")
    fecha_str: str = request.args.get("fecha")
    fase: str = request.args.get("fase")
    offset: object = request.args.get("_offset", DEFAULT_OFFSET)
    limit: object = request.args.get("_limit", DEFAULT_LIMIT)

    errores: list[dict[str, Any]] = validaciones_partidos(equipo, fecha_str, fase, offset, limit)

    if errores:
        return jsonify({"errors": errores}), 400
    
    offset_int: int = int(offset)
    limit_int: int = int(limit)

    condicion: str = f"WHERE {f'(`equipo_local`="{equipo}" OR `equipo_visitante`="{equipo}")' if equipo else ""}" \
                     f"{f'(DATE(`fecha`)="{fecha_str}")' if fecha_str else ""}" \
                     f"{f'(`fase`="{fase.lower()}")' if fase else ""}"
    
    nueva_condicion: str = ""
    for i in range(len(condicion)):
        nueva_condicion += condicion[i]
        if i != len(condicion) - 1 and condicion[i] == ')' and condicion[i + 1] == '(':
            nueva_condicion += " AND "

    consulta: str = f"SELECT * FROM `prode`.`partido` {nueva_condicion if nueva_condicion.strip() != "WHERE" else ""} LIMIT {limit_int} OFFSET {offset_int}"

    try:
        partidos: list[dict[str, Any]] = ejecutar_consulta(consulta)
    except mysql.connector.Error as error:
        return jsonify({
            "errors": [
                {
                    "code": 500,
                    "message": "Error interno del servidor",
                    "level": "error",
                    "description": str(error)
                }
            ]
        }), 500

    if not partidos:
        return jsonify({
            "errors": [
                {
                    "code": 404,
                    "message": "No encontrado",
                    "level": "info",
                    "description": "No se encontraron partidos que coincidieran con los parámetros de búsqueda especificados."
                }
            ]
        }), 404
    
    try:
        total_coincidencias: int = ejecutar_consulta(f"SELECT COUNT(*) as total FROM `prode`.`partido` {nueva_condicion if nueva_condicion.strip() != "WHERE" else ""}")[0]["total"]
    except mysql.connector.Error as error:
        return jsonify({
            "errors": [
                {
                    "code": 500,
                    "message": "Error interno del servidor",
                    "level": "error",
                    "description": str(error)
                }
            ]
        }), 500

    return jsonify({
        "partidos": partidos,
        "_links": {
            "_first": {
                "href": url_for(f"{URL_BASE}/partidos.obtener_partidos", _offset = 0, _limit = limit_int, _external = True),
            },
            "_prev": {
                "href": url_for(
                            f"{URL_BASE}/partidos.obtener_partidos",
                            _offset = offset_int - limit_int if offset_int - limit_int >= 0
                            else (total_coincidencias - 1) // limit_int * limit_int if total_coincidencias > 0 else 0,
                            _limit = limit_int,
                            _external = True
                        )
            },
            "_next": {
                "href": url_for(
                            f"{URL_BASE}/partidos.obtener_partidos",
                            _offset = limit_int + offset_int if limit_int + offset_int < total_coincidencias else 0,
                            _limit = limit_int,
                            _external = True
                        ),
            },
            "_last": {
                "href": url_for(
                            f"{URL_BASE}/partidos.obtener_partidos",
                            _offset = (total_coincidencias - 1) // limit_int * limit_int if total_coincidencias > 0 else 0,
                            _limit = limit_int,
                            _external = True
                        )
            }
        }
    }), 200