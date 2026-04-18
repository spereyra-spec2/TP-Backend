
def validar_id(id):
    if id <= 0:
        raise ValueError("El id debe ser un número entero positivo.")
