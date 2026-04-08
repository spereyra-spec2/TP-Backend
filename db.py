import csv
import os

ARCHIVO_CSV = 'usuarios.csv'
CAMPOS = ['id', 'nombre', 'email']


def _asegurar_archivo():
    os.makedirs(os.path.dirname(ARCHIVO_CSV), exist_ok=True)

    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
            writer.writeheader()


def leer_usuarios():
    _asegurar_archivo()

    with open(ARCHIVO_CSV, 'r', newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        usuarios = []
        for fila in reader:
            fila['id'] = int(fila['id'])
            usuarios.append(fila)
        return usuarios


def _guardar_usuarios(usuarios):
    _asegurar_archivo()

    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(usuarios)


def crear_usuario(nombre, email):
    usuarios = leer_usuarios()
    siguiente_id = max((usuario['id'] for usuario in usuarios), default=0) + 1

    nuevo_usuario = {
        'id': siguiente_id,
        'nombre': nombre,
        'email': email,
    }

    usuarios.append(nuevo_usuario)
    _guardar_usuarios(usuarios)
    return nuevo_usuario


def obtener_usuario(usuario_id):
    usuarios = leer_usuarios()
    return next((usuario for usuario in usuarios if usuario['id'] == usuario_id), None)


def actualizar_usuario(usuario_id, nombre, email):
    usuarios = leer_usuarios()

    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            usuario['nombre'] = nombre
            usuario['email'] = email
            _guardar_usuarios(usuarios)
            return usuario

    return None


def eliminar_usuario(usuario_id):
    usuarios = leer_usuarios()
    usuario = next((item for item in usuarios if item['id'] == usuario_id), None)

    if not usuario:
        return None

    usuarios_filtrados = [item for item in usuarios if item['id'] != usuario_id]
    _guardar_usuarios(usuarios_filtrados)
    return usuario
