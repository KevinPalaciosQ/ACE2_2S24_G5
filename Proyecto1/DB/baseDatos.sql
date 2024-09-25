-- show databases;
DROP DATABASE IF EXISTS arquiDB;
CREATE DATABASE arquiDB;

USE arquiDB;
DROP TABLE IF EXISTS Administrador;

CREATE TABLE Administrador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    contraseña VARCHAR(32) NOT NULL  -- Tamaño 32 para almacenar hash MD5
);
-- Crear la tabla Clima y la relación uno a uno con Administrador
CREATE TABLE Clima (
    id INT PRIMARY KEY,
    temperatura DECIMAL(5,2),
    humedad DECIMAL(5,2),
    FOREIGN KEY (id) REFERENCES Administrador(id)
);

-- Crear la tabla Estudiante
CREATE TABLE Estudiante (
    UID INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    saldo INT NOT NULL,
    RFID VARCHAR(255) NOT NULL UNIQUE,
    Estado ENUM('permitido', 'denegado')
);

-- Crear la tabla Administrativo
CREATE TABLE Administrativo (
    UID INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    saldo INT NOT NULL,
    RFID VARCHAR(255) NOT NULL UNIQUE,
    Estado ENUM('permitido', 'denegado')
);

-- Crear la tabla Vehículo
CREATE TABLE Vehiculo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cantidad INT,
    estudiante_UID INT UNIQUE,
    administrativo_UID INT UNIQUE,
    FOREIGN KEY (estudiante_UID) REFERENCES Estudiante(UID),
    FOREIGN KEY (administrativo_UID) REFERENCES Administrativo(UID)
);

-- Crear la tabla Estacionamiento
CREATE TABLE Estacionamiento (
    id INT PRIMARY KEY,
    espaciosDisponibles INT NOT NULL,
    vehiculo_id INT UNIQUE,
    FOREIGN KEY (vehiculo_id) REFERENCES Vehiculo(id)
);

-- Crear la tabla Historial_Ingreso_Egreso
CREATE TABLE Historial_Ingreso_Egreso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    UID_Estudiante INT,
    UID_Administrativo INT,
    fecha DATE,
    horaEntrada TIME,
    horaSalida TIME,
    -- Foreign Key para el UID de Estudiante
    FOREIGN KEY (UID_Estudiante) REFERENCES Estudiante(UID),
    -- Foreign Key para el UID de Administrativo
    FOREIGN KEY (UID_Administrativo) REFERENCES Administrativo(UID)
);


-- Relación uno a muchos entre Administrador y Estudiante
ALTER TABLE Estudiante ADD administrador_id INT,
    ADD FOREIGN KEY (administrador_id) REFERENCES Administrador(id);

-- Relación uno a muchos entre Administrador y Administrativo
ALTER TABLE Administrativo ADD administrador_id INT,
    ADD FOREIGN KEY (administrador_id) REFERENCES Administrador(id);
    
