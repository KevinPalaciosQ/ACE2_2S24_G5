Use arqbased;
-- Insertar un nuevo administrador con contraseña en formato hash MD5
INSERT INTO Administrador (usuario, pwd)
VALUES ('admin1', MD5('admin1'));

-- Insertar usuarios
INSERT INTO Usuario (nombre, apellido, saldo, RFID, tipoUsuario, estado, id_administrador)
VALUES ('Juan', 'Perez', 200.00, 'D46BE373', 'estudiante', 'fuera', 1),
       ('Maria', 'Lopez', 300.50, '860FA022', 'administrativo', 'fuera', 1);

-- Insertar Externos
INSERT INTO Externo (nombre, apellido, estado, id_administrador)
VALUES ('Monica', 'Sanchez', 'fuera', 1),
       ('Flavio', 'Villa', 'fuera', 1);
       
-- Insertar vehículos (uno a uno con Usuario)
INSERT INTO Vehiculo (placa, tipoVehiculo, estado, UID)
VALUES ('ABC-123', 'sedan', 'permitido', 1),
       ('XYZ-789', 'SUV', 'permitido', 2);

-- Insertar vehículos (uno a uno con Externo)
INSERT INTO Vehiculo (placa, tipoVehiculo, estado, id_externo)
VALUES ('ÑLKJ-753', 'toyota', 'permitido', 1),
       ('QWE-654', 'honda', 'permitido', 2);
       
-- Insertar estacionamiento
INSERT INTO Estacionamiento (capacidad, espaciosDisponibles)
VALUES (6, 6);


-- Insertar historial de ingreso y egreso de usuario
INSERT INTO Historial_Ingreso_Egreso (UID, id_vehiculo, fechaEntrada, horaEntrada, costo, esExterno)
VALUES (1, 1, '2024-09-25', '08:00:00', 3.00, false),
       (2, 2, '2024-09-25', '09:30:00', 0.00, false);
       
-- Insertar historial de ingreso y egreso de usuario Externo
INSERT INTO Historial_Ingreso_Egreso (id_externo, id_vehiculo, fechaEntrada, horaEntrada, costo, esExterno)
VALUES (1, 3, CURDATE(), CURTIME(), 3.00, true);

-- Insertar historial de ingreso y egreso de usuario Externo
INSERT INTO Historial_Ingreso_Egreso (id_externo, id_vehiculo, fechaEntrada, horaEntrada, costo, esExterno)
VALUES (2, 4, CURDATE(), CURTIME(), 3.00, true);
       