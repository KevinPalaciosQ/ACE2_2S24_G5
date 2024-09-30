import serial
import json

ard_object = serial.Serial('COM3', 9600)

data = ard_object.readline()

while True:
    if ard_object.in_waiting > 0:
        data = ard_object.readline().decode('utf-8').strip()
        try:
            id, temperature, humidity = data.split(',')
            data_json = {
                "id": id,
                "temperature": temperature,
                "humidity": humidity
            }
            print(json.dumps(data_json, indent=4))
        except ValueError:
            print(f"Error al procesar los datos: {data}")