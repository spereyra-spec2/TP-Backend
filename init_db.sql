CREATE DATABASE IF NOT EXISTS IDS;

use IDS;

CREATE TABLE if not exists usuarios(
    id_usuario INT NOT NULL AUTO_INCREMENT primary key ,
    nombre varchar(15) NOT NULL ,
    email varchar(40) NOT NULL
);

INSERT INTO usuarios(nombre, email)
VALUES
 ("Santino","spp@gmail.com"),
 ("Gustavo","gsc@gmaiil.com"),
 ("Sabrina","scr@gmail.com"),
 ("Pepe","pep@gmail.com");

CREATE TABLE if not exists partidos(
    id_partido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    equipo_local varchar(15) not null,
    equipo_visitante varchar(15) not null,
    fecha timestamp default current_timestamp,
    fase varchar(15) not null ,
    local int(2) not null,
    visitante int(2) not null
);

insert into partidos(equipo_local, equipo_visitante, fecha, fase,local, visitante)
VALUES
 ("Argentina","Francia","2026-06-20 18:40:00","grupos",3,0),
 ("Belgica","Portugal","2026-06-21 02:20:00","grupos",1,1),
 ("Brasil","Colombia","2026-06-22 05:00:00","grupos",0,1),
 ("Nigeria","España","2026-06-23 15:00:00","grupos",1,2),
 ("Alemania","Inglaterra","2026-06-24 21:00:00","grupos",2,1)
;

create table if not exists prediccion(
  id_usuario int(3) not null ,
  id_partido int(3) not null ,
  local int(2) not null,
  visitante int(2) not null
);

INSERT INTO prediccion(id_usuario, id_partido, local, visitante)
VALUES
(1,1,1,2),
(2,1,3,3),
(3,1,2,0),
(4,1,4,0),
(5,1,3,0),
(6,2,0,0),
(7,4,0,0),
(8,4,2,2),
(9,4,0,0),
(10,2,1,1),
(1,2,2,0),
(2,2,0,0),
(1,3,1,0),
(2,3,5,0),
(1,4,2,0),
(2,4,1,1),
(1,5,6,0),
(2,5,3,3);




