#include "WiFiModule.h"

dht11 DHT;
LiquidCrystal_I2C lcdInstance(0x27, 16, 2);
FirebaseData firebaseData;
RH_ASK driver(2000, D8, D7, D8);

volatile int desiredTemperature = 21;
volatile boolean increaseDesiredTemperature = false;
volatile boolean decreaseDesiredTemperature = false;

ICACHE_RAM_ATTR void increaseTemperature() {
    Serial.println("intrerupere");
    increaseDesiredTemperature = true;
}

ICACHE_RAM_ATTR void decreaseTemperature() {
    Serial.println("intrerupere");
    decreaseDesiredTemperature = true;
}

void TimeManager::timeManagerConfig(){
    configTime(0, 0, "pool.ntp.org", "time.nist.gov");
    setenv("TZ", "EET-2EEST,M3.5.0/3,M10.5.0/4", 1);
}

tm* TimeManager::getPointerToTMStruct() {
    time_t currentTime; //declare variable for storing epoch current time 
    time(&currentTime); //getting epch current time
    return localtime(&currentTime); //saving epoch current time in a tm structure
}

int TimeManager::getWeekDay() {
    return getPointerToTMStruct()->tm_wday; //returning weekday(int value from 0 to 6, 0 - Sunday, 6 - Saturday)
}

int TimeManager::getCurrentHour() {
    return getPointerToTMStruct()->tm_hour;
}

int TimeManager::getCurrentMinute(){
    return getPointerToTMStruct()->tm_min;
}

int TimeManager::getCurrentSecond(){
    return getPointerToTMStruct()->tm_sec;
}

int TimeManager::getHourFromTimeFormat(String timeFormat)
{
  return timeFormat.substring(0,timeFormat.indexOf(":")).toInt();
}

int TimeManager::getMinuteFromTimeFormat(String timeFormat)
{
  return timeFormat.substring(timeFormat.indexOf(":")+1).toInt();
}

void WiFiModule::defineInterrupts(){
    attachInterrupt(digitalPinToInterrupt(INCREASE_TEMPERATURE_PIN), increaseTemperature, RISING);
    attachInterrupt(digitalPinToInterrupt(DECREASE_TEMPERATURE_PIN), decreaseTemperature, RISING);
}

int WiFiModule::readInt(String fieldName){
      Firebase.getInt(firebaseData, fieldName);
      return firebaseData.intData();
}

String WiFiModule::readStr(String fieldName){
    Firebase.getString(firebaseData, fieldName);
    return firebaseData.stringData();
}

void WiFiModule::pinSetup(){
     pinMode(RELAY_PIN, OUTPUT);
     pinMode(INCREASE_TEMPERATURE_PIN, INPUT);
     pinMode(DECREASE_TEMPERATURE_PIN, INPUT);
     pinMode(LED_BUILTIN, OUTPUT);
     digitalWrite(RELAY_PIN, HIGH);
}

void WiFiModule::connectToInternet(String ssid, String password){
    WiFi.begin(ssid, password);
    unsigned long startTime = millis();
    while (WiFi.status() != WL_CONNECTED){
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
        if( (millis() - startTime) > TIME_TO_CONNECT ){
            break;
        }
    }
}


int WiFiModule::readHumidityFromSensor(){
   DHT.read(DHT11_PIN); // Reading data received from DHT11 sensor
   return DHT.humidity; // Reading just the humidity
}


int WiFiModule::readTemperatureFromSensor(){
   DHT.read(DHT11_PIN); // Reading data received from DHT11 sensor
   return DHT.temperature; // Reading just the temperature
}


void WiFiModule::sendHumidityToDatabase(int humidity){
    Firebase.setInt(firebaseData, "HumidityRoom1/Value", humidity);
}


void WiFiModule::sendCurrentTemperatureToDatabase(int currentTemperature){
    Firebase.setInt(firebaseData, "CurrentTempRoom1/Value", currentTemperature);
}


void WiFiModule::sendDesiredTemperatureToDatabase(String databaseField){
    Firebase.setInt(firebaseData, databaseField, desiredTemperature);
}


void WiFiModule::readDesiredTemperatureFromDatabase(String databaseField){
//    detachInterrupt(digitalPinToInterrupt(INCREASE_TEMPERATURE_PIN));
//    detachInterrupt(digitalPinToInterrupt(DECREASE_TEMPERATURE_PIN));
    desiredTemperature = readInt(databaseField);
//    attachInterrupt(digitalPinToInterrupt(INCREASE_TEMPERATURE_PIN), increaseTemperature, RISING);
//    attachInterrupt(digitalPinToInterrupt(DECREASE_TEMPERATURE_PIN), decreaseTemperature, RISING);
    Serial.print("Db value: ");
    Serial.println(desiredTemperature);
}

void WiFiModule::heatControl(int currentTemperature){
     if(currentTemperature <= (desiredTemperature - HYSTERESIS)){
         digitalWrite(RELAY_PIN, LOW);
         sendCommandToController(ON);
     }
     else if(currentTemperature >= (desiredTemperature + HYSTERESIS)){
         sendCommandToController(OFF);
         digitalWrite(RELAY_PIN, HIGH);
     }
}


void WiFiModule::initializeRFTransmitter(){
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

void WiFiModule::sendCommandToController(int command){
      TimeManager timeManager;
      while(timeManager.getCurrentSecond()%2!=0){
        delay(5);
      }//wait while second is odd

      char message[2];
      itoa(10 + command, message, 10);
      driver.send(((unsigned char *) message), strlen(message));
      driver.waitPacketSent();
}

void WiFiModule::statusIndicator(){
      if(WiFi.status() == WL_CONNECTED)
         digitalWrite(LED_BUILTIN, LOW);
      else
         digitalWrite(LED_BUILTIN, HIGH);
}

//Methods for LCD class
void LCD::initializeLCD(){
   lcdInstance.begin();
   lcdInstance.backlight();
   displayMessage("Initializing...");
}

void LCD::displayMessage(String message){
   lcdInstance.setCursor(0,0);
   lcdInstance.print(message);
}

void LCD::displayCurrentTemperature(int currentTemperature){
   char message[15];
   lcdInstance.setCursor(0,0);
   sprintf(message, "Curr. temp: %-6d", currentTemperature);
   lcdInstance.print(message);
}

void LCD::displayDesiredTemperature(){
   char message[15];
   lcdInstance.setCursor(0,1);
   sprintf(message, "Des. temp: %-6d", desiredTemperature);
   lcdInstance.print(message);
}
