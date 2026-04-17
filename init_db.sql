CREATE DATABASE IF NOT EXISTS partidos;
USE partidos;

CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pais VARCHAR(50) NOT NULL,
    estadio VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    FOREIGN KEY (equipo_local) REFERENCES equipos(id) ON DELETE CASCADE,
    FOREIGN KEY (equipo_visitante) REFERENCES equipos(id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    fase VARCHAR(25) NOT NULL
);




