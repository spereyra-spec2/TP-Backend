from flask import Flask
from flask_cors import CORS
from routes.partidos import partidos_bp
from routes.usuarios import usuarios_bp
from routes.predicciones import predicciones_bp
from routes.ranking import ranking_bp
from init_db import init_db

app = Flask(__name__)
CORS(app)
app.config["JSON_SORT_KEYS"] = False
app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(predicciones_bp)
app.register_blueprint(ranking_bp, url_prefix="/ranking")

try:
    init_db()
except Exception as e:
    print(f"Error al inicializar la base de datos: {e}")
    exit(1)


if __name__ == "__main__":
    app.run(port=5000, debug=True)

