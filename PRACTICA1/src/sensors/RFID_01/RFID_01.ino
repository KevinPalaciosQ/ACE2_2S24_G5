#include <SPI.h>
#include <MFRC522.h>
#include "User.h" 
#include <Servo.h>
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include "DHT.h"

// RC522 
#define RST_PIN 9                         
#define SS_PIN 10                         
MFRC522 mfrc522(SS_PIN, RST_PIN);         

//DHT11
#define DHTPIN 4     // Pin donde está conectado el sensor
#define DHTTYPE DHT11   // Descomentar si se usa el DHT 11
DHT dht(DHTPIN, DHTTYPE);

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
volatile bool extULogout     =   false;
const int coinHopperPin     =   3;
const int externalUserPin   =   6;

// Servo
Servo myServo;
const int servoPin          =   5;

// LCD I2C
LiquidCrystal_I2C lcd(0x27,16,2);  

void setup() {
  pinMode(PIRPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(PIRPin), handleInterrupt, CHANGE);
  pinMode(externalUserPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(coinHopperPin), logoutExternalUser, RISING);
  
  lcd.init();
  lcd.backlight();
  
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
  float h = dht.readHumidity(); //Leemos la Humedad
  float t = dht.readTemperature(); //Leemos la temperatura en grados Celsius
  float f = dht.readTemperature(true); //Leemos la temperatura en grados Fahrenheit

  String humidityText = "Humidity: " + String(h) + "%";
  String temperatureText = "Temp: " + String(t) + " C";

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(humidityText);
  lcd.setCursor(0,1);
  lcd.print(temperatureText);

  login();

}

void handleInterrupt() {
  pirCondition == true ? pirCondition = false : pirCondition = true;
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
    Serial.println("Servo at 90 degrees");
  }
  delay(2200);
  Serial.println("Servo at 0 degrees");
  for (int angle = 180; angle >= 0; angle--) {
    myServo.write(angle); 
    delay(15); 
  }
}

void login(){
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
              String userName = "User: "+pin;
              lcd.clear();
              Serial.println(userName + "\nUser logged in");

              lcd.setCursor(0, 0); 
              lcd.print(userName);
              
              lcd.setCursor(0, 1); // Coloca el cursor en la segunda fila, primera columna
              lcd.print("Logged in");

              handleServoMotion();
              break;

            } else if (users[i].getState() == true && digitalRead(logoutPin) == LOW) { //Verifica que estudiante/profesor ya este dentro y si detecta algo en la salida, **si se cumple hace LOGOUT**
              users[i].setState(false);
              lcd.clear();
              lcd.setCursor(0,0);
              lcd.print("User logged out");
              Serial.println("\nUser logged out");

              
              handleServoMotion();
              break;

            } else { // IMPRIME QUE EL USUARIO YA ESTA ADENTRO Y NO HA SALIDO
              if (users[i].getState()) {                                                  //
                Serial.println("User: " + users[i].getPin() + " is logged in");
                lcd.clear();
                lcd.setCursor(0, 0);
                lcd.print("User already logged in");
                lcd.setCursor(0, 1);
                lcd.print("logged in");
              } else { // IMPRIME QUE EL USUARIO YA ESTE AFUERA Y NO HA ENTRADO
                Serial.println("User: " + users[i].getPin() + " is logged out");
                lcd.clear();
                lcd.setCursor(0,0);
                lcd.print("User already");
                lcd.setCursor(0,1);
                lcd.print("logged out");
              }
            }
          } 
        }
        

        mfrc522.PICC_HaltA();
      }
    } else if (digitalRead(externalUserPin) == HIGH && digitalRead(loginPin) == LOW) { //DETECTA QUE PRESIONARON EL PULSADOR Y QUE DETECTO IR ENTRADA, ***HACE LOGIN COMO EXTERNO***
      Serial.println("External user logged in");
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("External user");
      lcd.setCursor(0,1);
      lcd.print("logged in");
      handleServoMotion();
    } else {
      if (extULogout == true && digitalRead(logoutPin) == LOW) { // Valida que se haya depositado la moneda y que en la salida haya alguien, *** HACE LOGOUT COMO EXTERNO***
        Serial.println("Coin inserted, External user logout");

        lcd.setCursor(0,0);
        lcd.print("Coin inserted:");
        lcd.setCursor(0,1);
        lcd.print("EU logged out");

        handleServoMotion();
        extULogout = false;
      } 
    }
  } //else if (extULogout) {
    //handleServoMotion();
  //}
}
