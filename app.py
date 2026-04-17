from flask import Flask, request, jsonify
from db import reemplazar_partido

app= Flask(__name__)

@app.route('/partidos/<int:id>', methods=['PUT'])
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

if __name__ == '__main__':
    app.run(port=5000, debug=True)