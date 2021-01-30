#include <RH_ASK.h>
#include <SPI.h> 

RH_ASK driver(2000, 4);

int commandModule1 = 0;
int commandModule2 = 0;

void setup()
{
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
  #ifdef RH_HAVE_SERIAL
      Serial.begin(9600);    // Debugging only
  #endif
      if (!driver.init())
  #ifdef RH_HAVE_SERIAL
      Serial.println("init failed");
  #else
    ;
#endif
}

void loop()
{
    unsigned char dataPackage[3];
    uint8_t dataPackageLength = sizeof(dataPackage);
    if (driver.recv(dataPackage, &dataPackageLength))
    {
        dataPackage[2] = '\0';
        Serial.println((char *) dataPackage);
        int dataPackageInt = atoi((char *) dataPackage);

        if((dataPackageInt/10) == 1){
            commandModule1 = dataPackageInt%10;
        }
        else{
            commandModule2 = dataPackageInt%10;
        }
        
        Serial.print("Module1:");
        Serial.println(commandModule1);
        Serial.print("Module2:");
        Serial.println(commandModule2);
        if(commandModule1 || commandModule2){
          digitalWrite(7, LOW);
          Serial.println("On");
        }else{
          digitalWrite(7, HIGH);
          Serial.println("Off");
        }
    }
}
