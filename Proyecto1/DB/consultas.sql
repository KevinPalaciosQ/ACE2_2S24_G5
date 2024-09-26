SELECT * FROM administrador;
SELECT * FROM usuario;
SELECT * FROM vehiculo;
SELECT * FROM estacionamiento;
SELECT * FROM clima;
SELECT * FROM historial_ingreso_egreso;

SELECT h.id, u.nombre, u.apellido, v.placa, h.fechaEntrada, h.horaEntrada, h.horaSalida, h.costo
FROM Historial_Ingreso_Egreso h
JOIN Usuario u ON h.UID = u.UID
JOIN Vehiculo v ON h.id_vehiculo = v.id
WHERE u.UID = 1;

