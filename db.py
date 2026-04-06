import csv, os
from datetime import datetime
from flask import jsonify, Response, url_for

ARCHIVO_CSV: str = "partidos.csv"
CAMPOS: list = ["id", "equipo_local", "equipo_visitante", "fecha", "fase", "resultado"]

def inicializar_archivo() -> None:
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()

def obtener_partidos(offset: int, limit: int, equipo: str | None, fecha: datetime | None, fase: str | None) -> Response:
    inicializar_archivo()

    with open(ARCHIVO_CSV, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        partidos: list = []
        coincidencias: int = 0

        for fila in enumerate(lector):
            if ((equipo is None or equipo.lower() in fila[1]["equipo_local"].lower() or equipo.lower() in fila[1]["equipo_visitante"].lower()) and
               (fecha is None or datetime.strptime(fila[1]["fecha"], "%Y-%m-%d") == fecha) and
               (fase is None or fila[1]["fase"].lower() == fase.lower())):
                coincidencias += 1

                if coincidencias >= offset and coincidencias < offset + limit:
                    partidos.append(fila[1])
        
        return jsonify({
            "partidos": partidos,
            "_links": {
                "_first": url_for("partidos", _offset=0, _limit=limit, _external=True),
                "_prev": url_for(
                    "partidos",
                    _offset = offset - limit if offset - limit >= 0 else (coincidencias - 1) // limit * limit if coincidencias > 0 else 0,
                    _limit=limit,
                    _external=True
                ),
                "_next": url_for(
                    "partidos",
                    _offset = limit + offset if limit + offset < coincidencias else 0,
                    _limit=limit,
                    _external=True
                ),
                "_last": url_for(
                    "partidos",
                    _offset = (coincidencias - 1) // limit * limit if coincidencias > 0 else 0,
                    _limit=limit,
                    _external=True
                )
            }
        }), 200