import csv
import os

ARCHIVO_CSV = 'usuarios.csv'
CAMPOS = ['id', 'nombre', 'email']


def asegurar_archivo(): # Si el archivo no existe, se crea uno.
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
            writer.writeheader()


def leer_usuarios(): #Lee y devuelve una lista de diccionarios con la id convertida en int(entero).
    asegurar_archivo()

    with open(ARCHIVO_CSV, 'r', newline='', encoding='utf-8') as archivo:
        reader = csv.DictReader(archivo)
        usuarios = []
        for fila in reader:
            fila['id'] = int(fila['id'])
            usuarios.append(fila)
        return usuarios


def guardar_usuarios(usuarios): # Borra el contenido del Archivo para remplazarlo por el parametro de la función.
    asegurar_archivo()

    with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
        writer.writeheader()
        writer.writerows(usuarios)

#Place Holder de Función en caso que mi equipo me pida hacer post en App.py (no estoy seguro)
#--------------------------------------------------------------------------------------------------------------------
#def crear_usuario(nombre, email): # Guarda un nuevo usuario a Archivo_cvs.
#    usuarios = leer_usuarios()
#    ids = []
#    for usuario in usuarios:
#        ids.append(usuario['id'])
#
#    siguiente_id = max(ids, default=0) + 1 # Devuelve el maximo de las ids. Si esta vacio, devuelve 0 como la id.
#
#    nuevo_usuario = {
#        'id': siguiente_id,
#        'nombre': nombre, # Parametro de función.
#        'email': email, # Parametro de función.
#    }
#
#    usuarios.append(nuevo_usuario) # Agrega el diccionario creado a la lista de diccionario de usuarios.
#    guardar_usuarios(usuarios) # Borra y remplaza el contenido del archivo por el parametro de función.
#    return nuevo_usuario
#---------------------------------------------------------------------------------------------------------------------


def obtener_usuario(usuario_id): # Lee y devuelve el usuario buscado por id (Parametro de función).
    usuarios = leer_usuarios()
    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            return usuario

    return None


def actualizar_usuario(usuario_id, nombre, email): # Si la Id del parametro coincide, remplaza los datos del usuario.
    usuarios = leer_usuarios()

    for usuario in usuarios:
        if usuario['id'] == usuario_id:
            usuario['nombre'] = nombre
            usuario['email'] = email
            guardar_usuarios(usuarios)
            return usuario

    return None


def eliminar_usuario(usuario_id): # Elimina al usuario buscado por parametro de función.
    usuarios = leer_usuarios()
    usuario = None

    for i in usuarios:
        if i['id'] == usuario_id:
            usuario = i
            usuarios.remove(i)
            break

    if not usuario:
        return None

    guardar_usuarios(usuarios)
    return usuario

