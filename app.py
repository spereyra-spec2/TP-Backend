from flask import Flask, request, jsonify
import db

app = Flask(__name__)


# GET y DELETE partidos por id

@app.route('/partidos/<int:id>', methods=['GET'])
def obtener_partido(id):
    partido = db.obtener_partido(id)
    if partido:
        return jsonify(partido), 200
    return jsonify({'error': 'Partido no encontrado'}), 404

@app.route('/partidos/<int:id>', methods=['DELETE'])
def eliminar_partido(id):
    partido = db.eliminar_partido(id)
    if partido:
        return jsonify({'message': 'Partido eliminado'}), 200
    return jsonify({'error': 'Partido no encontrado'}), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)