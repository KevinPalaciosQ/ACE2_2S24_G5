// C++ code
//
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd_1(32, 16, 2);

void setup()
{
  pinMode(A0,INPUT);
  lcd_1.init();
  lcd_1.setCursor(0, 0);
  lcd_1.backlight();
  lcd_1.display();
}

void loop()
{
  lcd_1.setCursor(0, 0);
  lcd_1.print("GRUPO 5");
  delay(2000); // Wait for 2000 millisecond(s)
  lcd_1.setCursor(0, 1);
  lcd_1.print("ARQUI 2 ");
  delay(2000); // Wait for 2000 millisecond(s)
  lcd_1.clear();
  int pinFotorresistencia = analogRead(A0);
  if(pinFotorresistencia<969){
  	lcd_1.print("Hay luz");
    lcd_1.setCursor(0, 1);
    lcd_1.print(pinFotorresistencia);
  }else{
  lcd_1.print("No Hay luz");
  }
  delay(2000);
  lcd_1.clear();
}