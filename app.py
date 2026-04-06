from datetime import datetime
from flask import Flask, jsonify, request, Response
import db

HOST_APP: str = "localhost"
PUERTO_APP: int = 5000
URL_BASE: str = "prode_api"
app: Flask = Flask(__name__)
app.json.sort_keys = False

MAX_LIMIT: int = 50
FASES: list = ["grupos", "dieciseisavos", "octavos", "cuartos", "semifinales", "final"]

@app.route(f"/{URL_BASE}/")
def hello_world() -> str:
    return "ProDe API"

@app.route(f"/{URL_BASE}/partidos", methods=["GET"])
def partidos() -> Response:
    errores: list = []

    try:
        offset: int = int(request.args.get("_offset", 0))

        if offset < 0:
            errores.append({
                "code": 400,
                "message": "Parámetro '_offset' negativo",
                "level": "error",
                "description": "El valor del parámetro '_offset' debe ser mayor o igual a 0."
            })
    except ValueError:
        errores.append({
            "code": 400,
            "message": "Parámetro '_offset' no entero",
            "level": "error",
            "description": "El valor del parámetro '_offset' debe ser un número entero."
        })

    try:
        limit: int = int(request.args.get("_limit", 10))

        if limit < 1 or limit > MAX_LIMIT:
            errores.append({
                "code": 400,
                "message": "Parámetro '_limit' fuera de rango",
                "level": "error",
                "description": f"El valor del parámetro '_limit' debe situarse dentro del siguiente ranngo: 1–{MAX_LIMIT}."
            })
    except ValueError:
        errores.append({
            "code": 400,
            "message": "Parámetro '_limit' no entero",
            "level": "error",
            "description": "El valor del parámetro '_limit' debe ser un número entero."
        })

    equipo: str = request.args.get("equipo", None)
    if equipo is not None and equipo.strip() == "":
        errores.append({
            "code": 400,
            "message": "Parámetro 'equipo' vacío",
            "level": "error",
            "description": "El valor del parámetro 'equipo' no puede ser una cadena vacía."
        })

    fecha_str: str = request.args.get("fecha", None)
    fecha: datetime | None = None
    if fecha_str is not None:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            errores.append({
                "code": 400,
                "message": "Parámetro 'fecha' inválido",
                "level": "error",
                "description": "El valor del parámetro 'fecha' debe tener formato YYYY-MM-DD."
            })

    fase: str = request.args.get("fase", None)
    if fase is not None and fase.strip() == "":
        errores.append({
            "code": 400,
            "message": "Parámetro 'fase' vacío",
            "level": "error",
            "description": "El valor del parámetro 'fase' no puede ser una cadena vacía."
        })

    if fase is not None and fase not in FASES:
        errores.append({
            "code": 400,
            "message": "Parámetro 'fase' inválido",
            "level": "error",
            "description": f"El valor del parámetro 'fase' debe ser uno de los siguientes: {', '.join(FASES)}."
        })

    if errores:
        return jsonify({ "errors": errores }), 400

    return db.obtener_partidos(offset, limit, equipo, fecha, fase)

if __name__ == "__main__":
    app.run(host=HOST_APP, port=PUERTO_APP, debug=True)