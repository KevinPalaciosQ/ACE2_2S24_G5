import mysql.connector
from mysql.connector import Error
import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa CORS
import hashlib
app = Flask(__name__)

CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',  # Cambia si tu servidor no está en localhost
        port=3306,         # Cambia si tu servidor usa otro puerto
        user='root',       # Cambia según tu usuario de MySQL
        password='dedicadoArqui2',  # Cambia por tu contraseña de MySQL
        database='arqbased'  # Cambia por tu base de datos
    )


'''
ACÁ VA EL CÓDIGO PARA INGRESO AL PARQUEO ******************************************************************************
'''

# ----------------------------------------------------------------------------------- INGRESO DE USUARIO ESTUDIANTE O ADMINISTRATIVO
@app.route('/administrador/entradaUsuario', methods=['POST'])
def logica_entradaUsuario():
    try:
        # Obtener el RFID del request
        rfid = request.json.get('rfid')
        
        if not rfid:
            return jsonify({
                "status": 400,
                "msg": "RFID no proporcionado."
            }), 400

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # 1.1 Comparar el RFID con el RFID almacenado en la base de datos
        query_usuario = """
            SELECT UID, nombre, apellido, saldo, Estado, tipoUsuario
            FROM Usuario
            WHERE RFID = %s;
        """
        cursor.execute(query_usuario, (rfid,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({
                "status": 401,
                "msg": "Usuario no encontrado."
            }), 401
        
        uid, nombre, apellido, saldo, estado, tipo_usuario = usuario

        # 1.2 Verificar si hay espacio disponible en el estacionamiento
        query_estacionamiento = """
            SELECT espaciosDisponibles
            FROM Estacionamiento
            LIMIT 1;
        """
        cursor.execute(query_estacionamiento)
        espacios_disponibles = cursor.fetchone()[0]

        if espacios_disponibles == 0:
            return jsonify({
                "status": 403,
                "msg": "Parqueo lleno."
            }), 403

        # Lógica de costo del parqueo
        costo_estudiante = 3.00
        costo_administrativo = 0.00
        es_externo = False

        # 1.2.1 Si el estado del usuario es "fuera" y el saldo es mayor o igual a Q3.00
        if estado == 'fuera' and (saldo >= costo_estudiante or tipo_usuario == 'administrativo'):
            # Si es estudiante
            if tipo_usuario == 'estudiante':
                if saldo >= costo_estudiante:
                    # Restar el costo del parqueo del saldo del estudiante
                    nuevo_saldo = saldo - costo_estudiante
                    query_update_saldo = """
                        UPDATE Usuario SET saldo = %s WHERE UID = %s;
                    """
                    cursor.execute(query_update_saldo, (nuevo_saldo, uid))

                    # Actualizar el historial de entrada para el estudiante
                    query_historial = """
                        INSERT INTO Historial_Ingreso_Egreso (UID, fecha, horaEntrada, costo, esExterno)
                        VALUES (%s, CURDATE(), CURTIME(), %s, %s);
                    """
                    cursor.execute(query_historial, (uid, costo_estudiante, es_externo))

                else:
                    return jsonify({
                        "status": 402,
                        "msg": "Saldo insuficiente para el estudiante."
                    }), 402

            # Si es administrativo
            elif tipo_usuario == 'administrativo':
                # Registrar la entrada del administrativo en el historial
                query_historial = """
                    INSERT INTO Historial_Ingreso_Egreso (UID, fecha, horaEntrada, costo, esExterno)
                    VALUES (%s, CURDATE(), CURTIME(), %s, %s);
                """
                cursor.execute(query_historial, (uid, costo_administrativo, es_externo))

            # Cambiar el estado del usuario a "dentro"
            query_update_estado = """
                UPDATE Usuario SET estado = 'dentro' WHERE UID = %s;
            """
            cursor.execute(query_update_estado, (uid,))

            # Reducir el espacio disponible en el estacionamiento
            query_update_espacios = """
                UPDATE Estacionamiento SET espaciosDisponibles = espaciosDisponibles - 1;
            """
            cursor.execute(query_update_espacios)

            # Confirmar cambios
            db_connection.commit()

            # Mostrar mensaje de bienvenida
            return jsonify({
                "status": 200,
                "msg": f"Bienvenido {nombre} {apellido}. Acceso permitido.",
                "estadoVehiculo": "permitido"
            }), 200

        # 1.2.2 Si el estado del usuario es "dentro" o el saldo es menor a Q3.00
        elif estado == 'dentro' or (tipo_usuario == 'estudiante' and saldo < costo_estudiante):
            return jsonify({
                "status": 403,
                "msg": "Acceso denegado. Estado 'dentro' o saldo insuficiente.",
                "estadoVehiculo": "denegado"
            }), 403

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al procesar la entrada: {err}"
        }), 400

    finally:
        cursor.close()
        db_connection.close()


# ----------------------------------------------------------------------------------- INGRESO DE USUARIOS EXTERNOS
@app.route('/administrador/logicaEntradaExterno', methods=['POST'])
def logica_entrada_externo():
    try:
        # Obtener los datos del request
        ingreso = request.json.get('ingreso')  # 1 indica que es un ingreso
        id_externo = request.json.get('id_externo')  # ID del usuario externo

        if ingreso != 1 or not id_externo:
            return jsonify({
                "status": 400,
                "msg": "Datos insuficientes. 'ingreso' o 'id_externo' no proporcionado correctamente."
            }), 400

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Verificar el estado del usuario externo en la tabla Externo
        query_externo = """
            SELECT estado
            FROM Externo
            WHERE id = %s
        """
        cursor.execute(query_externo, (id_externo,))
        externo = cursor.fetchone()

        if not externo:
            return jsonify({
                "status": 404,
                "msg": "Externo no encontrado."
            }), 404

        estado_externo = externo[0]

        # Verificar si el estado del Externo es "fuera"
        if estado_externo == "dentro":
            return jsonify({
                "status": 400,
                "msg": "El usuario externo ya está dentro del parqueo."
            }), 400

        # Verificar los espacios disponibles en el estacionamiento
        query_estacionamiento = """
            SELECT capacidad, espaciosDisponibles
            FROM Estacionamiento
            LIMIT 1
        """
        cursor.execute(query_estacionamiento)
        estacionamiento = cursor.fetchone()

        if not estacionamiento:
            return jsonify({
                "status": 400,
                "msg": "No se encontró información del estacionamiento."
            }), 400

        capacidad_total = estacionamiento[0]
        espacios_disponibles = estacionamiento[1]

        if espacios_disponibles == 0:
            return jsonify({
                "status": 400,
                "msg": "El parqueo está lleno."
            }), 400

        # Actualizar el estado del usuario externo a "dentro"
        query_update_externo = """
            UPDATE Externo
            SET estado = 'dentro'
            WHERE id = %s
        """
        cursor.execute(query_update_externo, (id_externo,))

        # Registrar la entrada del externo en el historial
        query_insert_historial = """
            INSERT INTO Historial_Ingreso_Egreso (id_externo, fechaEntrada, horaEntrada, costo, esExterno)
            VALUES (%s, CURDATE(), CURTIME(), 3.00, TRUE)
        """
        cursor.execute(query_insert_historial, (id_externo,))

        # Reducir el número de espacios disponibles en el estacionamiento
        query_update_estacionamiento = """
            UPDATE Estacionamiento
            SET espaciosDisponibles = espaciosDisponibles - 1
            WHERE id = (SELECT id FROM Estacionamiento LIMIT 1)
        """
        cursor.execute(query_update_estacionamiento)

        # Confirmar cambios
        db_connection.commit()

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver la respuesta con éxito
        return jsonify({
            "status": 200,
            "msg": "Ingreso permitido para el usuario externo. ¡Bienvenido!",
        }), 200

    except mysql.connector.Error as err:
        # Manejo de errores de la base de datos
        return jsonify({
            "status": 500,
            "msg": f"Error al procesar la entrada del usuario externo: {err}"
        }), 500

    except Exception as e:
        # Manejo de otros errores
        return jsonify({
            "status": 500,
            "msg": f"Error inesperado: {str(e)}"
        }), 500


'''
ACÁ VA EL CÓDIGO PARA EGRESO DEL PARQUEO ******************************************************************************
'''
# ----------------------------------------------------------------------------------- SALIDA DE USUARIO ESTUDIANTE O ADMINISTRATIVO
@app.route('/administrador/salidaUsuario', methods=['POST'])
def logica_salida_Usuario():
    try:
        # Obtener el RFID desde el cuerpo de la solicitud
        rfid = request.json.get('rfid')

        if not rfid:
            return jsonify({
                "status": 400,
                "msg": "RFID no proporcionado."
            }), 400

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Verificar si el RFID existe en la base de datos
        query_usuario = """
            SELECT UID, estado 
            FROM Usuario
            WHERE RFID = %s
        """
        cursor.execute(query_usuario, (rfid,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({
                "status": 404,
                "msg": "Usuario no encontrado."
            }), 404

        uid = usuario[0]
        estado_usuario = usuario[1]

        # Verificar el estado del usuario: Si está "dentro" o "fuera"
        if estado_usuario == "fuera":
            return jsonify({
                "status": 400,
                "msg": "El usuario ya está fuera del parqueo."
            }), 400

        # Si el estado es "dentro", permitir la salida
        # Actualizar el estado del vehículo a "permitido"
        query_update_vehiculo = """
            UPDATE Vehiculo
            SET estado = 'permitido'
            WHERE UID = %s
        """
        cursor.execute(query_update_vehiculo, (uid,))

        # Cambiar el estado del usuario a "fuera"
        query_update_usuario = """
            UPDATE Usuario
            SET estado = 'fuera'
            WHERE UID = %s
        """
        cursor.execute(query_update_usuario, (uid,))

        # Actualizar el historial de ingreso/egreso con la hora de salida
        query_update_historial = """
            UPDATE Historial_Ingreso_Egreso
            SET horaSalida = CURTIME()
            WHERE UID = %s AND horaSalida IS NULL
        """
        cursor.execute(query_update_historial, (uid,))

        # Aumentar el número de espacios disponibles en el estacionamiento
        query_update_estacionamiento = """
            UPDATE Estacionamiento
            SET espaciosDisponibles = espaciosDisponibles + 1
            WHERE id = (SELECT id FROM Estacionamiento LIMIT 1)
        """
        cursor.execute(query_update_estacionamiento)

        # Confirmar cambios
        db_connection.commit()

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Mostrar mensaje de éxito
        return jsonify({
            "status": 200,
            "msg": "Salida permitida. ¡Vuelva pronto!",
        }), 200

    except mysql.connector.Error as err:
        # Manejo de errores de la base de datos
        return jsonify({
            "status": 500,
            "msg": f"Error al procesar la salida: {err}"
        }), 500

    except Exception as e:
        # Manejo de otros errores
        return jsonify({
            "status": 500,
            "msg": f"Error inesperado: {str(e)}"
        }), 500

# ----------------------------------------------------------------------------------- SALIDA DE USUARIOS EXTERNOS

@app.route('/administrador/pagoSalidaExterno', methods=['POST'])
def pago_salida_externo():
    try:
        # Obtener el pago desde el cuerpo de la solicitud
        pago = request.json.get('pago')
        id_externo = request.json.get('id_externo')

        if not pago or not id_externo:
            return jsonify({
                "status": 400,
                "msg": "El pago o ID de externo no se ha proporcionado."
            }), 400

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Verificar si el usuario externo está "dentro" del parqueo
        query_externo = """
            SELECT estado 
            FROM Externo
            WHERE id = %s
        """
        cursor.execute(query_externo, (id_externo,))
        externo = cursor.fetchone()

        if not externo:
            return jsonify({
                "status": 404,
                "msg": "Usuario externo no encontrado."
            }), 404

        estado_externo = externo[0]

        # Verificar si el estado del externo es "dentro"
        if estado_externo == 'fuera':
            return jsonify({
                "status": 400,
                "msg": "El usuario externo ya está fuera del parqueo. Salida denegada."
            }), 400

        # Verificar si el pago es correcto y coincide con el historial de ingreso
        query_historial = """
            SELECT costo 
            FROM Historial_Ingreso_Egreso
            WHERE id_externo = %s AND horaSalida IS NULL
        """
        cursor.execute(query_historial, (id_externo,))
        historial = cursor.fetchone()

        if not historial:
            return jsonify({
                "status": 400,
                "msg": "No se encontró registro de ingreso para el usuario externo."
            }), 400

        costo_historial = historial[0]

        # Comparar el pago realizado con el costo del historial
        if pago != costo_historial:
            return jsonify({
                "status": 400,
                "msg": "El pago realizado no coincide con el costo. Salida denegada."
            }), 400

        # Permitir la salida: Actualizar el estado del usuario externo a "fuera"
        query_update_externo = """
            UPDATE Externo
            SET estado = 'fuera'
            WHERE id = %s
        """
        cursor.execute(query_update_externo, (id_externo,))

        # Actualizar el estado del vehículo a "permitido"
        query_update_vehiculo = """
            UPDATE Vehiculo
            SET estado = 'permitido'
            WHERE id_externo = %s
        """
        cursor.execute(query_update_vehiculo, (id_externo,))

        # Actualizar el historial de ingreso/egreso con la hora de salida
        query_update_historial = """
            UPDATE Historial_Ingreso_Egreso
            SET horaSalida = CURTIME()
            WHERE id_externo = %s AND horaSalida IS NULL
        """
        cursor.execute(query_update_historial, (id_externo,))

        # Aumentar el número de espacios disponibles en el estacionamiento
        query_update_estacionamiento = """
            UPDATE Estacionamiento
            SET espaciosDisponibles = espaciosDisponibles + 1
            WHERE id = (SELECT id FROM Estacionamiento LIMIT 1)
        """
        cursor.execute(query_update_estacionamiento)

        # Confirmar los cambios
        db_connection.commit()

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Mostrar mensaje de éxito
        return jsonify({
            "status": 200,
            "msg": "Pago recibido correctamente. Salida permitida. ¡Vuelva pronto!",
        }), 200

    except mysql.connector.Error as err:
        # Manejo de errores de la base de datos
        return jsonify({
            "status": 500,
            "msg": f"Error al procesar el pago y la salida: {err}"
        }), 500

    except Exception as e:
        # Manejo de otros errores
        return jsonify({
            "status": 500,
            "msg": f"Error inesperado: {str(e)}"
        }), 500


'''
ACÁ VA EL CÓDIGO PARA EL PANEL DE CLIMA ******************************************************************************
'''
# ----------------------------------------------------------------------------------- INSERTANDO DATOS EN CLIMA
@app.route('/administrador/insertarClima', methods=['POST'])
def insertar_clima():
    try:
        # Obtener los datos enviados en la solicitud POST
        data = request.get_json()
        temperatura = data.get('temperatura')
        humedad = data.get('humedad')

        # Validar que temperatura y humedad estén presentes
        if temperatura is None or humedad is None:
            return jsonify({
                "status": 400,
                "msg": "Faltan datos: temperatura y humedad son requeridos."
            }), 400

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para insertar el clima
        query_insert_clima = """
            INSERT INTO Clima (temperatura, humedad, id_administrador)
            VALUES (%s, %s, %s);
        """
        # id_administrador se fija en 1 para este ejemplo
        cursor.execute(query_insert_clima, (temperatura, humedad, 1))

        # Confirmar la inserción
        db_connection.commit()

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver una respuesta de éxito
        return jsonify({
            "status": 200,
            "msg": "Datos de clima insertados correctamente."
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al insertar datos de clima: {err}"
        }), 400


# ----------------------------------------------------------------------------------- OBTENER DATOS DEL CLIMA
@app.route('/administrador/getClimaActual', methods=['GET'])
def get_clima_actual():
    try:
        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para obtener el último registro de clima
        query_get_clima = """
            SELECT temperatura, humedad, fecha
            FROM Clima
            ORDER BY fecha DESC
            LIMIT 1;
        """
        cursor.execute(query_get_clima)
        clima = cursor.fetchone()

        if not clima:
            return jsonify({
                "status": 400,
                "msg": "No se encontraron datos de clima."
            }), 400

        # Extraer los valores de temperatura, humedad y fecha del resultado
        temperatura, humedad, fecha = clima

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver los datos de clima en la respuesta
        return jsonify({
            "status": 200,
            "msg": "Datos de clima obtenidos correctamente.",
            "temperatura": temperatura,
            "humedad": humedad,
            "fecha": fecha.strftime('%Y-%m-%d %H:%M:%S')  # Formato de fecha y hora
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener los datos de clima: {err}"
        }), 400





'''
ACÁ VA EL CÓDIGO PARA EL PANEL DE USUARIOS, INCLUYENDO EL LOGIN ******************************************************************************
'''
# -----------------------------------------------------------------------------------LOGIN
@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos JSON del POST request
    data = request.json
    user = data.get('user')
    password = data.get('password')
    
    # Validar que el user y password no sean None
    if not user or not password:
        return jsonify({
            "status": 400,
            "msg": "Faltan datos de usuario o contraseña."
        }), 400

    # Crear el hash MD5 de la contraseña ingresada
    password_hash = hashlib.md5(password.encode()).hexdigest()

    try:
        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para obtener el usuario con el nombre y el hash de la contraseña
        cursor.execute("SELECT * FROM Administrador WHERE usuario = %s AND pwd = %s", (user, password_hash))
        result = cursor.fetchone()

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Verificar si se encontró el usuario
        if result:
            return jsonify({
                "status": 200,
                "msg": "Login exitoso."
            }), 200
        else:
            return jsonify({
                "status": 401,
                "msg": "Credenciales incorrectas."
            }), 401

    except mysql.connector.Error as err:
        return jsonify({
            "status": 500,
            "msg": f"Error en la base de datos: {err}"
        }), 500
# -----------------------------------------------------------------------------------LISTA USUARIOS PARA PANEL DE USUARIOS

@app.route('/administrador/listarUsuarios', methods=['GET'])
def listar_usuarios():
    try:
        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para obtener los datos más recientes de historial por usuario
        query = """
            SELECT u.estado, u.saldo, h.fechaEntrada, h.horaEntrada, h.horaSalida, u.UID, u.tipoUsuario
            FROM Usuario u
            LEFT JOIN (
                SELECT h1.*
                FROM Historial_Ingreso_Egreso h1
                JOIN (
                    SELECT UID, MAX(CONCAT(fechaEntrada, ' ', horaEntrada)) AS max_fecha
                    FROM Historial_Ingreso_Egreso
                    GROUP BY UID
                ) h2 ON h1.UID = h2.UID AND CONCAT(h1.fechaEntrada, ' ', h1.horaEntrada) = h2.max_fecha
            ) h ON u.UID = h.UID;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()

        # Procesar los resultados
        usuarios = []
        for row in rows:
            usuarios.append({
                "estado": row[0],           # estado desde Usuario
                "saldo": row[1],            # saldo desde Usuario
                "fecha": str(row[2]),       # fechaEntrada desde Historial_Ingreso_Egreso
                "horaIngreso": str(row[3]), # horaEntrada desde Historial_Ingreso_Egreso
                "horaEgreso": str(row[4]),  # horaSalida desde Historial_Ingreso_Egreso
                "uid": row[5],              # UID desde Usuario
                "tipoUsuario": row[6]       # tipoUsuario desde Usuario
            })

        # Consulta SQL para obtener los datos más recientes de historial por externo
        query_externos = """
            SELECT e.estado, h.fechaEntrada, h.horaEntrada, h.horaSalida, e.id
            FROM Externo e
            LEFT JOIN (
                SELECT h1.*
                FROM Historial_Ingreso_Egreso h1
                JOIN (
                    SELECT id_externo, MAX(CONCAT(fechaEntrada, ' ', horaEntrada)) AS max_fecha
                    FROM Historial_Ingreso_Egreso
                    GROUP BY id_externo
                ) h2 ON h1.id_externo = h2.id_externo AND CONCAT(h1.fechaEntrada, ' ', h1.horaEntrada) = h2.max_fecha
            ) h ON e.id = h.id_externo;
        """

        cursor.execute(query_externos)
        rows_externos = cursor.fetchall()

        # Procesar los resultados de los externos
        externos = []
        for row in rows_externos:
            externos.append({
                "estado": row[0],           # estado desde Externo
                "fecha": str(row[1]),       # fechaEntrada desde Historial_Ingreso_Egreso
                "horaIngreso": str(row[2]), # horaEntrada desde Historial_Ingreso_Egreso
                "horaEgreso": str(row[3]),  # horaSalida desde Historial_Ingreso_Egreso
                "id": row[4]                # id desde Externo
            })

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver respuesta exitosa
        return jsonify({
            "status": 200,
            "msg": "Usuarios listados correctamente",
            "usuarios": usuarios,
            "externos": externos
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al listar usuarios: {err}"
        }), 400
    
# -----------------------------------------------------------------------------------BUSCAR USUARIO POR UID Y RETORNAR INFORMACION DE USUARIO Y HISTORIAL DE INGRESOS Y EGRESOS

@app.route('/administrador/obtenerusuario', methods=['POST'])
def obtener_usuario():
    try:
        # Obtener datos de la solicitud POST
        data = request.get_json()
        uid = data.get('uid')

        if not uid:
            return jsonify({
                "status": 400,
                "msg": "UID no proporcionado."
            }), 400

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consultar los datos del usuario basado en el UID
        query_usuario = """
            SELECT nombre, apellido, UID, RFID, saldo
            FROM Usuario
            WHERE UID = %s
        """
        cursor.execute(query_usuario, (uid,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({
                "status": 400,
                "msg": "Usuario no encontrado."
            }), 400

        # Consultar el historial de ingreso/egreso del usuario junto con los detalles del vehículo
        query_historial = """
            SELECT h.id, h.fechaEntrada, h.horaEntrada, h.horaSalida, h.costo, v.tipoVehiculo, v.placa
            FROM Historial_Ingreso_Egreso h
            LEFT JOIN Vehiculo v ON h.UID = v.UID
            WHERE h.UID = %s
            ORDER BY h.fechaEntrada DESC, h.horaEntrada DESC
        """
        cursor.execute(query_historial, (uid,))
        historial = cursor.fetchall()

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Procesar los datos del historial
        historial_list = []
        for record in historial:
            historial_list.append({
                "id": record[0],              # id desde Historial_Ingreso_Egreso
                "fecha": str(record[1]),       # fechaEntrada desde Historial_Ingreso_Egreso
                "horaEntrada": str(record[2]), # horaEntrada desde Historial_Ingreso_Egreso
                "horaSalida": str(record[3]),  # horaSalida desde Historial_Ingreso_Egreso
                "costo": record[4],            # costo desde Historial_Ingreso_Egreso
                "tipoVehiculo": record[5],     # tipoVehiculo desde Vehículo
                "placa": record[6]             # placa desde Vehículo
            })

        # Devolver la respuesta con la información del usuario y su historial
        return jsonify({
            "status": 200,
            "msg": "Usuario encontrado exitosamente.",
            "nombre": usuario[0],  # nombre desde Usuario
            "apellido": usuario[1], # apellido desde Usuario
            "uid": usuario[2],      # UID desde Usuario
            "rfid": usuario[3],     # RFID desde Usuario
            "saldo": usuario[4],    # saldo desde Usuario
            "historial": historial_list
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener usuario: {err}"
        }), 400
    
@app.route('/administrador/obtenerexterno', methods=['POST'])
def obtener_externo():
    try:
        # Obtener datos de la solicitud POST
        data = request.get_json()
        id_externo = data.get('id_externo')

        if not id_externo:
            return jsonify({
                "status": 400,
                "msg": "ID de externo no proporcionado."
            }), 400

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consultar los datos del usuario externo basado en el ID
        query_externo = """
            SELECT nombre, apellido, id
            FROM Externo
            WHERE id = %s
        """
        cursor.execute(query_externo, (id_externo,))
        externo = cursor.fetchone()

        if not externo:
            return jsonify({
                "status": 400,
                "msg": "Externo no encontrado."
            }), 400

        # Consultar el historial de ingreso/egreso del externo junto con los detalles del vehículo
        query_historial = """
            SELECT h.id, h.fechaEntrada, h.horaEntrada, h.horaSalida, h.costo, v.tipoVehiculo, v.placa
            FROM Historial_Ingreso_Egreso h
            LEFT JOIN Vehiculo v ON h.id_externo = v.id_externo
            WHERE h.id_externo = %s
            ORDER BY h.fechaEntrada DESC, h.horaEntrada DESC
        """
        cursor.execute(query_historial, (id_externo,))
        historial = cursor.fetchall()

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Procesar los datos del historial
        historial_list = []
        for record in historial:
            historial_list.append({
                "id": record[0],              # id desde Historial_Ingreso_Egreso
                "fecha": str(record[1]),       # fechaEntrada desde Historial_Ingreso_Egreso
                "horaEntrada": str(record[2]), # horaEntrada desde Historial_Ingreso_Egreso
                "horaSalida": str(record[3]),  # horaSalida desde Historial_Ingreso_Egreso
                "costo": record[4],            # costo desde Historial_Ingreso_Egreso
                "tipoVehiculo": record[5],     # tipoVehiculo desde Vehículo
                "placa": record[6]             # placa desde Vehículo
            })

        # Devolver la respuesta con la información del externo y su historial
        return jsonify({
            "status": 200,
            "msg": "Externo encontrado exitosamente.",
            "nombre": externo[0],  # nombre desde Externo
            "apellido": externo[1], # apellido desde Externo
            "id": externo[2],      # id desde Externo
            "historial": historial_list
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener externo: {err}"
        }), 400

# -----------------------------------------------------------------------------------EDITAR SALDO DEL USUARIO

# Ruta para sumar saldo
@app.route('/administrador/sumarSaldo', methods=['POST'])
def sumar_saldo():
    try:
        data = request.get_json()
        uid = data.get('uid')

        if not uid:
            return jsonify({
                "status": 400,
                "msg": "UID no proporcionado."
            }), 400

        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consultar el saldo actual del usuario
        cursor.execute("SELECT saldo FROM Usuario WHERE UID = %s", (uid,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({
                "status": 400,
                "msg": "Usuario no encontrado."
            }), 400

        # Sumar 1.00 al saldo
        nuevo_saldo = usuario[0] + 1.00
        cursor.execute("UPDATE Usuario SET saldo = %s WHERE UID = %s", (nuevo_saldo, uid))
        db_connection.commit()

        # Cerrar conexión
        cursor.close()
        db_connection.close()

        return jsonify({
            "status": 200,
            "msg": "Saldo incrementado correctamente.",
            "saldo": nuevo_saldo
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al actualizar el saldo: {err}"
        }), 400

# Ruta para restar saldo
@app.route('/administrador/restarSaldo', methods=['POST'])
def restar_saldo():
    try:
        data = request.get_json()
        uid = data.get('uid')

        if not uid:
            return jsonify({
                "status": 400,
                "msg": "UID no proporcionado."
            }), 400

        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consultar el saldo actual del usuario
        cursor.execute("SELECT saldo FROM Usuario WHERE UID = %s", (uid,))
        usuario = cursor.fetchone()

        if not usuario:
            return jsonify({
                "status": 400,
                "msg": "Usuario no encontrado."
            }), 400

        # Verificar que el saldo no sea menor a 0 al restar
        saldo_actual = usuario[0]
        if saldo_actual <= 0:
            return jsonify({
                "status": 400,
                "msg": "Saldo insuficiente. No se puede restar más."
            }), 400

        # Restar 1.00 del saldo
        nuevo_saldo = saldo_actual - 1.00
        cursor.execute("UPDATE Usuario SET saldo = %s WHERE UID = %s", (nuevo_saldo, uid))
        db_connection.commit()

        # Cerrar conexión
        cursor.close()
        db_connection.close()

        return jsonify({
            "status": 200,
            "msg": "Saldo restado correctamente.",
            "saldo": nuevo_saldo
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al actualizar el saldo: {err}"
        }), 400

'''
ACÁ VA EL CÓDIGO PARA EL PANEL DE MONITOREO ******************************************************************************
'''
# -----------------------------------------------------------------------------------OBTENER LA CANTIDAD DE VEHICULOS DENTRO DEL PARQUEO

@app.route('/administrador/getCantidadVehiculos', methods=['GET'])
def get_cantidad_vehiculos():
    try:
        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para obtener la capacidad total y los espacios disponibles del estacionamiento
        query = """
            SELECT capacidad, espaciosDisponibles
            FROM Estacionamiento
            LIMIT 1;
        """
        cursor.execute(query)
        estacionamiento = cursor.fetchone()

        if not estacionamiento:
            return jsonify({
                "status": 401,
                "msg": "No se encontró información sobre el estacionamiento."
            }), 401

        # Calcular la cantidad de vehículos dentro del parqueo
        capacidad_total = estacionamiento[0]            # Capacidad total del estacionamiento
        espacios_disponibles = estacionamiento[1]       # Espacios disponibles en el estacionamiento
        cantidad_vehiculos = capacidad_total - espacios_disponibles  # Vehículos dentro del parqueo

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver la respuesta con la cantidad de vehículos
        return jsonify({
            "status": 200,
            "msg": "Cantidad de vehículos obtenida correctamente.",
            "cantidad": cantidad_vehiculos
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener la cantidad de vehículos: {err}"
        }), 400

# -----------------------------------------------------------------------------------OBTENER LOS ESPACIOS DISPONIBLES DENTRO DEL PARQUEO

@app.route('/administrador/getEspaciosDisponibles', methods=['GET'])
def get_espacios_disponibles():
    try:
        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para obtener los espacios disponibles del estacionamiento
        query = """
            SELECT espaciosDisponibles
            FROM Estacionamiento
            LIMIT 1;
        """
        cursor.execute(query)
        estacionamiento = cursor.fetchone()

        if not estacionamiento:
            return jsonify({
                "status": 400,
                "msg": "No se encontró información sobre el estacionamiento."
            }), 400

        # Obtener el número de espacios disponibles
        espacios_disponibles = estacionamiento[0]

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver la respuesta con los espacios disponibles
        return jsonify({
            "status": 200,
            "msg": "Espacios disponibles obtenidos correctamente.",
            "espaciosDisponibles": espacios_disponibles
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener los espacios disponibles: {err}"
        }), 400


# -------------------------------------------------------------------   OBTENER EL PORCENTAJE DE OCUPACIÓN DENTRO DEL PARQUEO

@app.route('/administrador/getPorcentajeOcupacion', methods=['GET'])
def get_porcentaje_ocupacion():
    try:
        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para obtener la capacidad total y los espacios disponibles del estacionamiento
        query = """
            SELECT capacidad, espaciosDisponibles
            FROM Estacionamiento
            LIMIT 1;
        """
        cursor.execute(query)
        estacionamiento = cursor.fetchone()

        if not estacionamiento:
            return jsonify({
                "status": 400,
                "msg": "No se encontró información sobre el estacionamiento."
            }), 400

        # Obtener los valores de capacidad y espacios disponibles
        capacidad_total = estacionamiento[0]
        espacios_disponibles = estacionamiento[1]

        # Calcular el porcentaje de ocupación
        vehiculos_ocupando = capacidad_total - espacios_disponibles
        porcentaje_ocupacion = (vehiculos_ocupando / capacidad_total) * 100

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver la respuesta con el porcentaje de ocupación
        return jsonify({
            "status": 200,
            "msg": "Porcentaje de ocupación obtenido correctamente.",
            "porcentajeOcupacion": round(porcentaje_ocupacion, 2)
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener el porcentaje de ocupación: {err}"
        }), 400

# -------------------------------------------------------------------   OBTENER EL PORCENTAJE DE USUARIOS EXTERNOS
@app.route('/administrador/getPorcentajeExternos', methods=['GET'])
def get_porcentaje_externos():
    try:
        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta SQL para contar el total de registros en Historial_Ingreso_Egreso
        query_total = """
            SELECT COUNT(*) 
            FROM Historial_Ingreso_Egreso
            WHERE horaSalida IS NOT NULL;
        """
        cursor.execute(query_total)
        total_registros = cursor.fetchone()[0]

        if total_registros == 0:
            return jsonify({
                "status": 400,
                "msg": "No se han encontrado registros de ingresos y salidas."
            }), 400

        # Consulta SQL para contar los usuarios externos en el historial
        query_externos = """
            SELECT COUNT(*)
            FROM Historial_Ingreso_Egreso
            WHERE esExterno = TRUE AND horaSalida IS NOT NULL;
        """
        cursor.execute(query_externos)
        total_externos = cursor.fetchone()[0]

        # Calcular el porcentaje de usuarios externos
        porcentaje_externos = (total_externos / total_registros) * 100

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver la respuesta con el porcentaje de usuarios externos
        return jsonify({
            "status": 200,
            "msg": "Porcentaje de usuarios externos obtenido correctamente.",
            "porcentajeExternos": round(porcentaje_externos, 2)
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener el porcentaje de usuarios externos: {err}"
        }), 400

# -------------------------------------------------------------------   NUMERO DE VEHÍCULOS QUE HAN INGRESADO Y SALIDO DEL PARQUEO EN TODO EL DIA

@app.route('/administrador/getVehiculosDia', methods=['GET'])
def get_vehiculos_dia():
    try:
        # Obtener fecha actual para limitar la búsqueda al día de hoy
        fecha_hoy = datetime.date.today()

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta para obtener el número de vehículos que ingresaron hoy
        query_ingresados = """
            SELECT COUNT(*) 
            FROM Historial_Ingreso_Egreso 
            WHERE fechaEntrada = %s;
        """
        cursor.execute(query_ingresados, (fecha_hoy,))
        total_ingresados = cursor.fetchone()[0]

        # Consulta para obtener el número de vehículos que salieron hoy
        query_salidos = """
            SELECT COUNT(*) 
            FROM Historial_Ingreso_Egreso 
            WHERE horaSalida IS NOT NULL AND fechaEntrada = %s;
        """
        cursor.execute(query_salidos, (fecha_hoy,))
        total_salidos = cursor.fetchone()[0]

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver la respuesta con los datos de ingresados y salidos
        return jsonify({
            "status": 200,
            "msg": "Vehículos ingresados y salidos obtenidos correctamente.",
            "vehiculosIngresados": total_ingresados,
            "vehiculosSalidos": total_salidos
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener los datos de vehículos: {err}"
        }), 400


# lo mismo que el anterior pero para manejo en tiempo real            utilizar esta petición de preferencia
@app.route('/administrador/getVehiculosTiempoReal', methods=['GET'])
def get_vehiculos_tiempo_real():
    try:
        # Obtener fecha actual para limitar la búsqueda al día de hoy
        fecha_hoy = datetime.date.today()

        # Conectar a la base de datos
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        # Consulta para obtener el número de vehículos que ingresaron hoy
        query_ingresados = """
            SELECT COUNT(*) 
            FROM Historial_Ingreso_Egreso 
            WHERE fechaEntrada = %s;
        """
        cursor.execute(query_ingresados, (fecha_hoy,))
        total_ingresados = cursor.fetchone()[0]

        # Consulta para obtener el número de vehículos que están fuera (que ya salieron hoy)
        query_salidos = """
            SELECT COUNT(*) 
            FROM Historial_Ingreso_Egreso 
            WHERE horaSalida IS NOT NULL AND fechaEntrada = %s;
        """
        cursor.execute(query_salidos, (fecha_hoy,))
        total_salidos = cursor.fetchone()[0]

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Calcular los vehículos dentro (ingresados - salidos)
        vehiculos_dentro = total_ingresados - total_salidos

        # Devolver la respuesta con los datos de ingresados, salidos y vehículos dentro
        return jsonify({
            "status": 200,
            "msg": "Datos de vehículos en tiempo real obtenidos correctamente.",
            "vehiculosIngresados": total_ingresados,
            "vehiculosSalidos": total_salidos,
            "vehiculosDentro": vehiculos_dentro
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al obtener los datos de vehículos: {err}"
        }), 400

#if __name__ == "__main__":
#    connect_to_mysql()

if __name__ == "__main__":
    app.run(debug=True)
