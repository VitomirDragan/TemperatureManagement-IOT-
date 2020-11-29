#include "WiFiModule.h"
#include <String.h>

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

int getCurrentHour() {
    tm *timeStruct = getPointerToTMStruct();
    return timeStruct->tm_hour;
}

int getCurrentMinute(){
    tm *timeStruct = getPointerToTMStruct();
    return timeStruct->tm_min;
}

int getHourFromTimeFormat(String timeFormat)
{
  return timeFormat.substring(0,timeFormat.indexOf(":")).toInt();
}

int getMinuteFromTimeFormat(String timeFormat)
{
  return timeFormat.substring(timeFormat.indexOf(":")+1).toInt();
}


void loop() {  
    int dataPackage = wifiModule.readDataFromArduino();
    if (dataPackage % 10 == 1)
        wifiModule.sendDesiredTemperatureToDatabase(wifiModule.readDesiredTemperatureFromArduino(dataPackage));
    int switchTimingOn = wifiModule.readInt("SwitchTimingOn/Value");
    if (switchTimingOn) {
        int weekDay = getWeekDay();
        int currentHour = getCurrentHour();
        int currentMinute = getCurrentMinute();

        if (weekDay == 6 || weekDay == 0) {
            String A = wifiModule.readStr("Weekend/A");
            String B = wifiModule.readStr("Weekend/B");
            
            int hourA = getHourFromTimeFormat(A);
            int minuteA = getMinuteFromTimeFormat(A);
            int hourB = getHourFromTimeFormat(B);
            int minuteB = getMinuteFromTimeFormat(B);

            if ((hourA < currentHour && currentHour < hourB) || (hourA==currentHour && currentMinute >= minuteA) || (hourB==currentHour && currentMinute < minuteB)) {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("Weekend/TemperatureAB"));
            } else {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("Weekend/TemperatureBA"));
            }

        } else {
            String A = wifiModule.readStr("WorkingDay/A");
            String B = wifiModule.readStr("WorkingDay/B");
            String C = wifiModule.readStr("WorkingDay/C");
            String D = wifiModule.readStr("WorkingDay/D");

            int hourA = getHourFromTimeFormat(A);
            int minuteA = getMinuteFromTimeFormat(A);
            int hourB = getHourFromTimeFormat(B);
            int minuteB = getMinuteFromTimeFormat(B);
            int hourC = getHourFromTimeFormat(C);
            int minuteC = getMinuteFromTimeFormat(C);
            int hourD = getHourFromTimeFormat(D);
            int minuteD = getMinuteFromTimeFormat(D);            

            if ((hourA < currentHour && currentHour < hourB) || (hourA==currentHour && currentMinute >= minuteA) || (hourB==currentHour && currentMinute < minuteB)) {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureAB"));
            } else if ((hourB < currentHour && currentHour < hourC) || (hourB==currentHour && currentMinute >= minuteB) || (hourC==currentHour && currentMinute < minuteC)) {
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureBC"));
            } else if ((hourC < currentHour && currentHour < hourD) || (hourC==currentHour && currentMinute >= minuteC) || (hourD==currentHour && currentMinute < minuteD)) {
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
