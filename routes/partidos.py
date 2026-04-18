from flask import Flask, Blueprint, jsonify, request
from db import get_connection

partidos_bp = Blueprint("partidos",__name__)
#app = Flask(__name__)


#partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route('', methods=['POST'])
def agregar_datos_partidos():
    try:
        conexion = get_connection()
        cursor = conexion.cursor(dictionary=True)
        data = request.json

        if not data:
         return jsonify({'error': 'Datos incorrecto o incompletos'}), 400

        equipo_local = data.get('equipo_local')
        equipo_visitante = data.get('equipo_visitante')
        fecha = data.get('fecha')
        fase = data.get('fase')
        local = data.get('local')
        visitante = data.get('visitante')

        if not equipo_local or not equipo_visitante or not fecha or not fase:
            return jsonify({'error': 'Datos inválidos'}), 400

        cursor.execute(
            """SELECT * FROM partidos
            WHERE equipo_local = %s AND equipo_visitante = %s
            AND fecha = %s AND fase = %s""", (equipo_local, equipo_visitante, fecha, fase))

        existe_partido = cursor.fetchone()

        if existe_partido:
            return jsonify({'error': 'El partido ya existe'}), 409

        cursor.execute(
         """INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase, local, visitante) 
               VALUES (%s, %s, %s, %s, %s, %s)""", (equipo_local, equipo_visitante, fecha, fase, local, visitante))


        conexion.commit()
        cursor.close()
        conexion.close()


        return jsonify({'mensaje': 'Partido creado correctamente'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': 'Error del servidor'}), 500

"""

@app.errorhandler(404)  #BORRAR DE SER NECESARIO
def not_found(error):
    return jsonify ({'error': 'Recurso no encontrado',
                     'sugerencia': 'Use el endpoint válido /partidos'}), 404
"""

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
