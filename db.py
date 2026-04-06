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
    total: int = 0

    for i, fila in enumerate(lector):
      if ((i >= offset and i < offset + limit) and
         (equipo is None or equipo.lower() in fila["equipo_local"].lower() or equipo.lower() in fila["equipo_visitante"].lower()) and
         (fecha is None or datetime.strptime(fila["fecha"], "%Y-%m-%d") == fecha) and
         (fase is None or fila["fase"].lower() == fase.lower())):
        partidos.append(fila)
      total += 1
    
    return jsonify({
      "partidos": partidos,
      "_links": {
        "_first": url_for("partidos", _limit=limit, _offset=0, _external=True),
        "_prev": url_for(
          "partidos",
          _limit=limit,
          _offset = offset - limit if offset - limit >= 0 else (total - 1) // limit * limit if total > 0 else 0,
          _external=True),
        "_next": url_for(
          "partidos",
          _limit=limit,
          _offset = limit + offset if limit + offset < total else 0,
          _external=True
        ),
        "_last": url_for(
          "partidos",
          _limit=limit,
          _offset = (total - 1) // limit * limit,
          _external=True
        )
      }
    }), 200