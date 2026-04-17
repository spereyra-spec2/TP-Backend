from flask import Blueprint, jsonify, request
from db import get_user, put_user, delete_user
from errors import not_found, server_error, bad_request

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    try:
        usuario = get_user(id)

        if usuario is None:
            return jsonify(not_found), 404

        return jsonify({"mensaje": "Usuario encontrado.", "datos": usuario}), 200

    except Exception as e:
        return jsonify(server_error(e)), 500


@usuarios_bp.route('/<int:id>', methods=['PUT'])
def reemplazar_usuario(id):
    data = request.get_json(silent=True)
    if not data:
        return jsonify(bad_request), 400

    if "nombre" not in data or "email" not in data:
        return jsonify(bad_request), 400

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
