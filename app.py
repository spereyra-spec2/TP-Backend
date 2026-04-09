from config import PUERTO_APP, URL_BASE
from flask import Flask
from routes.partidos import partidos_bp

app: Flask = Flask(__name__)
app.json.sort_keys = False

app.register_blueprint(partidos_bp, url_prefix = f"/{URL_BASE}/partidos")

@app.route(f"/{URL_BASE}/")
def hello_world() -> str:
    return "ProDe API"

if __name__ == "__main__":
    app.run(host="localhost", port=PUERTO_APP, debug=True)