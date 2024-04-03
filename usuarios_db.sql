CREATE DATABASE IF NOT EXISTS Challenge_MELI_db;
USE Challenge_MELI_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fec_alta DATETIME,
    user_name VARCHAR(255),
    codigo_zip VARCHAR(10),
    credit_card_num VARCHAR(20),
    credit_card_ccv VARCHAR(3),
    cuenta_numero VARCHAR(20),
    direccion VARCHAR(255),
    geo_latitud VARCHAR(20),
    geo_longitud VARCHAR(20),
    color_favorito VARCHAR(50),
    foto_dni VARCHAR(255),
    ip VARCHAR(50),
    auto_marca VARCHAR(100),
    auto_modelo VARCHAR(20),
    auto_tipo VARCHAR(50),
    auto_color VARCHAR(50),
    cantidad_compras INT,
    avatar VARCHAR(255),
    fec_birthday DATETIME
);

CREATE USER IF NOT EXISTS 'meli'@'localhost' IDENTIFIED BY 'meli123';
GRANT ALL PRIVILEGES ON Challenge_MELI_db.* TO 'meli'@'%' IDENTIFIED BY 'meli123';

