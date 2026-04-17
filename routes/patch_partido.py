from flask import Blueprint, jsonify, request
from db import get_connection

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route("/<int:id>", methods=["PATCH"])
def mod_partido(id):
    data=request.get_json()

    if not data:
        return jsonify({"error": "el request body no puede estar vacio"}), 400
        
    columnas_modificables = {"ciudad", "estadio", "fase", "fecha", "local", "visitante"}

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
        cursor.execute("SELECT id FROM partidos WHERE ID = %s", (id,))
        if not cursor.fetchone():
            return jsonify({"error": "partido a modificar no encontrado"}), 404

        cursor.execute(f"UPDATE partidos SET {values_format} WHERE ID = %s", values)

        conn.commit()
        return jsonify({"message": "item actualizado correctamente"}), 200

    except Exception as ex:
        return jsonify({"error": str(ex)}),500

    cursor.close()
    conn.close()
