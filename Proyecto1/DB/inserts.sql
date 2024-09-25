-- Insertar un nuevo administrador con contraseña en formato hash MD5
INSERT INTO Administrador (usuario, contraseña)
VALUES ('admin1', MD5('admin1')),
('admin2', MD5('admin2')),
('admin3', MD5('admin3')),
('admin4', MD5('admin4')),
('admin5', MD5('admin5'));