#ifndef ARDUINOUNO_H
#define ARDUINOUNO_H

#include <SoftwareSerial.h>
#include <dht11.h>


class ArduinoUno{
public:
    static int oldDesiredTemperatureESP;
    static int desiredTemperature;
    void pinSetup();
    void initializeSerial();
    int readTemperatureFromSensor();
    int readHumidityFromSensor();
    void sendDataToESP8266(int currentTemperature, int humidity, int setTemperature, int flag);
    int readDesiredTemperatureFromESP8266();
    int setDesiredTemperature(int newDesiredTemperatureESP, int newDesiredTemperaturePotentiometer);
    void heatControl(int currentTemperature);
};

class LCD{
  public:
    void initializeLCD();
    void displayCurrentTemperature(int currentTemperature);
    void displayDesiredTemperature();
};

class Potentiometer{
  private:
    int mapDataToTemperature(int data);
  public:
    static int oldDesiredTemperaturePotentiometer;
    int smoothing();
    int readDesiredTemperature();
};
#endif
