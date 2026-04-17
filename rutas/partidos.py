from flask import Flask, Blueprint, jsonify, request
from db import get_connection

partidos_bp = Blueprint('partidos',__name__, url_prefix='/partidos')
app = Flask(__name__)

@partidos_bp.route('/partidos', methods=['POST'])
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

        if not equipo_local or not equipo_visitante or not fecha or not fase:
            return jsonify({'error': 'Datos inválidos'}), 400

        cursor.execute(
            """SELECT * FROM partidos_2
            WHERE equipo_local = %s AND equipo_visitante = %s
            AND fecha = %s AND fase = %s""", (equipo_local, equipo_visitante, fecha, fase))

        existe_partido = cursor.fetchone()

        if existe_partido:
            return jsonify({'error': 'El partido ya existe'}), 409

        cursor.execute(
         """INSERT INTO partidos_2 (equipo_local, equipo_visitante, fecha, fase) 
               VALUES (%s, %s, %s, %s)""", (equipo_local, equipo_visitante, fecha, fase))


        conexion.commit()
        cursor.close()
        conexion.close()


        return jsonify({'mensaje': 'Partido creado correctamente'}), 201

    except Exception as e:
        print(e)
        return jsonify({'error': 'Error del servidor'}), 500



@app.errorhandler(404)  #BORRAR DE SER NECESARIO
def not_found(error):
    return jsonify ({'error': 'Recurso no encontrado',
                     'sugerencia': 'Use el endpoint válido /partidos'}), 404