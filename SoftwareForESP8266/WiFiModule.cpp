#include "WiFiModule.h"

void WiFiModule::connectToInternet(String ssid, String password){
    WiFi.begin(ssid, password);
    Serial.print("Connecting...");
    while (WiFi.status() != WL_CONNECTED){
        delay(500);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("Connected, IP address: ");
    Serial.println(WiFi.localIP());
}

int WiFiModule::readDataFromArduino(){
    String dataPackageString = "";
    long int time = millis();
    while ((time + 20000) > millis()){
        while (Serial.available()){
            char character = Serial.read();
            dataPackageString += character;
        }
    }
    return dataPackageString.toInt();
}

int WiFiModule::readHumidityFromArduino(int dataPackage){
    int numberOfHumDigits = dataPackage % 10;
    dataPackage = dataPackage / 10;
    return dataPackage % int(pow(10, numberOfHumDigits));
}

int WiFiModule::readTemperatureFromArduino(int dataPackage){
    int numberOfHumDigits = dataPackage % 10;
    dataPackage = dataPackage / 10;
    return dataPackage / int(pow(10, numberOfHumDigits));
}

void WiFiModule::sendHumidityToDatabase(int humidity){
    Firebase.setInt("HumidityRoom2/Value", humidity);
}

void WiFiModule::sendTemperatureToDatabase(int currentTemperature){
    Firebase.setInt("CurrentTempRoom2/Value", currentTemperature);
}

int WiFiModule::readDesiredTemperatureFromDatabase(){
    return Firebase.getInt("DesiredTempRoom2/Value");
}

void WiFiModule::sendDesiredTemperatureToArduino(int desiredTemperature){
    Serial.println(desiredTemperature);
}
