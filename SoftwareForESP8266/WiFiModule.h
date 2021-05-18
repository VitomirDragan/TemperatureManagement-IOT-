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

#define FIREBASE_HOST "temperaturemanagement-iot.firebaseio.com" // The path of the database
#define FIREBASE_AUTH "S7iqWxfvmFh67MJJBoWKlSBtJ2F1m8tFGv8sBBin" // Secret key for allowing the connection to database
#define RELAY_PIN D3
#define DHT11_PIN D0
#define INCREASE_TEMPERATURE_PIN D5
#define DECREASE_TEMPERATURE_PIN D6
#define TIME_TO_CONNECT 15000 // The maximum time allowed for WiFi module to connect to internet
#define MAX_TEMP 32 // Maximum temperature allowed to be set
#define MIN_TEMP 15 // Minimum temperature allowed to be set
#define ON 1 // Value of command for starting the heating
#define OFF 0 // Value of command for stopping the heating
#define PREVENT_TIMEOUT 2 // Value of command to prevent the heat cotrol module to timeout
#define HYSTERESIS 1 // Tolerance over the set temperature.

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
extern volatile boolean endOfInterval;

// Class which is dealing with time management
class TimeManager {
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

// Class that implements the functionalities of RF transmitter
class RFTransmitter {
private:
    TimeManager timer;
public:
    void initializeRFTransmitter();

    void sendCommandToController(int command);
};


// Class defined for DHT11 sensor
class DHTSensor {
public:
    int readHumidity();

    int readTemp();
};

// WiFiModule class implements functions realized by ESP8266 
class WiFiModule {
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

    void readStreamValue(volatile int &variable, FirebaseData &instance, String databaseField);

    int checkForUpdate(FirebaseData &instance, String databaseField);

    void heatControl(int currentTemperature);

    int readInt(String fieldName);

    String readStr(String fieldName);

    void statusIndicator();

    void defineInterrupts();
};

// Class used for mapping the LCD functionalities
class LCD {
public:
    void initializeLCD();

    void displayMessage(String message);

    void displayCurrentTemperature(int currentTemperature);

    void displayDesiredTemperature();
};


#endif
