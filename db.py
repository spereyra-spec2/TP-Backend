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

        for fila in lector:
            if ((equipo is None or equipo.lower() in fila["equipo_local"].lower() or equipo.lower() in fila["equipo_visitante"].lower()) and
               (fecha is None or datetime.strptime(fila["fecha"], "%Y-%m-%d") == fecha) and
               (fase is None or fila["fase"].lower() == fase.lower())):
                
                # Cuenta todas las coincidencias, pero solo agrega la fila al resultado si está dentro del rango _offset y _limit
                if coincidencias >= offset and coincidencias < offset + limit:
                    partidos.append(fila)
                
                # Cuenta el total de coincidencias para paginación
                coincidencias += 1
        
        if len(partidos) == 0:
            return jsonify({
                "errors": [
                    {
                        "code": 404,
                        "message": "No encontrado",
                        "level": "info",
                        "description": "No se encontraron partidos que coincidieran con los parámetros de búsqueda especificados."
                    }
                ]
            }), 404
        
        return jsonify({
            "partidos": partidos,
            "_links": {
                "_first": {
                    "href": url_for("partidos", _offset=0, _limit=limit, _external=True),
                },
                "_prev": {
                    "href": url_for(
                                "partidos",
                                _offset = offset - limit if offset - limit >= 0 else (coincidencias - 1) // limit * limit if coincidencias > 0 else 0,
                                _limit=limit,
                                _external=True
                            )
                },
                "_next": {
                    "href": url_for(
                                "partidos",
                                _offset = limit + offset if limit + offset < coincidencias else 0,
                                _limit=limit,
                                _external=True
                            ),
                },
                "_last": {
                    "href": url_for(
                                "partidos",
                                _offset = (coincidencias - 1) // limit * limit if coincidencias > 0 else 0,
                                _limit=limit,
                                _external=True
                            )
                }
            }
        }), 200