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

        # Cerrar cursor y conexión
        cursor.close()
        db_connection.close()

        # Devolver respuesta exitosa
        return jsonify({
            "status": 200,
            "msg": "Usuarios listados correctamente",
            "usuarios": usuarios
        }), 200

    except mysql.connector.Error as err:
        return jsonify({
            "status": 400,
            "msg": f"Error al listar usuarios: {err}"
        }), 400
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