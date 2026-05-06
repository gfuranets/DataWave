CREATE DATABASE IF NOT EXISTS DataWave;
USE DataWave;

CREATE TABLE user (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    UNIQUE (username)
);

CREATE TABLE ship (
    ship_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id_refer INT,
    name VARCHAR(50) NOT NULL,
    token VARCHAR(255),
    CONSTRAINT fk_user FOREIGN KEY (user_id_refer) REFERENCES user(user_id),
    UNIQUE (name),
    UNIQUE (token)
);

CREATE TABLE data (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    ship_id_refer INT,
    data VARCHAR(255),
    timestamp DATETIME,
    CONSTRAINT fk_ship FOREIGN KEY (ship_id_refer) REFERENCES ship(ship_id)
);
