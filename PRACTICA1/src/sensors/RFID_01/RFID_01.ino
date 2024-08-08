#include <SPI.h>
#include <MFRC522.h>
#include "User.h" 

#define RST_PIN 9                         //Pin 9 para el reset del RC522
#define SS_PIN 10                         //Pin 10 para el SS (SDA) del RC522

MFRC522 mfrc522(SS_PIN, RST_PIN);         

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
  if (mfrc522.PICC_IsNewCardPresent()) {  
    if (mfrc522.PICC_ReadCardSerial()) {  
      Serial.print("Card UID:");    
      pin = "";                           

      for (byte i = 0; i < mfrc522.uid.size; i++) {
        pin += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
        pin += String(mfrc522.uid.uidByte[i], HEX);
      }

      pin.toUpperCase(); 

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
