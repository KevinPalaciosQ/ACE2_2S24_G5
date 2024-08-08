#include <SPI.h>
#include <MFRC522.h>
#include "User.h" // Incluye el archivo de encabezado para la clase User

#define RST_PIN 9                         //Pin 9 para el reset del RC522
#define SS_PIN 10                         //Pin 10 para el SS (SDA) del RC522

MFRC522 mfrc522(SS_PIN, RST_PIN);         //Creamos el objeto para el RC522

User user1("860FA022");                   //Se crea un objeto de tipo usuario con su pin correspondiente
User user2("D46BE373");                   //Se crea un objeto de tipo usuario con su pin correspondiente
String pin = "";

void setup() {
  Serial.begin(9600);                     //Iniciamos la comunicación serial
  SPI.begin();                            //Iniciamos el bus SPI
  mfrc522.PCD_Init();                     //Iniciamos el MFRC522
  Serial.println("Lectura del UID");      //Imprimimos en consola el inicio de la lectura del UID
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent()) {  //Leemos si hay una tarjeta presente

  /*
      Propósito: Intenta leer el número de serie (UID) de la tarjeta RFID actual.
      Retorno: Devuelve true si se ha leído correctamente el UID de la tarjeta y false si ha fallado en la lectura.
      Cómo Funciona: Cuando esta función es llamada, el lector intenta obtener la información de la tarjeta que 
      está cerca. Si la lectura es exitosa, la información de la tarjeta (como el UID) se almacena en el objeto mfrc522.
  */

    if (mfrc522.PICC_ReadCardSerial()) {  // Enviamos serialemente su UID
      Serial.print("Card UID:");    
      pin = "";                           // Limpiar el pin antes de llenarlo nuevamente
      
      // La direccion se guarda en un array de bytes, que imprimimos uno u otro utilizando operador ternario
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        
        //Se valida que se imprima un 0 acompanado de un numero si es menor a 16 para siempre tener
        //el formato de 4 pares, si el numero es mayor a 16 solo imprimimos un espacio para tener
        //separados los pares
        Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
        //Accedo a la posicion i del arreglo y lo imprimo en formato hexadecimal
        Serial.print(mfrc522.uid.uidByte[i], HEX);
        
        pin += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
        pin += String(mfrc522.uid.uidByte[i], HEX);
      }

      pin.toUpperCase(); // Asegúrate de que el pin esté en mayúsculas para la comparación

      if (pin.equals(user1.getPin())) {
        user1.setState(true);
        Serial.println("\nUser 1");
      } else if (pin.equals(user2.getPin())) {
        user2.setState(true);
        Serial.println("\nUser 2");
      } else {
        Serial.println("User desconocido");
      }

      mfrc522.PICC_HaltA();
    }
  }
}
