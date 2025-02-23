#include <SPI.h>
#include <MFRC522.h>
#include "User.h" 
#include <Servo.h>
#include <Wire.h> 
#include "DHT.h"
#include <EEPROM.h>

// RC522 
#define RST_PIN 9                         
#define SS_PIN 10                         
MFRC522 mfrc522(SS_PIN, RST_PIN);         

//DHT11
#define DHTPIN 4     // Pin donde está conectado el sensor
#define DHTTYPE DHT11   // Descomentar si se usa el DHT 11
DHT dht(DHTPIN, DHTTYPE);

// Users
String student = "860FA022";
String admin = "D46BE373";
User users[]                = { User("860FA022"), User("D46BE373") };  
//User users[]                = { User("Student"), User("Admin") };  
const int numUsers          = sizeof(users) / sizeof(users[0]);
String pin                  =    "";

// PIR and IR sensors
volatile bool pirCondition  =   false;  
const int loginPin          =   8;  
const int logoutPin         =   7; 
const int PIRPin            =   2;  

volatile unsigned long lastInterruptTime = 0; // Tiempo de la última interrupción
const unsigned long debounceDelay = 50; // Tiempo de debounce en milisegundos

// Coin Hopper
volatile bool extULogout     =   false;
const int coinHopperPin     =   3;
const int externalUserPin   =   6;

// Servo
Servo myServo;
const int servoPin          =   5;



void setup() {
  pinMode(PIRPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIRPin), handleInterrupt, CHANGE);
  pinMode(externalUserPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(coinHopperPin), logoutExternalUser, RISING);
  
  pinMode(loginPin, INPUT);   
  pinMode(logoutPin, INPUT); 
  pinMode(externalUserPin, INPUT); 

  Serial.begin(9600);                     //Iniciamos la comunicación serial
  dht.begin();
  myServo.attach(servoPin);
  SPI.begin();                            //Iniciamos el bus SPI
  mfrc522.PCD_Init();                     //Iniciamos el MFRC522
}

void loop() {
  delay(2000);
  float h = dht.readHumidity(); 
  float t = dht.readTemperature();

  String humidityText = "Humidity: " + String(h) + "%";
  String temperatureText = "Temp: " + String(t) + " C";

  Serial.print("ENVIRONMENT-");
  Serial.print(humidityText);
  Serial.print("-");
  Serial.println(temperatureText);

  login();

}

void handleInterrupt() {
  unsigned long currentTime = millis(); 
  
  if (currentTime - lastInterruptTime < debounceDelay) {
    return;
  }

  lastInterruptTime = currentTime;

  if (pirCondition == true) {
    pirCondition = false;
  } else {
    pirCondition = true;
    //Serial.println("Cambiando de 0 a 1");
  }
}

void logoutExternalUser() {
  if (extULogout == false) {
    extULogout = true;
  } 
}

void handleServoMotion() {
  for (int angle = 0; angle <= 180; angle++) {
    myServo.write(angle); 
    delay(15); 
  }
  while (pirCondition == true) {
  }
  delay(2200);
  for (int angle = 180; angle >= 0; angle--) {
    myServo.write(angle); 
    delay(15); 
  }
}

void login(){
  byte studentState;
  byte adminState;
  EEPROM.get(0, studentState);
  EEPROM.get(1, adminState);
  users[0].setState(studentState != 0);
  users[1].setState(adminState != 0);

  // if (users[0].getState()){
  //   Serial.println("Student: Logged in");
  // } else {
  //   Serial.println("Student: Logged out");
  // } 
  // if (users[1].getState()){
  //   Serial.println("Admin: Logged in");
  // } else {
  //   Serial.println("Admin: Logged out");
  // }

  if (pirCondition == true || digitalRead(logoutPin) == LOW){
    if (mfrc522.PICC_IsNewCardPresent()) {  
      if (mfrc522.PICC_ReadCardSerial()) {  
        pin = "";                           

        for (byte i = 0; i < mfrc522.uid.size; i++) {                   //Obtiene ID de TARJETA
          pin += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
          pin += String(mfrc522.uid.uidByte[i], HEX);
        }

        pin.toUpperCase(); 

        for (int i = 0; i < numUsers; i++) {  // Itera sobre el array de objetos User
          if (pin.equals(users[i].getPin())) { // Compara ID estudiante/profesor con el ID de la tarjeta y ve que pertenezca a la lista de usuarios
            if (users[i].getState() == false && digitalRead(loginPin) == LOW) { // Verifica que detecte IR ENTRADA y que el usuario haya salido antes, ******si se cumple hace LOGIN******
              users[i].setState(true);
              EEPROM.write(i, 1);
              String userName = "User: "+pin;

              if (pin.equals("860FA022")){
                Serial.println("LOGIN-Admin-860FA022");
              } else {
                Serial.println("LOGIN-Student-D46BE373");
              }

              handleServoMotion();
              break;

            } else if (users[i].getState() == true && digitalRead(logoutPin) == LOW) { //Verifica que estudiante/profesor ya este dentro y si detecta algo en la salida, **si se cumple hace LOGOUT**
              users[i].setState(false);
              EEPROM.write(i, 0);
              if (users[i].getPin().equals("860FA022")){
                Serial.println("LOGOUT-Admin-860FA022");
              } else {
                Serial.println("LOGOUT-Student-D46BE373");
              }
              
              handleServoMotion();
              break;

            } else { // IMPRIME QUE EL USUARIO YA ESTA ADENTRO Y NO HA SALIDO
              if (users[i].getState()) {                                                  //
                //Serial.println("User: " + users[i].getPin() + " is logged in");
              } else { // IMPRIME QUE EL USUARIO YA ESTE AFUERA Y NO HA ENTRADO
                //Serial.println("User: " + users[i].getPin() + " is logged out");
              }
            }
          } 
        }
        

        mfrc522.PICC_HaltA();
      }
    } else if (digitalRead(externalUserPin) == HIGH && digitalRead(loginPin) == LOW) { //DETECTA QUE PRESIONARON EL PULSADOR Y QUE DETECTO IR ENTRADA, ***HACE LOGIN COMO EXTERNO***
      //Serial.println("External user logged in");
      Serial.println("LOGIN-External-XXXXXX");
      handleServoMotion();
    } else {
      if (extULogout == true && digitalRead(logoutPin) == LOW) { // Valida que se haya depositado la moneda y que en la salida haya alguien, *** HACE LOGOUT COMO EXTERNO***
        //Serial.println("Coin inserted, External user logout");
        Serial.println("LOGOUT-External-XXXXXX");

        handleServoMotion();
        extULogout = false;
      } 
    }
  } //else if (extULogout) {
    //handleServoMotion();
  //}
}
