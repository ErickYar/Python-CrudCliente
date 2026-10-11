create database empresa_db;
use empresa_db;
create table cliente(
id int auto_increment primary key,
nombre varchar(100) not null,
correo varchar(100) not null unique,
telefono varchar(20)
);