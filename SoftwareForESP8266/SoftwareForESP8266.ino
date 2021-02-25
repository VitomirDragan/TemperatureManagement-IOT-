#include "WiFiModule.h"

WiFiModule wifiModule;
LCD lcd;
TimeManager timeManager;

FirebaseData streamDesiredTemperature;
FirebaseData streamSwitchIntervalsOn;


void updateTemperatureValue(String fieldName){  
    //wifiModule.sendDesiredTemperatureToDatabase(fieldName);

}

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
}


void loop() {
  Serial.println("loop");
  if(increaseDesiredTemperature || decreaseDesiredTemperature){
    if(increaseDesiredTemperature){
      if(desiredTemperature < MAX_TEMP){
          desiredTemperature++;
          lcd.displayDesiredTemperature();
          if (WiFi.status() == WL_CONNECTED)
          {
              wifiModule.sendDesiredTemperatureToDatabase("DesiredTempRoom2/Zapier/Value");
          }
      }
      increaseDesiredTemperature = false;
    }else{
        if(desiredTemperature > MIN_TEMP){
          desiredTemperature--;
          lcd.displayDesiredTemperature();
          if (WiFi.status() == WL_CONNECTED)
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
        wifiModule.checkForUpdate(switchIntervalsOn, streamSwitchIntervalsOn, "SwitchIntervalsOn/Value");
        //Serial.print("temp online:");
        //Serial.println(desiredTemperature);
        if (switchIntervalsOn) {
            int weekDay = timeManager.getWeekDay();
            int currentHour = timeManager.getCurrentHour();
            int currentMinute = timeManager.getCurrentMinute();

            if (weekDay == 6 || weekDay == 0) {
                String A = wifiModule.readStr("Weekend/A");
                String B = wifiModule.readStr("Weekend/B");

                int hourA = timeManager.getHourFromTimeFormat(A);
                int minuteA = timeManager.getMinuteFromTimeFormat(A);
                int hourB = timeManager.getHourFromTimeFormat(B);
                int minuteB = timeManager.getMinuteFromTimeFormat(B);

                if ((hourA < currentHour && currentHour < hourB) ||
                    (hourA == currentHour && currentMinute >= minuteA) ||
                    (hourB == currentHour && currentMinute < minuteB)) {
                      wifiModule.readDesiredTemperatureFromDatabase("Weekend/TemperatureAB");
//                      wifiModule.heatControl(currentTemperature);
                } else {
                    wifiModule.readDesiredTemperatureFromDatabase("Weekend/TemperatureBA");
//                    wifiModule.heatControl(currentTemperature);
                 
                }
              wifiModule.heatControl(currentTemperature); 
            } else {
                String A = wifiModule.readStr("WorkingDay/A");
                String B = wifiModule.readStr("WorkingDay/B");
                String C = wifiModule.readStr("WorkingDay/C");
                String D = wifiModule.readStr("WorkingDay/D");

                int hourA = timeManager.getHourFromTimeFormat(A);
                int minuteA = timeManager.getMinuteFromTimeFormat(A);
                int hourB = timeManager.getHourFromTimeFormat(B);
                int minuteB = timeManager.getMinuteFromTimeFormat(B);
                int hourC = timeManager.getHourFromTimeFormat(C);
                int minuteC = timeManager.getMinuteFromTimeFormat(C);
                int hourD = timeManager.getHourFromTimeFormat(D);
                int minuteD = timeManager.getMinuteFromTimeFormat(D);

                if ((hourA < currentHour && currentHour < hourB) ||
                    (hourA == currentHour && currentMinute >= minuteA) ||
                    (hourB == currentHour && currentMinute < minuteB)) {
                        wifiModule.readDesiredTemperatureFromDatabase("WorkingDay/TemperatureAB");
//                        wifiModule.heatControl(currentTemperature);

                } else if ((hourB < currentHour && currentHour < hourC) ||
                           (hourB == currentHour && currentMinute >= minuteB) ||
                           (hourC == currentHour && currentMinute < minuteC)) {
                              wifiModule.readDesiredTemperatureFromDatabase("WorkingDay/TemperatureBC");
//                              wifiModule.heatControl(currentTemperature);
                } else if ((hourC < currentHour && currentHour < hourD) ||
                           (hourC == currentHour && currentMinute >= minuteC) ||
                           (hourD == currentHour && currentMinute < minuteD)) {
                              wifiModule.readDesiredTemperatureFromDatabase("WorkingDay/TemperatureCD");
//                              wifiModule.heatControl(currentTemperature);
                } else {
                    wifiModule.readDesiredTemperatureFromDatabase("WorkingDay/TemperatureDA");
//                    wifiModule.heatControl(currentTemperature);
                }
                 wifiModule.heatControl(currentTemperature);
            }
            operatingModeChanged = true;
        } else {
            wifiModule.checkForUpdate(desiredTemperature, streamDesiredTemperature,"/DesiredTempRoom2/Zapier/Value");
            if(operatingModeChanged){
               wifiModule.readDesiredTemperatureFromDatabase("DesiredTempRoom2/Zapier/Value");
               operatingModeChanged = false;
            }
            wifiModule.heatControl(currentTemperature);
        }
    } else {
        //Serial.print("Temp, offline:");
        //Serial.println(desiredTemperature);
        wifiModule.heatControl(currentTemperature);
        operatingModeChanged = true;
    }
     wifiModule.statusIndicator();
     //detachInterrupt(digitalPinToInterrupt(INCREASE_TEMPERATURE_PIN));
     //detachInterrupt(digitalPinToInterrupt(DECREASE_TEMPERATURE_PIN));  
     lcd.displayDesiredTemperature();
     lcd.displayCurrentTemperature(currentTemperature);
     //attachInterrupt(digitalPinToInterrupt(INCREASE_TEMPERATURE_PIN), increaseTemperature, RISING);
     //attachInterrupt(digitalPinToInterrupt(DECREASE_TEMPERATURE_PIN), decreaseTemperature, RISING);
  }
}
