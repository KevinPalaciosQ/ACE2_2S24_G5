import serial, time

ard_object = serial.Serial('COM3', 9600)

data = ard_object.readline()

while True:
    print(data)
    time.sleep(1)
    data = ard_object.readline()