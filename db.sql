CREATE DATABASE IF NOT EXISTS mundial_db;
USE mundial_db;

CREATE TABLE partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipo_local VARCHAR(100) NOT NULL,
    equipo_visitante VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    fase ENUM('grupos', 'dieciseisavos', 'octavos', 'cuartos', 'semis', 'final') NOT NULL,
    goles_local INT DEFAULT NULL,
    goles_visitante INT DEFAULT NULL
);

INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase) 
VALUES 
('Argentina', 'Francia', '2026-06-10', 'grupos'), 
('Mexico', 'Italia', '2026-12-09', 'octavos'), 
('Chile', 'Argelia', '2026-05-06', 'semis');