#include "WiFiModule.h"

WiFiModule wifiModule;


void setup() {
    Serial.begin(9600);
    wifiModule.connectToInternet("Vitomir", "vitomir10");
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);

    configTime(0, 0, "pool.ntp.org", "time.nist.gov");
    setenv("TZ", "EET-2EEST,M3.5.0/3,M10.5.0/4", 1);
}

tm *getPointerToTMStruct() {
    time_t currentTime; //declare variable for storing epoch current time 
    time(&currentTime); //getting epch current time
    return localtime(&currentTime); //saving epoch current time in a tm structure
}

int getWeekDay() {
    return getPointerToTMStruct()->tm_wday; //returning weekday(int value from 0 to 6, 0 - Sunday, 6 - Saturday)
}

String getCurrentTime() {
    tm *timeStruct = getPointerToTMStruct();
    return String(timeStruct->tm_hour) + ":" + String(timeStruct->tm_min); //returning current time(format hh:mm)
}


void loop() {
    int dataPackage = wifiModule.readDataFromArduino();
    if (dataPackage % 10 == 1)
        wifiModule.sendDesiredTemperatureToDatabase(wifiModule.readDesiredTemperatureFromArduino(dataPackage));
    int switchTimingOn = wifiModule.readInt("SwitchTimingOn/Value");
    if (switchTimingOn) {
        int weekDay = getWeekDay();
        String timeNow = getCurrentTime();

        if (weekDay == 6 || weekDay == 0) {
            String a = wifiModule.readStr("Weekend/A");
            String b = wifiModule.readStr("Weekend/B");

            if (a <= timeNow && timeNow < b) {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("Weekend/TemperatureAB"));
            } else {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("Weekend/TemperatureBA"));
            }

        } else {
            String a = wifiModule.readStr("WorkingDay/A");
            String b = wifiModule.readStr("WorkingDay/B");
            String c = wifiModule.readStr("WorkingDay/C");
            String d = wifiModule.readStr("WorkingDay/D");

            if (a <= timeNow && timeNow <= b) {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureAB"));
            } else if (b < timeNow && timeNow <= c) {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureBC"));
            } else if (c < timeNow && timeNow <= d) {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureCD"));
            } else {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureDA"));
            }
        }
    } else {
        wifiModule.sendDesiredTemperatureToArduino(wifiModule.readDesiredTemperatureFromDatabase());
    }
    wifiModule.sendTemperatureToDatabase(wifiModule.readTemperatureFromArduino(dataPackage));
    wifiModule.sendHumidityToDatabase(wifiModule.readHumidityFromArduino(dataPackage));
}
