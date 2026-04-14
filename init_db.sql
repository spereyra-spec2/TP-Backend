CREATE DATABASE IF NOT EXISTS prode;
USE prode;

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

