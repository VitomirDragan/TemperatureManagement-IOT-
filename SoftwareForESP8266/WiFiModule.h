#ifndef WIFIMODULE_H
#define WIFIMODULE_H

#include <stdlib.h>
#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include <FirebaseESP8266HTTPClient.h>
#include <FirebaseJson.h>
#include <time.h>
#include <dht11.h>
#include <LiquidCrystal_I2C.h>
#include <String.h>
#include <RH_ASK.h>
#include <SPI.h>

#define FIREBASE_HOST "temperaturemanagement-iot.firebaseio.com"
#define FIREBASE_AUTH "S7iqWxfvmFh67MJJBoWKlSBtJ2F1m8tFGv8sBBin"
#define RELAY_PIN D3
#define DHT11_PIN D0
#define INCREASE_TEMPERATURE_PIN D5
#define DECREASE_TEMPERATURE_PIN D6
#define TIME_TO_CONNECT 15000
#define MAX_TEMP 32
#define MIN_TEMP 15
#define ON 1
#define OFF 0
#define PREVENT_TIMEOUT 2
#define HYSTERESIS 1

extern volatile int desiredTemperature;
extern volatile int lastHumidityValue;
extern volatile int lastTemperatureValue;
extern volatile int lastDesiredTemperature;
extern volatile int switchIntervalsOn;
extern volatile int endHour;
extern volatile int endMinute;
extern volatile boolean increaseDesiredTemperature;
extern volatile boolean decreaseDesiredTemperature; 
extern volatile boolean timeIntervalsOperatingMode;
extern volatile boolean normalOperatingMode;
  

class TimeManager{
  public:
    void timeManagerConfig();
    tm *getPointerToTMStruct();
    int getWeekDay();
    int getCurrentHour();
    int getCurrentMinute();
    int getCurrentSecond();
    int getHourFromTimeFormat(String timeFormat);
    int getMinuteFromTimeFormat(String timeFormat);
};

class RFTransmitter{
  private:
    TimeManager timer;
  public:
    void initializeRFTransmitter();
    void sendCommandToController(int command);
};

class DHTSensor{
  public:
    int readHumidity();
    int readTemp(); 
};

class WiFiModule{
  private:
    RFTransmitter transmitter;
  public:
    void pinSetup();
    void connectToInternet(String ssid, String password);
    void sendHumidityToDatabase(int humidity);
    void sendCurrentTemperatureToDatabase(int currentTemperature);
    void sendDesiredTemperatureToDatabase(String databaseField);
    void readDesiredTemperatureFromDatabase(String databaseField);
    void stream(FirebaseData &instance, String path);
    void readStreamValue(volatile int & variable, FirebaseData &instance, String databaseField);
    int checkForUpdate(FirebaseData &instance, String databaseField);
    void heatControl(int currentTemperature);
    int readInt(String fieldName);
    String readStr(String fieldName);
    void statusIndicator();
    void defineInterrupts();
};

class LCD{
  public:
    void initializeLCD();
    void displayMessage(String message);
    void displayCurrentTemperature(int currentTemperature);
    void displayDesiredTemperature();
};


#endif
