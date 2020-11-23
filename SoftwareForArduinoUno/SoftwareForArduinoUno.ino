#include "ArduinoUno.h"
ArduinoUno arduinoUno;
LCD lcd;
Potentiometer potentiometer;

void setup() {
  Serial.begin(9600);
  arduinoUno.pinSetup();
  arduinoUno.initializeSerial();
  lcd.initializeLCD();
}

void loop(){
  int currentTemperature = arduinoUno.readTemperatureFromSensor();
  lcd.displayCurrentTemperature(currentTemperature);
  
  int humidity = arduinoUno.readHumidityFromSensor();
  
  int newDesiredTemperatureESP = arduinoUno.readDesiredTemperatureFromESP8266();
  int newDesiredTemperaturePotentiometer = potentiometer.readDesiredTemperature();
  int flag = arduinoUno.setDesiredTemperature(newDesiredTemperatureESP, newDesiredTemperaturePotentiometer);
  Serial.print("Desired temperature: ");
  Serial.println(ArduinoUno::desiredTemperature);
  arduinoUno.sendDataToESP8266(currentTemperature, humidity, ArduinoUno::desiredTemperature, flag);

  lcd.displayDesiredTemperature();
 // Serial.println(ArduinoUno::desiredTemperature);
  arduinoUno.heatControl(currentTemperature);
}
