#include "WiFiModule.h"

WiFiModule wifiModule;
LCD lcd;
TimeManager timeManager;



void updateTemperatureValue(String fieldName){  
    //wifiModule.sendDesiredTemperatureToDatabase(fieldName);
    wifiModule.readDesiredTemperatureFromDatabase(fieldName);
}

void setup() {
    lcd.initializeLCD();
    wifiModule.pinSetup();
    wifiModule.connectToInternet("Asus", "vitomir10");
    wifiModule.initializeRFTransmitter();
    timeManager.timeManagerConfig();
    Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
    wifiModule.defineInterrupts();
}


void loop() {
  Serial.println("loop");
  if(increaseDesiredTemperature || decreaseDesiredTemperature){
    if(increaseDesiredTemperature){
      if(desiredTemperature < MAX_TEMP){
          desiredTemperature++;
          lcd.displayDesiredTemperature();
          wifiModule.sendDesiredTemperatureToDatabase("DesiredTempRoom1/Zapier/Value");
      }
      increaseDesiredTemperature = false;
    }else{
        if(desiredTemperature > MIN_TEMP){
          desiredTemperature--;
          lcd.displayDesiredTemperature();
          wifiModule.sendDesiredTemperatureToDatabase("DesiredTempRoom1/Zapier/Value");
        }
      decreaseDesiredTemperature = false;
    }
  }else{
    int currentTemperature = wifiModule.readTemperatureFromSensor();
    int humidity = wifiModule.readHumidityFromSensor();


    if (WiFi.status() == WL_CONNECTED) {
        int switchIntervalsOn = wifiModule.readInt("SwitchIntervalsOn/Value");
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
                   updateTemperatureValue("Weekend/TemperatureAB");
                   wifiModule.heatControl(currentTemperature);
                } else {
                   updateTemperatureValue("Weekend/TemperatureBA");
                    wifiModule.heatControl(currentTemperature);
                 
                }

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
                    updateTemperatureValue("WorkingDay/TemperatureAB");
                    wifiModule.heatControl(currentTemperature);

                } else if ((hourB < currentHour && currentHour < hourC) ||
                           (hourB == currentHour && currentMinute >= minuteB) ||
                           (hourC == currentHour && currentMinute < minuteC)) {
                    updateTemperatureValue("WorkingDay/TemperatureBC");
                    wifiModule.heatControl(currentTemperature);
           
                } else if ((hourC < currentHour && currentHour < hourD) ||
                           (hourC == currentHour && currentMinute >= minuteC) ||
                           (hourD == currentHour && currentMinute < minuteD)) {
                    updateTemperatureValue("WorkingDay/TemperatureCD");
                    wifiModule.heatControl(currentTemperature);
                } else {
                    updateTemperatureValue("WorkingDay/TemperatureDA");
                    wifiModule.heatControl(currentTemperature);
                }
            }
        } else {
            updateTemperatureValue("DesiredTempRoom1/Zapier/Value");
            wifiModule.heatControl(currentTemperature);
        }
        wifiModule.sendCurrentTemperatureToDatabase(currentTemperature);
        wifiModule.sendHumidityToDatabase(humidity);
    } else {
        //Serial.print("Temp, offline:");
        //Serial.println(desiredTemperature);
        wifiModule.heatControl(currentTemperature);
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
