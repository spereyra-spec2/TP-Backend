from flask import Blueprint, jsonify, request, url_for
from db import get_connection

usuarios_bp = Blueprint("usuarios", __name__)

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

    

