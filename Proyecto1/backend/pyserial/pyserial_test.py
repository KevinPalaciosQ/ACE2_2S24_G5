import time
import serial
import json
import re, random, string, requests

url = 'http://localhost:3306'
ard_object = serial.Serial('COM3', 9600)
time.sleep(2)  # Esperar a que la conexión se establezca

def weather_request(humidity_data, temp_data):
    weather_data = {
        "temperatura"   :   humidity_data,
        "humedad"       :   temp_data
    }
    responseLoginAdmin = requests.post(url+'/administrador/insertarClima', json=weather_data)

    if responseLoginAdmin.status_code == 200:
        print("Datos enviados correctamente:", responseLoginAdmin.json())
    else:
        print(f"Error {responseLoginAdmin.status_code}: {responseLoginAdmin.json()}")

def userlogin_request(id, path):
    data = {
        "rfid"  : id
    }
    responseLogin = requests.post(url+path, json=data)
    print(responseLogin.json())

def userlogout_request(id, path):
    data = {
        "rfid"  :   id
    }
    responseLogout = requests.post(url+path, json=data)
    print(responseLogout.json())


while True:
    if ard_object.in_waiting > 0:
        data = ard_object.readline().decode('utf-8').strip()
        try:
            user_type = data.split('-')
            if len(user_type) < 3:
                print(f"Error en formato de datos: {data}")
                continue  # Ir a la siguiente iteración si el formato es incorrecto
            if user_type[0] == 'LOGIN':
                if user_type[1] == "Admin":
                    id, temperature, humidity = user_type[2].split(',')
                    temp_value = re.findall(r"\d+\.\d+", temperature)[0]  # Buscar número con decimales en x
                    humidity_value = re.findall(r"\d+\.\d+", humidity)[0]  # Buscar número con decimales en y
                    data_json = {
                        "login" : [
                            {
                                "id": id,
                                "humidity": temp_value,
                                "temperature": humidity_value
                            }
                        ]
                    }
                    print(json.dumps(data_json, indent=4))

                    userlogin_request(id, '/administrador/entradaUsuario')
                    weather_request(humidity_value, temp_value)

                elif user_type[1] == "Student":
                    id, temperature, humidity = user_type[2].split(',')
                    temp_value = re.findall(r"\d+\.\d+", temperature)[0]  # Buscar número con decimales en x
                    humidity_value = re.findall(r"\d+\.\d+", humidity)[0]  # Buscar número con decimales en y
                    data_json = {
                        "login" : [
                            {
                                "id": id,
                                "humidity": temp_value,
                                "temperature": humidity_value
                            }
                        ]
                    }
                    print(json.dumps(data_json, indent=4))

                    userlogin_request(id, '/administrador/entradaUsuario')
                    weather_request(humidity_value, temp_value)

                elif user_type[1] == "External":
                    id, temperature, humidity = user_type[2].split(',')
                    temp_value = re.findall(r"\d+\.\d+", temperature)[0]  # Buscar número con decimales en x
                    humidity_value = re.findall(r"\d+\.\d+", humidity)[0]  # Buscar número con decimales en y

                    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
                    numbers = ''.join(random.choices(string.digits, k=2))
                    random_string = letters + numbers

                    data_json = {
                        "login" : [
                            {
                                "id": random_string,
                                "humidity": temp_value,
                                "temperature": humidity_value
                            }
                        ]
                    }
                    print(json.dumps(data_json, indent=4))

                    userlogin_request(random_string, '/administrador/logicaEntradaExterno')
                    weather_request(humidity_value, temp_value)

                else:
                    print(f"Error user no compatible")
            elif user_type[0] == 'LOGOUT':
                if user_type[1] == "Admin":
                    id, temperature, humidity = user_type[2].split(',')
                    temp_value = re.findall(r"\d+\.\d+", temperature)[0]  # Buscar número con decimales en x
                    humidity_value = re.findall(r"\d+\.\d+", humidity)[0]  # Buscar número con decimales en y
                    data_json = {
                        "logout" : [
                            {
                                "id": id,
                                "humidity": temp_value,
                                "temperature": humidity_value
                            }
                        ]
                    }
                    print(json.dumps(data_json, indent=4))

                    userlogout_request(id, '/administrador/entradaUsuario')
                    weather_request(humidity_value, temp_value)

                elif user_type[1] == "Student":
                    id, temperature, humidity = user_type[2].split(',')
                    temp_value = re.findall(r"\d+\.\d+", temperature)[0]  # Buscar número con decimales en x
                    humidity_value = re.findall(r"\d+\.\d+", humidity)[0]  # Buscar número con decimales en y
                    data_json = {
                        "logout" : [
                            {
                                "id": id,
                                "humidity": temp_value,
                                "temperature": humidity_value
                            }
                        ]
                    }
                    print(json.dumps(data_json, indent=4))

                    userlogout_request(id, '/administrador/entradaUsuario')
                    weather_request(humidity_value, temp_value)

                elif user_type[1] == "External":
                    id, temperature, humidity = user_type[2].split(',')
                    temp_value = re.findall(r"\d+\.\d+", temperature)[0]  # Buscar número con decimales en x
                    humidity_value = re.findall(r"\d+\.\d+", humidity)[0]  # Buscar número con decimales en y
                    data_json = {
                        "logout" : [
                            {
                                "id": id,
                                "humidity": temp_value,
                                "temperature": humidity_value
                            }
                        ]
                    }
                    print(json.dumps(data_json, indent=4))

                    userlogout_request(id, '/administrador/pagoSalidaExterno')
                    weather_request(humidity_value, temp_value)

        except ValueError:
            print(f"Error al procesar los datos: {ValueError}")
    else:
        time.sleep(0.1)  # Esperar un poco antes de volver a comprobar


