from flask import Flask, jsonify, request

import db

app = Flask(__name__)

@app.route('/usuarios/<int:id>', methods=['PUT'])
def reemplazar_usuario(id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({'error': 'El body debe ser JSON'}), 400

    nombre = data.get('nombre')
    email = data.get('email')

    if not nombre or not email:
        return jsonify({'error': 'Los campos nombre y email son obligatorios'}), 400

    usuario = db.actualizar_usuario(usuario_id=id, nombre=nombre, email=email)
    if usuario:
        return jsonify(usuario), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404


@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = db.obtener_usuario(id)
    if usuario:
        return jsonify(usuario), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario_eliminado = db.eliminar_usuario(id)
    if usuario_eliminado:
        return jsonify({'message': 'Usuario eliminado'}), 200
    return jsonify({'error': 'Usuario no encontrado'}), 404


if __name__ == '__main__':
    app.run(port=5000, debug=True)
