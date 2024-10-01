UPDATE Estacionamiento
SET espaciosDisponibles = espaciosDisponibles - 1
WHERE id = 1;

UPDATE Estacionamiento
SET espaciosDisponibles = espaciosDisponibles + 1
WHERE id = 1;

SELECT espaciosDisponibles 
FROM Estacionamiento
WHERE id = 1;

UPDATE Usuario
SET saldo = saldo - 3.00
WHERE UID = 1;

UPDATE Usuario
SET estado = 'dentro'
WHERE UID = 1;

UPDATE Historial_Ingreso_Egreso
SET horaSalida = CURTIME()
WHERE id = 1;

UPDATE Usuario
SET estado = 'fuera'
WHERE UID = 1;

UPDATE Usuario
SET estado = 'dentro'
WHERE UID = 2;

UPDATE vehiculo
SET estado = 'denegado'
WHERE id = 1;


UPDATE Externo
SET estado = 'dentro'
WHERE id = 1;

UPDATE Historial_Ingreso_Egreso
SET horaSalida = CURTIME()
WHERE id = 3;