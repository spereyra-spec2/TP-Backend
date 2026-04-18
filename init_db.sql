CREATE DATABASE IF NOT EXISTS IDS;

use IDS;

CREATE TABLE if not exists partidos(
    id_partido INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    equipo_local varchar(15) not null,
    equipo_visitante varchar(15) not null,
    fecha timestamp default current_timestamp,
    fase varchar(15) not null ,
    local int(2) not null,
    visitante int(2) not null
);

create table if not exists prediccion(
  id_usuario int(3) not null ,
  id_partido int(3) not null ,
  local int(2) not null,
  visitante int(2) not null
);





