#include "WiFiModule.h"

WiFiModule wifiModule;
LCD lcd;
TimeManager timeManager;

FirebaseData streamDesiredTemperature;
FirebaseData streamSwitchIntervalsOn;
FirebaseData streamIntervals;


void setup() {
    lcd.initializeLCD();
    wifiModule.pinSetup();
    wifiModule.connectToInternet("Asus", "vitomir10");
    wifiModule.initializeRFTransmitter();
    timeManager.timeManagerConfig();
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
    wifiModule.defineInterrupts();
    wifiModule.stream(streamDesiredTemperature,"/DesiredTempRoom2/Zapier/Value");
    wifiModule.stream(streamSwitchIntervalsOn, "/SwitchIntervalsOn/Value");  
    wifiModule.stream(streamIntervals, "/Intervals");
}


void loop() {
  Serial.println("loop");
  if(increaseDesiredTemperature || decreaseDesiredTemperature){
    if(increaseDesiredTemperature){
      if(desiredTemperature < MAX_TEMP){
          desiredTemperature++;
          lcd.displayDesiredTemperature();
          if (WiFi.status() == WL_CONNECTED && (!switchIntervalsOn))
          {
              wifiModule.sendDesiredTemperatureToDatabase("DesiredTempRoom2/Zapier/Value");
          }
      }
      increaseDesiredTemperature = false;
    }else{
        if(desiredTemperature > MIN_TEMP){
          desiredTemperature--;
          lcd.displayDesiredTemperature();
          if (WiFi.status() == WL_CONNECTED && (!switchIntervalsOn))
          {
              wifiModule.sendDesiredTemperatureToDatabase("DesiredTempRoom2/Zapier/Value");
          }
        }
      decreaseDesiredTemperature = false;
    }
  }else{
    int currentTemperature = wifiModule.readTemperatureFromSensor();
    int humidity = wifiModule.readHumidityFromSensor();


    if (WiFi.status() == WL_CONNECTED) {
        wifiModule.sendCurrentTemperatureToDatabase(currentTemperature);
        wifiModule.sendHumidityToDatabase(humidity);
        wifiModule.readStreamValue(switchIntervalsOn, streamSwitchIntervalsOn, "SwitchIntervalsOn/Value");
        if (switchIntervalsOn) {
            int weekDay = timeManager.getWeekDay();
            int currentHour = timeManager.getCurrentHour();
            int currentMinute = timeManager.getCurrentMinute();
            if(wifiModule.checkForUpdate(streamIntervals, "/Intervals") || (!timeIntervalsOperatingMode))
            {
            if (weekDay == 6 || weekDay == 0) {
                String A = wifiModule.readStr("Intervals/Weekend/A");
                String B = wifiModule.readStr("Intervals/Weekend/B");

                int hourA = timeManager.getHourFromTimeFormat(A);
                int minuteA = timeManager.getMinuteFromTimeFormat(A);
                int hourB = timeManager.getHourFromTimeFormat(B);
                int minuteB = timeManager.getMinuteFromTimeFormat(B);

                if ((hourA < currentHour && currentHour < hourB) ||
                    (hourA == currentHour && currentMinute >= minuteA) ||
                    (hourB == currentHour && currentMinute < minuteB)) {
                      wifiModule.readDesiredTemperatureFromDatabase("Intervals/Weekend/TemperatureAB");
                      endHour = hourB;
                      endMinute = minuteB;
                } else {
                    wifiModule.readDesiredTemperatureFromDatabase("Intervals/Weekend/TemperatureBA");
                    endHour = hourA;
                    endMinute = minuteA;       
                }
            } else {
                String A = wifiModule.readStr("Intervals/WorkingDay/A");
                String B = wifiModule.readStr("Intervals/WorkingDay/B");
                String C = wifiModule.readStr("Intervals/WorkingDay/C");
                String D = wifiModule.readStr("Intervals/WorkingDay/D");

                int hourA = timeManager.getHourFromTimeFormat(A);
                int minuteA = timeManager.getMinuteFromTimeFormat(A);
                int hourB = timeManager.getHourFromTimeFormat(B);
                int minuteB = timeManager.getMinuteFromTimeFormat(B);
                int hourC = timeManager.getHourFromTimeFormat(C);
                int minuteC = timeManager.getMinuteFromTimeFormat(C);
                int hourD = timeManager.getHourFromTimeFormat(D);
                int minuteD = timeManager.getMinuteFromTimeFormat(D);


                if ((hourA < currentHour && currentHour < hourB) || 
                     (hourA == hourB && currentHour == hourA && currentMinute >= minuteA && currentMinute < minuteB)||
                    (hourA == currentHour && hourB != currentHour && currentMinute >= minuteA) ||
                    (hourA != currentHour && hourB == currentHour && currentMinute < minuteB)) {
                        wifiModule.readDesiredTemperatureFromDatabase("Intervals/WorkingDay/TemperatureAB");
                        endHour = hourB;
                        endMinute = minuteB;
                } else if ((hourB < currentHour && currentHour < hourC) || 
                     (hourB == hourC && currentHour == hourB && currentMinute >= minuteB && currentMinute < minuteC)||
                    (hourB == currentHour && hourC != currentHour && currentMinute >= minuteB) ||
                    (hourB != currentHour && hourC == currentHour && currentMinute < minuteC)){
                              wifiModule.readDesiredTemperatureFromDatabase("Intervals/WorkingDay/TemperatureBC");
                              endHour = hourC;
                              endMinute = minuteC;
                } else if ((hourC < currentHour && currentHour < hourD) || 
                     (hourC == hourD && currentHour == hourC && currentMinute >= minuteC && currentMinute < minuteD)||
                    (hourC == currentHour && hourD != currentHour && currentMinute >= minuteC) ||
                    (hourC != currentHour && hourD == currentHour && currentMinute < minuteD)) {
                              wifiModule.readDesiredTemperatureFromDatabase("Intervals/WorkingDay/TemperatureCD");
                              endHour = hourD;
                              endMinute = minuteD;
                } else {
                    wifiModule.readDesiredTemperatureFromDatabase("Intervals/WorkingDay/TemperatureDA");
                    endHour = hourA;
                    endMinute = minuteA;
                }
            }
                 timeIntervalsOperatingMode = true;
                 normalOperatingMode = false;
            }
            wifiModule.heatControl(currentTemperature); 
            if(endHour == currentHour && endMinute == currentMinute){
              timeIntervalsOperatingMode = false;
            }
        } else {
            wifiModule.readStreamValue(desiredTemperature, streamDesiredTemperature,"/DesiredTempRoom2/Zapier/Value");
            if(!normalOperatingMode){
               wifiModule.readDesiredTemperatureFromDatabase("DesiredTempRoom2/Zapier/Value");
               normalOperatingMode = true;
               timeIntervalsOperatingMode = false;
            }
            wifiModule.heatControl(currentTemperature);
        }
    } else {
        wifiModule.heatControl(currentTemperature);
        timeIntervalsOperatingMode = false;
        normalOperatingMode = false;
    }
     wifiModule.statusIndicator();
     lcd.displayDesiredTemperature();
     lcd.displayCurrentTemperature(currentTemperature);
  }
}
