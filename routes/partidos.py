from flask import Flask, Blueprint, jsonify, request, url_for, Response
from db import get_connection, ejecutar_consulta, reemplazar_partido
from routes.validaciones_partidos import validaciones_partidos
from routes.validaciones_partidos import validar_id
from typing import Any
import mysql.connector


partidos_bp = Blueprint("partidos",__name__)

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

    equipo_filter = f'(`equipo_local`="{equipo}" OR `equipo_visitante`="{equipo}")' if equipo else ""
    fecha_filter  = f'(DATE(`fecha`)="{fecha_str}")' if fecha_str else ""
    fase_filter   = f'(`fase`="{fase.lower()}")' if fase else ""

    condicion: str = f"WHERE {equipo_filter}{fecha_filter}{fase_filter}"
    
    nueva_condicion: str = ""
    for i in range(len(condicion)):
        nueva_condicion += condicion[i]
        if i != len(condicion) - 1 and condicion[i] == ')' and condicion[i + 1] == '(':
            nueva_condicion += " AND "

    condicion_final = nueva_condicion if nueva_condicion.strip() != "WHERE" else ""
    consulta: str = f"SELECT * FROM `prode`.`partido` {condicion_final} LIMIT {limit_int} OFFSET {offset_int}"

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
        condicion_final = nueva_condicion if nueva_condicion.strip() != "WHERE" else ""
        total_coincidencias: int = ejecutar_consulta(f"SELECT COUNT(*) as total FROM `prode`.`partido` {condicion_final}")[0]["total"]
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
                "href": url_for("partidos.obtener_partidos", _offset = 0, _limit = limit_int, _external = True),
            },
            "_prev": {
                "href": url_for(
                            "partidos.obtener_partidos",
                            _offset = offset_int - limit_int if offset_int - limit_int >= 0
                            else (total_coincidencias - 1) // limit_int * limit_int if total_coincidencias > 0 else 0,
                            _limit = limit_int,
                            _external = True
                        )
            },
            "_next": {
                "href": url_for(
                            "partidos.obtener_partidos",
                            _offset = limit_int + offset_int if limit_int + offset_int < total_coincidencias else 0,
                            _limit = limit_int,
                            _external = True
                        ),
            },
            "_last": {
                "href": url_for(
                            "partidos.obtener_partidos",
                            _offset = (total_coincidencias - 1) // limit_int * limit_int if total_coincidencias > 0 else 0,
                            _limit = limit_int,
                            _external = True
                        )
            }
        }
    }), 200

@partidos_bp.route('', methods=['POST'])
def agregar_datos_partidos():
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        data = request.json

        if not data:
         return jsonify({'errors': [
             {
                "code":"400",
                "message":"BAD_REQUEST",
                "level":"error",
                "description":"El cuerpo de la solocitud está vació o mal formado"
             }
         ]
    }), 400

        equipo_local = data.get('equipo_local')
        equipo_visitante = data.get('equipo_visitante')
        fecha = data.get('fecha')
        fase = data.get('fase')
        resultado = data.get('resultado')

        if not equipo_local or not equipo_visitante or not fecha or not fase:
            return jsonify({'error': [
                {
                    "code":"400",
                    "message":"BAD_REQUEST",
                    "level":"error",
                    "description":"Faltan campos obligatorios"
                }
            ]
        }), 400

        cursor.execute(
            """SELECT * FROM partido
            WHERE equipo_local = %s AND equipo_visitante = %s
            AND fecha = %s AND fase = %s""", (equipo_local, equipo_visitante, fecha, fase))

        existe_partido = cursor.fetchone()

        if existe_partido:
            return jsonify({'errors': [
                {
                "code":"409",
                "message":"CONFLICT",
                "level":"error",
                "description":"Ya existe un partido con los mismos datos"
                }
            ]
        }), 409

        cursor.execute(
         """INSERT INTO partido (equipo_local, equipo_visitante, fecha, fase, resultado) 
               VALUES (%s, %s, %s, %s, %s)""", (equipo_local, equipo_visitante, fecha, fase, resultado))


        conexion.commit()
        cursor.close()
        conexion.close()


        return jsonify({'mensaje': 'Partido creado correctamente'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': [
            {
            "code":"500",
            "message":"INTERNAL_SERVER_ERROR",
            "level":"error",
            "description":"Ocurrió un error inesperado"
            }
        ]
    }), 500

"""

@app.errorhandler(404)  
def not_found(error):
    return jsonify ({'error': 'Recurso no encontrado',
                     'sugerencia': 'Use el endpoint válido /partidos'}), 404
"""

@partidos_bp.route("/<int:id>", methods=["PATCH"])
def mod_partido(id):
    data=request.get_json()

    if not data:
        return jsonify({"errors": [
            {
            "code":"400",
            "message":"BAD_REQUEST",
            "level":"error",
            "description":"El request body no puede estar vacío"
            }
        ]
    }), 400
        
    columnas_modificables = {"equipo_local", "equipo_visitante", "fecha", "fase", "resultado"}

    valores_a_mod = {}

    #crear una diccionario con las columnas a modificar que se encuentren en el body y en la lista y los valores del body
    for col, value in data.items():
        if col in columnas_modificables:
            valores_a_mod[col] = value
    if not valores_a_mod:
        return jsonify({"error": "no se envio ningun valor modificable"}), 400

    tmp = []
    for valor in valores_a_mod:
        tmp.append(f"{valor} = %s")
    values_format = ", ".join(tmp)
    #values format es "valor1 = %s, valor2 = %s" y asi

    values = list(valores_a_mod.values())
    values.append(id)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id FROM partido WHERE ID = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"errors": [
                {
                    "code":"404",
                    "message":"NOT_FOUND",
                    "level":"error",
                    "description":"partido a modificar no encontrado"
                }]}), 404

        cursor.execute(f"UPDATE partido SET {values_format} WHERE ID = %s", values)

        conn.commit()
        return ("", 200)

    except Exception as ex:
        return jsonify({"errors": [
            {
                "code": "500",
                "message": "INTERNAL SERVER ERROR",
                "level": "error",
                "description": str(ex)
            }
    ]}), 500

    finally:
        cursor.close()
        conn.close()

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

@partidos_bp.route('/<int:id>', methods=['PUT'])
def reemplazo_partido(id):
    try:
        data = request.get_json()
        datos_requeridos = ['equipo_local','equipo_visitante', 'fecha', 'fase']
        for dato in datos_requeridos:
            if dato not in data: 
                return jsonify({
                    "errors":[{
                        'status': 400,
                        'error': 'bad request',
                        'message': f'el campo {dato} no puede estar vacío'

                    }]
                }), 400

        call = reemplazar_partido(id,data)
        if call:
            return '', 204
        
    except Exception as e:
        return jsonify({
           'errors':[{
           'status': 500,
            'error': 'internal problem',
            'message': 'ha ocurrido un problema interno'
              }]
        }), 500
     
@partidos_bp.route('/<int:id>/resultados', methods=['PUT'])
def remplazar_datos_partido(id):
    datos = request.get_json()

    if not datos or 'local' not in datos or 'visitante' not in datos:
        return jsonify({
            "code": 400,
            "message": "Petición inválida",
            "level": "error",
            "description": "Faltan campos obligatorios"
        }), 400

    if not isinstance(datos['local'], int) or not isinstance(datos['visitante'], int):
        return jsonify({
            "code": 400,
            "message": "Petición inválida",
            "level": "error",
            "description": "Los datos deben ser números"
        }), 400

    conexion = get_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("SELECT id, resultado FROM partido WHERE id = %s", (id,))
        partido = cursor.fetchone()

        if not partido:
            return jsonify({
                "code": 404,
                "message": "No encontrado",
                "level": "error",
                "description": f"El partido {id} no existe"
            }), 404

        resultado_id = partido['resultado']


        if resultado_id is None:
            insert_query = "INSERT INTO resultado (local, visitante) VALUES (%s, %s)"
            cursor.execute(insert_query, (datos['local'], datos['visitante']))

            nuevo_resultado_id = cursor.lastrowid


            update_partido = "UPDATE partido SET resultado = %s WHERE id = %s"
            cursor.execute(update_partido, (nuevo_resultado_id, id))

        else:
            update_query = "UPDATE resultado SET local = %s, visitante = %s WHERE id = %s"
            cursor.execute(update_query, (datos['local'], datos['visitante'], resultado_id))

        conexion.commit()
        return '', 204

    except Exception as error:
        return jsonify({
            "code": 500,
            "message": str(error),
            "level": "error",
            "description": "Error interno al acceder a la base de datos"
        }), 500

    finally:
        cursor.close()
        conexion.close()