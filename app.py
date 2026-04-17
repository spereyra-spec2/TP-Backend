from flask import Flask
from flask import Blueprints
from rutas.partidos import partidos_bp
app = Flask(__name__)

app.register_blueprint(partidos_bp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)