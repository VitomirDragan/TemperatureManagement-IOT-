#include "WiFiModule.h"


FirebaseData firebaseData;
int WiFiModule::readInt(String fieldName){
    Firebase.getInt(firebaseData, fieldName);
    return firebaseData.intData();
}

String WiFiModule::readStr(String fieldName){
    Firebase.getString(firebaseData, fieldName);
    return firebaseData.stringData();
}


void WiFiModule::connectToInternet(String ssid, String password){
    WiFi.begin(ssid, password);
    Serial.print("Connecting...");
    while (WiFi.status() != WL_CONNECTED){
        delay(200);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("Connected, IP address: ");
    Serial.println(WiFi.localIP());
}

int WiFiModule::readDataFromArduino(){
    String dataPackageString = "";
    long int time = millis();
    while ((time + 3000) > millis()){
        while (Serial.available()){
            char character = Serial.read();
            dataPackageString += character;
        }
    }
    return dataPackageString.toInt();
}

int WiFiModule::readHumidityFromArduino(int dataPackage){
    int numberOfHumDigits = (dataPackage/1000) % 10;
    dataPackage = (dataPackage/1000) / 10;
    return dataPackage % int(pow(10, numberOfHumDigits));
}

int WiFiModule::readTemperatureFromArduino(int dataPackage){
    int numberOfHumDigits = (dataPackage/1000) % 10;
    dataPackage = (dataPackage/1000) / 10;
    return dataPackage / int(pow(10, numberOfHumDigits));
}

int WiFiModule::readDesiredTemperatureFromArduino(int dataPackage){
    return (dataPackage/10) % 100;
}
void WiFiModule::sendHumidityToDatabase(int humidity){
    Firebase.setInt(firebaseData, "HumidityRoom2/Value", humidity);
}

void WiFiModule::sendTemperatureToDatabase(int currentTemperature){
    Firebase.setInt(firebaseData, "CurrentTempRoom2/Value", currentTemperature);
}

void WiFiModule::sendDesiredTemperatureToDatabase(int setTemperature){
    Firebase.setInt(firebaseData, "DesiredTempRoom2/Value", setTemperature);
}

int WiFiModule::readDesiredTemperatureFromDatabase(){
    return readInt("DesiredTempRoom2/Value");
}

void WiFiModule::sendDesiredTemperatureToArduino(int desiredTemperature){
    Serial.println(desiredTemperature);
}
