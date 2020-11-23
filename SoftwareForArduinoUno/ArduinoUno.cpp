#include "ArduinoUno.h"

dht11 DHT;
SoftwareSerial serial(2, 3);
#define DHT11_PIN A1
#define POT_PIN A2
#include <Wire.h>
#include <LiquidCrystal_I2C.h>


LiquidCrystal_I2C lcdInstance(0x27, 16, 2);

int Potentiometer::oldDesiredTemperaturePotentiometer = 0;
int ArduinoUno::oldDesiredTemperatureESP = 0;
int ArduinoUno::desiredTemperature = 0;

//Methods for ArduinoUno class
void ArduinoUno::pinSetup(){
   pinMode(7, OUTPUT);
   digitalWrite(7, HIGH);
}

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

void ArduinoUno::sendDataToESP8266(int currentTemperature, int humidity, int setTemperature, int flag){
   String currentTemperatureString = String(currentTemperature);
   String humidityString = String(humidity);
   String data = currentTemperatureString + humidityString + humidityString.length() + String(setTemperature) + String(flag);
   Serial.print("Data package: ");
   Serial.println(data);
   serial.println(data);
}

int ArduinoUno::readDesiredTemperatureFromESP8266(){
   String desiredTemperatureString = "";
   long int time = millis();
   while ((time + 12000) > millis()){
      while (serial.available()){
          char character = serial.read();
          desiredTemperatureString += character;
       }
    }
    int desiredTemperatureInt = desiredTemperatureString.toInt();
    Serial.println(desiredTemperatureInt);
    if(desiredTemperatureInt != 0){
      return desiredTemperatureInt;
    }
    else{
      return ArduinoUno::oldDesiredTemperatureESP;
    }
}

void ArduinoUno::heatControl(int currentTemperature){

   if(ArduinoUno::desiredTemperature != 0){
      if(currentTemperature < ArduinoUno::desiredTemperature){
          digitalWrite(7, LOW);
      }
      else{
          digitalWrite(7, HIGH);
      }
   }
}

int ArduinoUno::setDesiredTemperature(int newDesiredTemperatureESP, int newDesiredTemperaturePotentiometer){
  Serial.println(ArduinoUno::oldDesiredTemperatureESP);
  Serial.println(newDesiredTemperatureESP);
  Serial.println(Potentiometer::oldDesiredTemperaturePotentiometer);
  Serial.println(newDesiredTemperaturePotentiometer);
  if((ArduinoUno::oldDesiredTemperatureESP != newDesiredTemperatureESP) && (Potentiometer::oldDesiredTemperaturePotentiometer != newDesiredTemperaturePotentiometer)){
     ArduinoUno::oldDesiredTemperatureESP = newDesiredTemperatureESP;
     Potentiometer::oldDesiredTemperaturePotentiometer = newDesiredTemperaturePotentiometer;
     ArduinoUno::desiredTemperature = newDesiredTemperaturePotentiometer;
     Serial.println("Pot si App");
     return 1;
  }
  else
      if(ArduinoUno::oldDesiredTemperatureESP != newDesiredTemperatureESP){
        ArduinoUno::oldDesiredTemperatureESP = newDesiredTemperatureESP;
        ArduinoUno::desiredTemperature = newDesiredTemperatureESP;
        Serial.print("App: ");
        Serial.println(ArduinoUno::oldDesiredTemperatureESP);
        return 0;
      }
      else
          if(Potentiometer::oldDesiredTemperaturePotentiometer != newDesiredTemperaturePotentiometer){
            Potentiometer::oldDesiredTemperaturePotentiometer = newDesiredTemperaturePotentiometer;
            ArduinoUno::desiredTemperature = newDesiredTemperaturePotentiometer; 
            Serial.println("Pot");
            return 1;
          }
          else
              Serial.println("Nu se intra in if");
              return 0;
}

//Methods for LCD class
void LCD::initializeLCD(){
   lcdInstance.begin();
   lcdInstance.backlight();
}

void LCD::displayCurrentTemperature(int currentTemperature){
   lcdInstance.setCursor(0,0);
   lcdInstance.print("Curr. temp: ");
   lcdInstance.print(currentTemperature);
}

void LCD::displayDesiredTemperature(){
   char message[15];
   lcdInstance.setCursor(0,1);
   sprintf(message, "Des. temp: %-6d", ArduinoUno::desiredTemperature);
   lcdInstance.print(message);
}

//Methods for Potentiometer class
int Potentiometer::mapDataToTemperature(int data){
   return map(data, 0, 1023, 15, 32);
}

int Potentiometer::smoothing(){
  float total = 0;
  int samples = 2000;
  for(int i = 0; i < samples; i++){
    total += analogRead(POT_PIN);    
  }
  return int(floor(total/samples));
}

int Potentiometer::readDesiredTemperature(){
  int smth = smoothing();
  Serial.print("Smoothing: ");
  Serial.println(smth);
  return mapDataToTemperature(smth);
}
