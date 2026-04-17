from flask import Flask, jsonify, request
from Routes.remplazar_datos_partidos import partidos_bp

app = Flask(__name__)

app.register_blueprint(partidos_bp)


if __name__ == '__main__':
    app.run(debug=True)