#include <SPI.h>
#include <MFRC522.h>
#include "User.h" 
#include <Servo.h>

// RC522
#define RST_PIN 9                         
#define SS_PIN 10                         
MFRC522 mfrc522(SS_PIN, RST_PIN);         
// Users
User users[]                = { User("860FA022"), User("D46BE373") };  
const int numUsers          = sizeof(users) / sizeof(users[0]);
String pin                  =    "";

// PIR and IR sensors
volatile bool pirCondition  =   false;  
const int loginPin          =   8;  
const int logoutPin         =   7; 
const int PIRPin            =   2;  

// Coin Hopper
volatile bool extULogin     =   false;
const int coinHopperPin     =   6;
const int externalUserPin   =   3;

// Servo
Servo myServo;
const int servoPin          =   5;

void setup() {
  pinMode(PIRPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIRPin), handleInterrupt, CHANGE);
  pinMode(externalUserPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(externalUserPin), loginExternalUser, RISING);
  pinMode(loginPin, INPUT);   
  pinMode(logoutPin, INPUT); 
  pinMode(coinHopperPin, INPUT); 
  myServo.attach(servoPin);
  Serial.begin(9600);                     //Iniciamos la comunicación serial
  SPI.begin();                            //Iniciamos el bus SPI
  mfrc522.PCD_Init();                     //Iniciamos el MFRC522
}

void loop() {
  if (pirCondition == true){
    if (mfrc522.PICC_IsNewCardPresent()) {  
      if (mfrc522.PICC_ReadCardSerial()) {  
        pin = "";                           

        for (byte i = 0; i < mfrc522.uid.size; i++) {
          pin += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
          pin += String(mfrc522.uid.uidByte[i], HEX);
        }

        pin.toUpperCase(); 

        for (int i = 0; i < numUsers; i++) {  // Itera sobre el array de objetos User
          if (pin.equals(users[i].getPin())) {
            if (users[i].getState() == false && digitalRead(loginPin) == HIGH) {
              users[i].setState(true);
              Serial.println("User: "+pin);
              Serial.println("\nUser logged in");

              handleServoMotion();
              break;

            } else if (users[i].getState() == true && digitalRead(logoutPin) == HIGH) {
              users[i].setState(false);
              Serial.println("\nUser logged out");
              
              handleServoMotion();
              break;

            } else {
              if (users[i].getState()) {
                Serial.println("User: " + users[i].getPin() + " is logged in");
              } else {
                Serial.println("User: " + users[i].getPin() + " is logged out");
              }
            }
          } 
        }
        

        mfrc522.PICC_HaltA();
      }
    } else if (extULogin == true && digitalRead(loginPin) == HIGH) {
      Serial.println("External user logged in");
      handleServoMotion();
      extULogin = false;
    } else {
      if (digitalRead(coinHopperPin) == HIGH && digitalRead(logoutPin) == HIGH) {
        Serial.println("Coin inserted, External user logout");
        handleServoMotion();
      } 
    }
  }
}

void handleInterrupt() {
  pirCondition == true ? pirCondition = false : pirCondition = true;
}

void loginExternalUser() {
  if (extULogin == false) {
    extULogin = true;
  } 
}

void handleServoMotion() {
  for (int angle = 0; angle <= 180; angle++) {
    myServo.write(angle); 
    delay(15); 
  }
  while (pirCondition == true) {
    Serial.println("Servo at 90 degrees");
  }
  delay(2000);
  Serial.println("Servo at 0 degrees");
  for (int angle = 180; angle >= 0; angle--) {
    myServo.write(angle); 
    delay(15); 
  }
}
