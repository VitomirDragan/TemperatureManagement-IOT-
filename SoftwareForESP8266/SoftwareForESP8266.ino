#include "WiFiModule.h"
WiFiModule wifiModule; 

void setup()
{
  Serial.begin(9600);
  wifiModule.connectToInternet("Vitomir", "vitomir10");
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop()
{  
  int dataPackage = wifiModule.readDataFromArduino();
  if( dataPackage%10 == 1 )
    wifiModule.sendDesiredTemperatureToDatabase( wifiModule.readDesiredTemperatureFromArduino(dataPackage) );
  wifiModule.sendDesiredTemperatureToArduino( wifiModule.readDesiredTemperatureFromDatabase() );
  wifiModule.sendTemperatureToDatabase( wifiModule.readTemperatureFromArduino(dataPackage) );
  wifiModule.sendHumidityToDatabase( wifiModule.readHumidityFromArduino(dataPackage) );
}
