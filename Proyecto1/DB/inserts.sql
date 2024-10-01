Use arqbased;
-- Insertar un nuevo administrador con contraseña en formato hash MD5
INSERT INTO Administrador (usuario, pwd)
VALUES ('admin1', MD5('admin1'));


-- Insertar usuarios
INSERT INTO Usuario (nombre, apellido, saldo, RFID, tipoUsuario, estado, id_administrador)
VALUES ('Juan', 'Perez', 200.00, '860FA022', 'estudiante', 'fuera', 1),
       ('Maria', 'Lopez', 300.50, 'D46BE373', 'administrativo', 'fuera', 1);

-- Insertar usuarios
INSERT INTO Usuario (nombre, apellido, saldo, RFID, tipoUsuario, estado, id_administrador)
VALUES ('Veronica', 'Sanchez', 200.00, '789FE373', 'estudiante', 'fuera', 1),
       ('Mauricio', 'Castillo', 100.55, 'C75EB373', 'estudiante', 'fuera', 1);

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

-- Insertar registros de clima
INSERT INTO Clima (temperatura, humedad, id_administrador)
VALUES (40, 70, 1),
(32, 50, 1);
-- VALUES (25.5, 60, 1), (26.3, 58, 1);

-- Insertar historial de ingreso y egreso
INSERT INTO Historial_Ingreso_Egreso (UID, id_vehiculo, id_estacionamiento, fechaEntrada, horaEntrada, costo)
VALUES (1, 1, 1, '2024-09-25', '08:00:00', 3.00),
       (2, 2, 1, '2024-09-25', '09:30:00', 0.00);
       
-- Insertar historial de ingreso y egreso de usuario
INSERT INTO Historial_Ingreso_Egreso (id_externo, id_vehiculo, id_estacionamiento, fechaEntrada, horaEntrada, costo, esExterno)
VALUES (1, 3, 1, CURDATE(), CURTIME(), 3.00, true);
-- (2, 2, 1, CURDATE(), CURTIME(), 3.00, false);
       