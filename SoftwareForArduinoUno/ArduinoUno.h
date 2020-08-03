#ifndef ARDUINOUNO_H
#define ARDUINOUNO_H

#include <SoftwareSerial.h>
#include <dht11.h>

class ArduinoUno{
public:
    void initializeSerial();
    int readTemperatureFromSensor();
    int readHumidityFromSensor();
    void sendDataToESP8266(int currentTemperature, int humidity);
    int readDesiredTemperatureFromESP8266();
    void heatControl(int currentTemperature, int desiredTemperature);
};

#endif
