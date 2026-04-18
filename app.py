from flask import Flask


from flask_cors import CORS
from routes.partidos import partidos_bp
from routes.usuarios import usuarios_bp
from routes.predicciones import predicciones_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(partidos_bp, url_prefix="/partidos")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(predicciones_bp)


if __name__ == "__main__":
    app.run(port=5000, debug=True)

