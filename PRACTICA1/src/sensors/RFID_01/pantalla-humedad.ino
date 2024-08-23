#include <DHT.h>

#define DHTPIN 4 
#define DHTTYPE DHT11
 

DHT dht(DHTPIN,DHTTYPE);

void setup(){
    Serial.begin(9600);
    dht.begin();
}

void loop(){
    delay(5000);
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    float lectura = dht.readTemperature(true);
    if(isnan(humidity)||isnan(temperature)||isnan(lectura)){
        Serial.println("ERROR EN EL SENSOR ");
        return;
    }
    Serial.print("Humidity: ");
    Serial.print(humidity);
    Serial.print("% Temperature: ");
    Serial.println(temperature);
    Serial.println("°C");
}
