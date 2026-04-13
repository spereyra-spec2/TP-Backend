import csv
import os
from datetime import datetime

def obtener_partido(id):
    partidos = obtener_partidos()
    for partido in partidos:
        if partido['id'] == id:
            return partido
        
    return None


def obtener_usuario(usuario_id): 
    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            return usuario

    return None