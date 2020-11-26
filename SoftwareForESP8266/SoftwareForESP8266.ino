#include "WiFiModule.h"
WiFiModule wifiModule; 


void setup()
{
  Serial.begin(9600);
  wifiModule.connectToInternet("Vitomir", "vitomir10");
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  //See https://github.com/nayarsystems/posix_tz_db/blob/master/zones.csv for Timezone codes for your region
  setenv("TZ", "EET-2EEST,M3.5.0/3,M10.5.0/4", 1);
}

String get_time(){
  time_t now;
  time(&now);
  char time_output[30];
  // See http://www.cplusplus.com/reference/ctime/strftime/ for strftime functions
  strftime(time_output, 30, "%T", localtime(&now)); 
  return String(time_output); // returns Sat 20-Apr-19 12:31:45
}


void loop()
{  
  int dataPackage = wifiModule.readDataFromArduino();
  if( dataPackage%10 == 1 )
    wifiModule.sendDesiredTemperatureToDatabase( wifiModule.readDesiredTemperatureFromArduino(dataPackage) );
  int switchIntervalsOn = wifiModule.readInt("SwitchIntervalsOn/Value");
  if(switchIntervalsOn)
  {
    String a = wifiModule.readStr("WorkingDay/A");
    String b = wifiModule.readStr("WorkingDay/B");
    String c = wifiModule.readStr("WorkingDay/C");
    String d = wifiModule.readStr("WorkingDay/D");
    String timeNow = get_time();
    if(a <= timeNow && timeNow <= b){
      wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureAB"));
    }
    else if(b < timeNow && timeNow <= c){
            wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureBC"));
         }
         else if(c < timeNow && timeNow <= d){
                wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureCD"));
              }
              else{
                    wifiModule.sendDesiredTemperatureToArduino(wifiModule.readInt("WorkingDay/TemperatureDA"));
                  }
    }
    else{
        wifiModule.sendDesiredTemperatureToArduino(wifiModule.readDesiredTemperatureFromDatabase());
    }
  wifiModule.sendTemperatureToDatabase( wifiModule.readTemperatureFromArduino(dataPackage) );
  wifiModule.sendHumidityToDatabase( wifiModule.readHumidityFromArduino(dataPackage) );
}
