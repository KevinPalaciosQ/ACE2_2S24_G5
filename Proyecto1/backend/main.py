import mysql.connector
from mysql.connector import Error
from datetime import timedelta
from flask import Flask, jsonify, request
import hashlib
app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',  # Cambia si tu servidor no está en localhost
        port=3306,         # Cambia si tu servidor usa otro puerto
        user='root',       # Cambia según tu usuario de MySQL
        password='dedicadoArqui2',  # Cambia por tu contraseña de MySQL
        database='arqbased'  # Cambia por tu base de datos
    )

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












'''
ACÁ VA EL CÓDIGO PARA EL PANEL DE CLIMA ******************************************************************************
'''

# -----------------------------------------------------------------------------------Clima
@app.route('/administrador/graficaClima', methods=['GET'])
def get_clima():
    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM Usuario")
    rows = cursor.fetchall()
    cursor.close()
    db_connection.close()
    
    usuarios = []
    for row in rows:
        usuarios.append({
            "UID": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "saldo": row[3],
            "RFID": row[4],
            "tipoUsuario": row[5]
        })
    return jsonify(usuarios)


'''
def connect_to_mysql():
    try:
        # Crear la conexión a MySQL
        connection = mysql.connector.connect(
            host='localhost',  # Cambia si tu servidor no está en localhost
            port=3306,         # Cambia si tu servidor usa otro puerto
            user='root',       # Cambia según tu usuario de MySQL
            password='dedicadoArqui2',  # Cambia por tu contraseña de MySQL
            database='arqbased'  # Cambia por tu base de datos
        )

        if connection.is_connected():
            print("Conexión exitosa a MySQL")
            cursor = connection.cursor()
            
            # Ejecutar una consulta simple
            cursor.execute("SELECT * FROM Historial_Ingreso_Egreso;")
            rows = cursor.fetchall()

            print("Datos de la tabla:")
            for row in rows:
                # Desempaquetar las columnas de la fila
                (id, UID, id_vehiculo, id_estacionamiento, fecha_entrada, hora_entrada, hora_salida, costo) = row

                # Formatear la fecha de entrada
                fecha_entrada_str = fecha_entrada.strftime('%Y-%m-%d')

                # Formatear la hora de entrada (timedelta a horas, minutos y segundos)
                hora_entrada_str = (timedelta(seconds=hora_entrada.seconds) 
                                    if isinstance(hora_entrada, timedelta) 
                                    else hora_entrada)

                # Formatear la hora de salida (puede ser None si no ha salido)
                hora_salida_str = (timedelta(seconds=hora_salida.seconds) 
                                   if isinstance(hora_salida, timedelta) 
                                   else 'No ha salido')

                # Imprimir los resultados formateados
                print(f"ID: {id}, UID: {UID}, Vehículo: {id_vehiculo}, Estacionamiento: {id_estacionamiento}")
                print(f"Fecha de Entrada: {fecha_entrada_str}")
                print(f"Hora de Entrada: {hora_entrada_str}")
                print(f"Hora de Salida: {hora_salida_str}")
                print(f"Costo: {costo}")
                print("-----")

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión cerrada")
'''
#if __name__ == "__main__":
#    connect_to_mysql()

if __name__ == "__main__":
    app.run(debug=True)