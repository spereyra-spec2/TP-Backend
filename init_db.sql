CREATE DATABASE IF NOT EXISTS prode_db;
USE prode_db;

CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pais VARCHAR(50) NOT NULL,
    estadio VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS resultado (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    local INT NOT NULL,
    visitante INT NOT NULL
);


CREATE TABLE IF NOT EXISTS partido (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(50) NOT NULL,
    equipo_visitante VARCHAR(50) NOT NULL,
    fecha DATE NOT NULL,
    fase ENUM('grupos', 'dieciseisavos', 'octavos', 'cuartos', 'semis', 'final') NOT NULL,
    resultado INT,
    FOREIGN KEY (resultado) REFERENCES resultado(id)
);

CREATE TABLE IF not EXISTS usuarios (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nombre VARCHAR(60) NOT NULL,
	email VARCHAR(90) NOT NULL UNIQUE
);

create table if not exists prediccion(
  id_usuario int NOT NULL ,
  id_partido int NOT NULL ,
  local integer NOT NULL,
  visitante integer NOT NULL
);


