from flask import Blueprint, jsonify, request, url_for
from db import get_user, put_user, delete_user, get_connection
from errors import not_found, server_error, bad_request
import mysql.connector
from mysql.connector import IntegrityError

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("", methods=["POST"])
def add_usuario():
    try:    
        data = request.get_json(silent= True)
        if data is None:
            return jsonify({"errors":[
                {"code": 400,
                 "message": "Faltan campos obligatorios, nombre y email",
                 "level": "error"
                 }]}), 400
        nombre = data.get("nombre")
        email = data.get("email")
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
                   INSERT INTO usuarios (nombre, email)
                   VALUES (%s, %s)
                   """, (nombre, email))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Usuario agregado correctamente"}), 201
    except IntegrityError:
        return jsonify({"errors":[
                {"code": 409,
                 "message": "El correo electronico ya se encuentra registrado",
                 "level": "advertencia"
                 }]}), 409
    except Exception as e:
        return jsonify({"errors":[
                {"code": 500,
                 "message": "Error interno del servidor",
                 "level": "critico"
                 }]}), 500


@usuarios_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    if id <= 0:
        return jsonify(bad_request("El ID debe ser un número positivo.")), 400
    try:
        usuario = get_user(id)

        if usuario is None:
            return jsonify(not_found), 404

        return jsonify({"mensaje": "Usuario encontrado.", "datos": usuario}), 200

    except Exception as e:
        return jsonify(server_error(e)), 500


@usuarios_bp.route('/<int:id>', methods=['PUT'])
def reemplazar_usuario(id):
    if id <= 0:
        return jsonify(bad_request("El ID debe ser un número positivo.")), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify(bad_request("El body debe ser JSON")), 400

    if "nombre" not in data or "email" not in data:
        return jsonify(bad_request("El body debe tener los campos 'nombre' y 'email.'")), 400

    try:
        datos_acts = put_user(data,id)

        if datos_acts is False:
            return jsonify(not_found), 404

        usuario = get_user(id)
        return jsonify({"mensaje" : "Usuario actualizado con existo." , "datos actualizados" : usuario}) , 200

    except Exception as e:
        return jsonify(server_error(e)), 500

@usuarios_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    if id <= 0:
        return jsonify(bad_request("El ID debe ser un número positivo.")), 400
        
    try:
        usuario = get_user(id)
        if usuario is None:
            return jsonify(not_found), 404

        delete = delete_user(id)

        if delete is False:
            return jsonify(not_found), 404

        return jsonify({"mensaje" : "Usuario eliminado con exito." , "datos eliminados" : usuario}) , 200

    except Exception as e:
        return jsonify(server_error(e)), 500

# SI NO FUNCIONA AÑADIR GETCONNECTIO Y COSAS A db.py
LIMIT_DEFAULT = 10
@usuarios_bp.route("", methods=["GET"])
def get_usuarios():

    str_limit = request.args.get("_limit")
    try:
        if not str_limit:
            limit = LIMIT_DEFAULT
        else:
            limit = int(str_limit)
    except Exepcion:
        return jsonify({"error": "_limit debe ser de tipo int"}), 400

    str_offset = request.args.get("_offset")
    try:
        if not str_offset:
            offset = 0
        else:
            offset = int(str_offset)
    except Exeption:
        return jsonify({"error": "offset debe ser de tipo int"}), 400

    

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(f"SELECT * FROM usuarios LIMIT {limit} OFFSET {offset}")
        usuarios = cursor.fetchall()
        cursor.execute("SELECT COUNT(*) as total FROM usuarios")
        total = cursor.fetchone()["total"]
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500
    finally:
        cursor.close()
        conn.close()

    if not usuarios:
        return jsonify({"error": "tabla usuarios vacia"}), 204

    last_offset = max(0, (total // limit) * limit)
    if last_offset >= total:
        last_offset = max(0, last_offset - limit)

    return jsonify({
        "usuarios": usuarios,
        "links":{
            "_first": {
                "href": url_for("usuarios.get_usuarios", _offset = 0, _limit = limit, external = True),
            },
            "_prev":{
                "href": url_for("usuarios.get_usuarios", _offset = offset - limit if offset - limit >= 0 else 0, _limit = limit, external = True),
            },
            "_next":{
                "href": url_for("usuarios.get_usuarios", _offset = offset + limit, _limit = limit, external = True),
            },
            "_last":{
                "href": url_for("usuarios.get_usuarios", _offset = limit - offset if limit - offset >= 0 else 0, _limit = limit, external = True),
            }
        }
}), 200


