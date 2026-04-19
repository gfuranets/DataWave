CREATE DATABASE IF NOT EXISTS DataWave;
USE DataWave;

CREATE TABLE user (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(30),
	email VARCHAR(40)
);

CREATE TABLE ship (
    ship_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id_refer INT,
    code VARCHAR(10),
    name VARCHAR(50),
    CONSTRAINT fk_user FOREIGN KEY (user_id_refer) REFERENCES user(user_id)
);

CREATE TABLE data (
    data_id INT AUTO_INCREMENT PRIMARY KEY,
    ship_id_refer INT,
    data VARCHAR(40),
    timestamp DATETIME,
    CONSTRAINT fk_ship FOREIGN KEY (ship_id_refer) REFERENCES ship(ship_id)
);
