#include "ArduinoUno.h"

dht11 DHT;
SoftwareSerial serial(2, 3);
#define DHT11_PIN A1

void ArduinoUno::initializeSerial(){
    serial.begin(9600);
}

int ArduinoUno::readTemperatureFromSensor(){
   DHT.read(DHT11_PIN); // Reading data received from DHT11 sensor
   return DHT.temperature;
}

int ArduinoUno::readHumidityFromSensor(){
   DHT.read(DHT11_PIN); // Reading data received from DHT11 sensor
   return DHT.humidity; // Reading just the humidity
}

void ArduinoUno::sendDataToESP8266(int currentTemperature, int humidity){
   String currentTemperatureString = String(currentTemperature);
   String humidityString = String(humidity);
   String data = currentTemperatureString + humidityString + humidityString.length();
   serial.println(data);
}

int ArduinoUno::readDesiredTemperatureFromESP8266(){
   String desiredTemperature = "";
   long int time = millis();
   while ((time + 20000) > millis()){
      while (serial.available()){
          char character = serial.read();
          desiredTemperature += character;
       }
    }
    return desiredTemperature.toInt();
}

void ArduinoUno::heatControl(int currentTemperature, int desiredTemperature){

   if(desiredTemperature != 0){
      if(currentTemperature < desiredTemperature){
          Serial.println("Centrala pornita");
          digitalWrite(7, HIGH);
      }
      else{
          Serial.println("Centrala oprita");
          digitalWrite(7, LOW);
      }
   }
}
