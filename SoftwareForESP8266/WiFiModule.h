#ifndef WIFIMODULE_H
#define WIFIMODULE_H

//#include <Firebase.h>
//#include <FirebaseArduino.h>
//#include <FirebaseCloudMessaging.h>
//#include <FirebaseError.h>
//#include <FirebaseHttpClient.h>
//#include <FirebaseObject.h>
//#include <ArduinoJson.h>
//#include <ESP8266WiFi.h>
//#include <String.h>
//#include <time.h>
//#include "FirebaseESP8266.h"

#include <FirebaseESP8266.h>
#include <FirebaseESP8266HTTPClient.h>
#include <FirebaseJson.h>
#include <time.h>



#include <ESP8266WiFi.h>

#define FIREBASE_HOST "temperaturemanagement-iot.firebaseio.com"
#define FIREBASE_AUTH "S7iqWxfvmFh67MJJBoWKlSBtJ2F1m8tFGv8sBBin"



class WiFiModule{
  public:
    void connectToInternet(String ssid, String password);
    int readDataFromArduino();
    int readHumidityFromArduino(int dataPackage);
    int readTemperatureFromArduino(int dataPackage);
    int readDesiredTemperatureFromArduino(int dataPackage);
    void sendHumidityToDatabase(int humidity);
    void sendTemperatureToDatabase(int currentTemperature);
    void sendDesiredTemperatureToDatabase(int setTemperature);
    int readDesiredTemperatureFromDatabase();
    void sendDesiredTemperatureToArduino(int desiredTemperature);
    int readInt(String fieldName);
    String readStr(String fieldName);
};

#endif
