-- Eliminar base de datos si ya existe
DROP DATABASE IF EXISTS arqbased;

-- Crear la base de datos
CREATE DATABASE arqbased;

-- Usar la base de datos
USE arqbased;

-- Eliminación de tablas anteriores
DROP TABLE IF EXISTS Administrador, Usuario, Vehiculo, Estacionamiento, Historial_Ingreso_Egreso, Externo;

-- Creación de la tabla Administrador
CREATE TABLE Administrador (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    pwd VARCHAR(32) NOT NULL  -- Tamaño 32 para almacenar hash MD5
);

-- Creación de la tabla Usuario
CREATE TABLE Usuario (
    UID INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    saldo FLOAT NOT NULL,
    RFID VARCHAR(100) NOT NULL UNIQUE,
    tipoUsuario ENUM('estudiante', 'administrativo') NOT NULL,
    estado ENUM('dentro', 'fuera') NOT NULL,
    id_administrador INT,
    FOREIGN KEY (id_administrador) REFERENCES Administrador(id) ON DELETE CASCADE
);

-- Creación de la tabla Externo
CREATE TABLE Externo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    estado ENUM('dentro', 'fuera') NOT NULL,
    id_administrador INT,
    FOREIGN KEY (id_administrador) REFERENCES Administrador(id) ON DELETE CASCADE
);

-- Creación de la tabla Vehículo
CREATE TABLE Vehiculo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(20) NOT NULL,
    tipoVehiculo VARCHAR(50) NOT NULL,
    estado ENUM('permitido', 'denegado') NOT NULL,
    UID INT UNIQUE,  -- Relación uno a uno con Usuario
    id_externo INT UNIQUE,  -- Relación uno a uno con Externo (permitimos solo un dueño)
    FOREIGN KEY (UID) REFERENCES Usuario(UID) ON DELETE CASCADE,
    FOREIGN KEY (id_externo) REFERENCES Externo(id) ON DELETE CASCADE
);

-- Creación de la tabla Estacionamiento
-- CREATE TABLE Estacionamiento (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     capacidad INT NOT NULL,
--     espaciosDisponibles INT NOT NULL
-- );

-- Creación de la tabla Historial_Ingreso_Egreso
CREATE TABLE Historial_Ingreso_Egreso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    UID INT,  -- Llave foránea de Usuario
    id_externo INT,  -- Llave foránea de Externo
    id_vehiculo INT,  -- Llave foránea de Vehículo
    -- id_estacionamiento INT,  -- Llave foránea de Estacionamiento
    fechaEntrada DATE NOT NULL,
    horaEntrada TIME NOT NULL,
    horaSalida TIME,
    costo FLOAT,
    esExterno BOOLEAN NOT NULL,  -- Nuevo atributo para marcar si es un usuario externo
    FOREIGN KEY (UID) REFERENCES Usuario(UID) ON DELETE CASCADE,
    FOREIGN KEY (id_externo) REFERENCES Externo(id) ON DELETE CASCADE,
    FOREIGN KEY (id_vehiculo) REFERENCES Vehiculo(id) ON DELETE CASCADE
    -- FOREIGN KEY (id_estacionamiento) REFERENCES Estacionamiento(id) ON DELETE CASCADE
);
