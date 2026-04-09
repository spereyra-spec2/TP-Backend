from datetime import datetime
from typing import Any

FASES: list[str] = ["grupos", "dieciseisavos", "octavos", "cuartos", "semis", "final"]
LIMIT_MAX: int = 50

def validar_equipo(equipo: str) -> dict | None:
    if equipo and equipo.strip() == "":
        return {
            "code": 400,
            "message": "Parámetro 'equipo' vacío",
            "level": "error",
            "description": "El valor del parámetro 'equipo' no puede ser una cadena vacía."
        }

def validar_fecha(fecha_str: str) -> dict | None:
    if fecha_str is not None:
        try:
            fecha: datetime = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            return {
                "code": 400,
                "message": "Parámetro 'fecha' inválido",
                "level": "error",
                "description": "El valor del parámetro 'fecha' debe tener formato YYYY-MM-DD y ser un día del año real."
            }

def validar_fase(fase: str) -> dict | None:
    if fase and fase.strip() == "":
        return {
            "code": 400,
            "message": "Parámetro 'fase' vacío",
            "level": "error",
            "description": "El valor del parámetro 'fase' no puede ser una cadena vacía."
        }

    if fase and fase.lower() not in FASES:
        return {
            "code": 400,
            "message": "Parámetro 'fase' inválido",
            "level": "error",
            "description": f"El valor del parámetro 'fase' debe ser uno de los siguientes: {", ".join(FASES)}."
        }

def validar_offset(offset: object) -> dict | None:
    try:
        offset_int: int = int(offset)

        if offset_int < 0:
            return {
                "code": 400,
                "message": "Parámetro '_offset' negativo",
                "level": "error",
                "description": "El valor del parámetro '_offset' debe ser mayor o igual a 0."
            }
    except ValueError:
        return {
            "code": 400,
            "message": "Parámetro '_offset' no entero",
            "level": "error",
            "description": "El valor del parámetro '_offset' debe ser un número entero."
        }

def validar_limit(limit: object) -> dict | None:
    try:
        limit_int: int = int(limit)

        if limit_int < 1 or limit_int > LIMIT_MAX:
            return {
                "code": 400,
                "message": "Parámetro '_limit' fuera de rango",
                "level": "error",
                "description": f"El valor del parámetro '_limit' debe situarse dentro del siguiente rango: 1–{LIMIT_MAX}."
            }
    except ValueError:
        return {
            "code": 400,
            "message": "Parámetro '_limit' no entero",
            "level": "error",
            "description": "El valor del parámetro '_limit' debe ser un número entero."
        }

def validaciones_partidos(equipo: str, fecha_str: str, fase: str, offset: object, limit: object) -> list:
    errores: list[dict[str, Any]] = []
    
    val_equipo: dict | None = validar_equipo(equipo)
    errores.append(val_equipo) if val_equipo else None

    val_fecha: datetime | dict | None = validar_fecha(fecha_str)
    errores.append(val_fecha) if val_fecha else None

    val_fase: dict | None = validar_fase(fase)
    errores.append(val_fase) if val_fase else None

    val_offset: dict | None = validar_offset(offset)
    errores.append(val_offset) if val_offset else None

    val_limit: dict | None = validar_limit(limit)
    errores.append(val_limit) if val_limit else None

    return errores