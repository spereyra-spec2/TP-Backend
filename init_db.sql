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


INSERT INTO resultado (local, visitante) VALUES
(2, 0), 
(1, 1);


INSERT INTO partido (equipo_local, equipo_visitante, fecha, fase, resultado) VALUES
-- Grupo A
('Mexico',        'Sudafrica',        '2026-06-11', 'grupos', 1),
('Corea del Sur', 'Republica Checa',  '2026-06-12', 'grupos', 2),
('Mexico',        'Corea del Sur',    '2026-06-16', 'grupos', NULL),
('Sudafrica',     'Republica Checa',  '2026-06-16', 'grupos', NULL);
