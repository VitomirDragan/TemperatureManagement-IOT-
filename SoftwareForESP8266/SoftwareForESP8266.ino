#include "WiFiModule.h"
WiFiModule wifiModule; 

void setup()
{
  Serial.begin(9600);
  wifiModule.connectToInternet("DIGI-7395", "XF3U8YMH");
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop()
{  
  int dataPackage = wifiModule.readDataFromArduino();
  
  wifiModule.sendHumidityToDatabase( wifiModule.readHumidityFromArduino(dataPackage) );
  wifiModule.sendTemperatureToDatabase( wifiModule.readTemperatureFromArduino(dataPackage) );
  wifiModule.sendDesiredTemperatureToArduino( wifiModule.readDesiredTemperatureFromDatabase() );

}
