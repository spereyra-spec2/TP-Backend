CREATE DATABASE IF NOT EXISTS basedatos;
USE basedatos;

CREATE TABLE IF not EXISTS partidos (
	ID INT PRIMARY KEY AUTO_INCREMENT,
	local VARCHAR(50),
	visitante VARCHAR(50),
	estadio VARCHAR(50),
	ciudad VARCHAR(50),
	fecha VARCHAR(50),
	fase VARCHAR(50)
);
CREATE TABLE IF not EXISTS usuarios (
	UID INT PRIMARY KEY AUTO_INCREMENT,
	name VARCHAR(50),
	age INT
);



INSERT INTO partidos
	(local, visitante, estadio, ciudad, fecha, fase)
VALUES	
	("River", "Boca", "mi casa", "pehuajo", "mañana", "128avos"),
	("union", "defensores", "estadio curaru", "curaru", "ayer", "final");
