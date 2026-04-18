CREATE DATABASE IF NOT EXISTS prode_db;
USE prode_db;

CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pais VARCHAR(50) NOT NULL,
    estadio VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
--    FOREIGN KEY (equipo_local) REFERENCES equipos(id) ON DELETE CASCADE,
--    FOREIGN KEY (equipo_visitante) REFERENCES equipos(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    fase VARCHAR(25) NOT NULL
);

CREATE TABLE IF not EXISTS usuarios (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(60) NOT NULL,
	email VARCHAR(90) NOT NULL UNIQUE
);
CREATE TABLE IF not EXISTS predicciones (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    partido_id INT NOT NULL,
    goles_local_pred INT NOT NULL,
    goles_visitante_pred INT NOT NULL,
    fecha_prediccion DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
    UNIQUE KEY unique_prediccion (usuario_id, partido_id)
);


