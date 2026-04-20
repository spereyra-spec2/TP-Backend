# TP-Backend
Segundo TP de la materia Introducción al Desarrollo de Software
# ProDe API Collection
## Estructura

```
TP-Backend/

├── app.py
├── config.py  #variables de configuración (para conectar con MySQL)
├── db.py
├── errors.py
├── init_db.py
├── init_db.sql
├── README.md│
├── .gitignore
├── requirements.txt  
├── routes/
    ├── partidos.py
    ├── predicciones.py    
    ├── ranking.py
    ├── reemplazar_datos_partido.py #(resultados)
    ├── usuarios.py
    └── validaciones_partidos.py
  

```

## Endpoints

### Partidos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/partidos` | Lista partidos con filtros opcionales |
| `GET` | `/partidos/:id` | Obtiene un partido por ID |
| `POST` | `/partidos` | Crea un nuevo partido |
| `PUT` | `/partidos/:id` | Reemplaza todos los campos de un partido |
| `PATCH` | `/partidos/:id` | Actualiza parcialmente un partido |
| `DELETE` | `/partidos/:id` | Elimina un partido |

#### Filtros disponibles en GET /partidos

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `fecha` | Fecha del partido | `2022-11-22` |
| `equipo` | Nombre del equipo | `ARGENTINA` |
| `fase` | Fase del torneo | `GRUPOS` |
| `_offset` | Paginación — inicio | `0` |
| `_limit` | Paginación — cantidad | `10` |

### Resultados

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `PUT` | `/partidos/:id/resultado` | Carga el resultado de un partido |

### Predicciones

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/partidos/:id/prediccion` | Registra una predicción para un partido |

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/usuarios` | Lista usuarios |
| `GET` | `/usuarios/:id` | Obtiene un usuario por ID |
| `POST` | `/usuarios` | Crea un nuevo usuario |
| `PUT` | `/usuarios/:id` | Reemplaza todos los campos de un usuario |
| `DELETE` | `/usuarios/:id` | Elimina un usuario |

### Ranking

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/ranking` | Obtiene el ranking de usuarios |

## Variables de contiguración

El entorno `config.py` incluye las siguientes variables configurables:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `host` | `localhost` | Host |
| `user` | `root` | Usuario predeterminado |
| `pasword` | `root` | Variable a cambiar |
| `data_base` | `prode_db` | Nombre base de datos |


## Uso

1. Clonar el repositorio
2. Navegar hasta la carpeta del proyecto
3. Crear un entorno virtual.
4. Abrir PostMan
5. Seleccionar el entorno en **config.py**
6. Ajustar las variables de configuración según sea necesario