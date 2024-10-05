Use arqbased;
SELECT * FROM administrador;
SELECT * FROM usuario;
SELECT * FROM externo;
SELECT * FROM vehiculo;
SELECT * FROM estacionamiento;
SELECT * FROM clima;
SELECT * FROM historial_ingreso_egreso;

SELECT espaciosDisponibles from Estacionamiento;

SELECT id from vehiculo where UID = 2;
SELECT id from vehiculo where id_externo = 2;

SELECT espaciosDisponibles
FROM Estacionamiento
LIMIT 1;