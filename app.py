from flask import Flask
from init_db import init_db
from routes.partidos.partidos import partidos_bp

app = Flask(__name__)

try:
    init_db()
except Exception as e:
    print(f"Error al inicializar la base de datos: {e}")
    exit(1)

app.register_blueprint(partidos_bp, url_prefix="/partidos")


if __name__ == '__main__':
    app.run(port=5000, debug=True)