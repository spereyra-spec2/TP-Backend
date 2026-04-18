not_found = {
            "error": [
                {
                    "code": 404,
                    "message": "No encontrado",
                    "level": "info",
                    "description": "No se encontraron usuarios con el id indicado."
                }
            ]
        }
def server_error(error):
    error500 = {"error": [
                    {
                        "code": 500,
                        "message": "Error interno en el servidor",
                        "level": "error",
                        "description": str(error)
                    }
                ]
            }
    return error500

bad_request = {
            "error": [
                {
                    "code": 400,
                    "message": "Petición inválida",
                    "level": "info",
                    "description": "Faltan campos obligatorios o el formato JSON es incorrecto. Verifica los datos ingresados en el body."
                }
            ]
        }

# Cree esta parte para ahorrarme el escribir tanto.