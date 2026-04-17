CREATE DATABASE IF NOT EXISTS mundial;
USE mundial;

CREATE TABLE IF NOT EXISTS partidos (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(100) NOT NULL,
    equipo_visitante VARCHAR(100) NOT NULL,
    goles_local INT DEFAULT 0,
    goles_visitante INT DEFAULT 0,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO mundial.partidos (equipo_local, equipo_visitante, goles_local, goles_visitante)
VALUES ('Argentina', 'Francia', 0, 0);
INSERT INTO mundial.partidos (equipo_local, equipo_visitante, goles_local, goles_visitante)
VALUES ('Uruguay', 'Brasil', 0, 0);

INSERT INTO mundial.partidos (equipo_local, equipo_visitante, goles_local, goles_visitante)
VALUES ('Alemania', 'Japon', 0, 0);
INSERT INTO mundial.partidos (equipo_local, equipo_visitante, goles_local, goles_visitante)
VALUES ('España', 'Belgica', 0, 0);
SELECT * FROM mundial.partidos;
TRUNCATE TABLE mundial.partidos;