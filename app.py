from flask import Flask
from init_db import init_db
from routes.partidos import partidos_bp

app = Flask(__name__)
init_db()

app.register_blueprint(partidos_bp, url_prefix="/partidos")


if __name__ == '__main__':
    app.run(port=5000, debug=True)