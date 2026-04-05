import csv
import os
from datetime import datetime

ARCHIVO_CSV = 'partidos.csv'
CAMPOS = ['id', 'equipo_local', 'equipo_visitante', 'fecha', 'fase', 'resultado']

def inicializar_archivo():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
            writer =csv.DictWriter(file, fieldnames=CAMPOS)
            writer.writeheader()


def obtener_partidos():
    inicializar_archivo()
    partidos = []
    with open(ARCHIVO_CSV, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for fila in reader:
            fila['id'] = int(fila['id'])
            fila['fecha'] = datetime.strptime(fila['fecha'], '%Y-%m-%d').strftime('%Y-%m-%d')
            partidos.append(fila)

    return partidos

def guardar_partidos(partidos):
    with open(ARCHIVO_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=CAMPOS)
        writer.writeheader()
        for partido in partidos:
            writer.writerow(partido)

def obtener_partido(id):
    partidos = obtener_partidos()
    for partido in partidos:
        if partido['id'] == id:
            return partido
        
    return None

def eliminar_partido(id):
    partidos = obtener_partidos()
    partidos_filtrados = [p for p in partidos if p['id'] != id]
    if len(partidos) != len(partidos_filtrados):
        guardar_partidos(partidos_filtrados)
        return True
    
    return False