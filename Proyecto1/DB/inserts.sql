Use arqbased;
-- Insertar un nuevo administrador con contraseña en formato hash MD5
INSERT INTO Administrador (usuario, pwd)
VALUES ('admin1', MD5('admin1')),
('admin2', MD5('admin2')),
('admin3', MD5('admin3')),
('admin4', MD5('admin4')),
('admin5', MD5('admin5'));


-- Insertar usuarios
INSERT INTO Usuario (nombre, apellido, saldo, RFID, tipoUsuario, estado, id_administrador)
VALUES ('Juan', 'Perez', 150.75, '860FA022', 'estudiante', 'fuera', 1),
       ('Maria', 'Lopez', 300.50, 'D46BE373', 'administrativo', 'fuera', 1);

-- Insertar usuarios
INSERT INTO Usuario (nombre, apellido, saldo, RFID, tipoUsuario, estado, id_administrador)
VALUES ('Veronica', 'Sanchez', 200.00, '789FE373', 'estudiante', 'fuera', 1),
       ('Mauricio', 'Castillo', 100.55, 'C75EB373', 'estudiante', 'fuera', 1);
       
-- Insertar vehículos (uno a uno con Usuario)
INSERT INTO Vehiculo (placa, tipoVehiculo, estado, UID)
VALUES ('ABC-123', 'sedan', 'permitido', 1),
       ('XYZ-789', 'SUV', 'permitido', 2);

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
       
-- Insertar historial de ingreso y egreso
INSERT INTO Historial_Ingreso_Egreso (UID, id_vehiculo, id_estacionamiento, fechaEntrada, horaEntrada, costo)
VALUES (1, 1, 1, CURDATE(), CURTIME(), 3.00);
       