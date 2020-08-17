#include "ArduinoUno.h"
ArduinoUno arduinoUno;

void setup() {
  Serial.begin(9600);
  pinMode(7, OUTPUT);
  arduinoUno.initializeSerial();
}

void loop(){
  int currentTemperature = arduinoUno.readTemperatureFromSensor();
  int humidity = arduinoUno.readHumidityFromSensor();
  arduinoUno.sendDataToESP8266(currentTemperature, humidity);
  delay(200);
  
  int desiredTemperature = arduinoUno.readDesiredTemperatureFromESP8266();
  delay(200);
  Serial.println(desiredTemperature);
  arduinoUno.heatControl(currentTemperature, desiredTemperature);
}
