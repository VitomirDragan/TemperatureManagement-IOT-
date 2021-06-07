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
#define RELAY_PIN D3 // Define the pin which connects to relay
#define DHT11_PIN D0 // Define the pin which connects to temperature and humidity sensor
#define INCREASE_TEMPERATURE_PIN D5 // Define the pin which connects to increase temperature button
#define DECREASE_TEMPERATURE_PIN D6 // Define the pin which connects to decrease temperature button
#define TIME_TO_CONNECT 15000 // The maximum time allowed for WiFi module to connect to internet
#define MAX_TEMP 32 // Maximum temperature allowed to be set
#define MIN_TEMP 15 // Minimum temperature allowed to be set
#define ON 1 // Value of command for starting the heating
#define OFF 0 // Value of command for stopping the heating
#define PREVENT_TIMEOUT 2 // Value of command to prevent the heat cotrol module to timeout
#define HYSTERESIS 1 // Tolerance over the set temperature.

extern volatile int desiredTemperature; // Stores the value of temperature that should be in the room 
extern volatile int lastHumidityValue; // Last value of humidity
extern volatile int lastTemperatureValue; // Last value of temperature
extern volatile int switchIntervalsOn; // Indicates the current operating mode of the sistem
extern volatile int endHour; // Indicates the hour when interval is ending
extern volatile int endMinute; // Indicates the minute when interval is ending
extern volatile boolean increaseDesiredTemperature; // Indicates that an interrupt was triggered by pressing the increase temperature button 
extern volatile boolean decreaseDesiredTemperature; // Indicates that an interrupt was triggered by pressing the decrease temperature button 
extern volatile boolean timeIntervalsOperatingMode; // Indicates if the automatic operating mode is ON or OFF
extern volatile boolean normalOperatingMode; // Indicates if the manual operating mode is ON or OFF
extern volatile boolean endOfInterval; // Indicates if the end of interval was reached or not

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
