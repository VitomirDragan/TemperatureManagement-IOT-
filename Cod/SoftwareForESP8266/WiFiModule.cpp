#include "WiFiModule.h"

dht11 DHT;
LiquidCrystal_I2C lcdInstance(0x27, 16, 2);
FirebaseData firebaseData;
RH_ASK driver(2000, D8, D7, D8);

volatile int desiredTemperature = 21;
volatile int lastHumidityValue = 0;
volatile int lastTemperatureValue = 0;
volatile int switchIntervalsOn = 0;
volatile int endHour = 0;
volatile int endMinute = 0;
volatile boolean increaseDesiredTemperature = false;
volatile boolean decreaseDesiredTemperature = false;
volatile boolean timeIntervalsOperatingMode = false;
volatile boolean normalOperatingMode = false;
volatile boolean endOfInterval = false;

ICACHE_RAM_ATTR void increaseTemperature() {
    /* This function is called when an interrupt occurs 
    after pressing the increase temperature button */
    increaseDesiredTemperature = true;
}

ICACHE_RAM_ATTR void decreaseTemperature() {
    /* This function is called when an interrupt occurs 
    after pressing the decrease temperature button */
    decreaseDesiredTemperature = true;
}

void TimeManager::timeManagerConfig() {
    configTime(0, 0, "pool.ntp.org", "time.nist.gov"); // Set server name
    setenv("TZ", "EET-2EEST,M3.5.0/3,M10.5.0/4", 1); // Set time zone
}

tm *TimeManager::getPointerToTMStruct() {
    time_t currentTime; // Declare variable for storing epoch current time 
    time(&currentTime); // Getting epoch current time
    return localtime(&currentTime); // Saving epoch current time in a tm structure
}

int TimeManager::getWeekDay() {
    return getPointerToTMStruct()->tm_wday; // Returning weekday(int value from 0 to 6, 0 - Sunday, 6 - Saturday)
}

int TimeManager::getCurrentHour() {
    return getPointerToTMStruct()->tm_hour; // Returning current hour
}

int TimeManager::getCurrentMinute() {
    return getPointerToTMStruct()->tm_min; // Returning current minute
}

int TimeManager::getCurrentSecond() {
    return getPointerToTMStruct()->tm_sec; // Returning current second
}

int TimeManager::getHourFromTimeFormat(String timeFormat) {
    return timeFormat.substring(0, timeFormat.indexOf(":")).toInt(); // Extract hour from string and convert it to int
}

int TimeManager::getMinuteFromTimeFormat(String timeFormat) {
    return timeFormat.substring(
            timeFormat.indexOf(":") + 1).toInt(); // Extract minute from string and convert it to int
}

void WiFiModule::defineInterrupts() {
    attachInterrupt(digitalPinToInterrupt(INCREASE_TEMPERATURE_PIN), increaseTemperature,
                    RISING); // Define interrupt for INCREASE_TEMPERATURE_PIN 
    attachInterrupt(digitalPinToInterrupt(DECREASE_TEMPERATURE_PIN), decreaseTemperature,
                    RISING); // Define interrupt for DECREASE_TEMPERATURE_PIN
}

int WiFiModule::readInt(String fieldName) {
    // Read integer stored in fieldName from database
    Firebase.getInt(firebaseData, fieldName);
    return firebaseData.intData();
}

String WiFiModule::readStr(String fieldName) {
    // Read string stored in fieldName from database
    Firebase.getString(firebaseData, fieldName);
    return firebaseData.stringData();
}

void WiFiModule::pinSetup() {
    // Set the mode for each pin used
    pinMode(RELAY_PIN, OUTPUT);
    pinMode(INCREASE_TEMPERATURE_PIN, INPUT);
    pinMode(DECREASE_TEMPERATURE_PIN, INPUT);
    pinMode(LED_BUILTIN, OUTPUT);
}

void WiFiModule::connectToInternet(String ssid, String password) {
    WiFi.begin(ssid, password); // Set credentials for the WiFi netwotk
    unsigned long startTime = millis(); // Save the time when WiFi module begins to establish a connection
    while (WiFi.status() != WL_CONNECTED) { // While connection is not established, execute the next instructions
        digitalWrite(LED_BUILTIN, HIGH); // Turn ON built in led
        delay(100); // Wait 100 miliseconds
        digitalWrite(LED_BUILTIN, LOW); // Turn OFF built in led
        delay(100); // Wait 100 miliseconds
        if ((millis() - startTime) > TIME_TO_CONNECT) {
            break; // If the time while trying to connect exceeded TIME_TO_CONNECT, then break the while loop
        }
    }
}


int DHTSensor::readHumidity() {
    DHT.read(DHT11_PIN); // Reading data received from DHT11 sensor
    return DHT.humidity; // Reading just the humidity
}


int DHTSensor::readTemp() {
    DHT.read(DHT11_PIN); // Reading data received from DHT11 sensor
    return DHT.temperature; // Reading just the temperature
}


void WiFiModule::sendHumidityToDatabase(int humidity) {
    if (lastHumidityValue != humidity) {
        // If the value of humidity was modified, save it in database
        if (Firebase.setInt(firebaseData, "HumidityRoom1/Value", humidity) == false) {
            return;
        }
        lastHumidityValue = humidity; // Save the new value of humidity
    }
}


void WiFiModule::sendCurrentTemperatureToDatabase(int currentTemperature) {
    if (lastTemperatureValue != currentTemperature) {
        // If the value of temperature was modified, save it in database
        if (Firebase.setInt(firebaseData, "CurrentTempRoom1/Value", currentTemperature) == false) {
            return;
        }
        lastTemperatureValue = currentTemperature; // Save the new value of temperature
    }
}


void WiFiModule::sendDesiredTemperatureToDatabase(String databaseField) {
    // Save the value of desiredTemperature in database
    if (Firebase.setInt(firebaseData, databaseField, desiredTemperature) == false) {
        return;
    }
}

void WiFiModule::readDesiredTemperatureFromDatabase(String databaseField) {
    int value = readInt(databaseField); // Read tempreature frim specifed field
    if (value >= MIN_TEMP && value <= MAX_TEMP) {
        desiredTemperature = readInt(databaseField); // Save the value read after verifying that is valid
    }
}


int WiFiModule::checkForUpdate(FirebaseData &instance, String databaseField) {
    if (Firebase.readStream(instance) == false) { // Read the stream of data from the specified path
        Serial.println("readStream failed");
    }
    if (instance.streamTimeout() == true) { // Verify if connection timed out
        Serial.println("Timeout check");
        stream(instance, databaseField); // Reestablish the connection 
    }
    if (instance.streamAvailable()) { // Check if there is data available
        return 1;
    }
    return 0;
}

void WiFiModule::readStreamValue(volatile int &variable, FirebaseData &instance, String databaseField) {
    if (checkForUpdate(instance, databaseField)) {
        // Read the data available from the stream
        variable = instance.intData();
    }
}

void WiFiModule::stream(FirebaseData &instance, String path) {
    // Connect to specified path of database and monitor for changes
    if (Firebase.beginStream(instance, path) == false) {
        return;
    }
}

void WiFiModule::heatControl(int currentTemperature) {
    if (currentTemperature <= (desiredTemperature - HYSTERESIS)) {
        digitalWrite(RELAY_PIN, LOW); // Open the solenoid valve
        transmitter.sendCommandToController(ON); // Send command to heat controller to start heating
    } else if (currentTemperature >= (desiredTemperature + HYSTERESIS)) {
        transmitter.sendCommandToController(OFF); // Send command to heat controller to stop heating
        digitalWrite(RELAY_PIN, HIGH); // Close the solenoid valve
    } else if (currentTemperature == desiredTemperature) {
        transmitter.sendCommandToController(PREVENT_TIMEOUT); // Prevent the heat controller to timeout
    }
}

void WiFiModule::statusIndicator() {
    if (WiFi.status() == WL_CONNECTED) // Verify if the module is connected to internet
        digitalWrite(LED_BUILTIN, LOW); // Turn ON the LED
    else
        digitalWrite(LED_BUILTIN, HIGH); // Turn OFF the LED
}

void RFTransmitter::initializeRFTransmitter() {
    // Start initialization of RF transmitter
    if (!driver.init())
        Serial.println("Initialization failed!");
}

void RFTransmitter::sendCommandToController(int command) {
    while (timer.getCurrentSecond() % 2 != 0) {
        delay(5);
    }// Wait while second is even

    char message[2];
    itoa(10 + command, message,
         10); // Form the message that will be sent to heat control module. Command can be 0-stop heating, 1-start heating or 2-prevent timeout. 
              //We add 10 to the command as a module identifier
    driver.send(((unsigned char *) message), strlen(message)); // Send the message
    driver.waitPacketSent(); // Wait for the message to be sent
}

//Methods for LCD class
void LCD::initializeLCD() {
    lcdInstance.begin(); // Call this function to set the dimensions of LCD
    lcdInstance.backlight(); // Turn ON the backlight
    displayMessage("Initializing...");
}

void LCD::displayMessage(String message) {
    lcdInstance.setCursor(0, 0); // Set cursor at the beginnig of the first row
    lcdInstance.print(message); // Print the message received as parameter
}

void LCD::displayCurrentTemperature(int currentTemperature) {
    char message[15];
    lcdInstance.setCursor(0, 0); // Set cursor at the beginnig of the first row
    sprintf(message, "Curr. temp: %-6d", currentTemperature); // Form the message to be displayed
    lcdInstance.print(message); // Print the message
}

void LCD::displayDesiredTemperature() {
    char message[15];
    lcdInstance.setCursor(0, 1); // Set the cursor at the beginning of the second row
    sprintf(message, "Des. temp: %-6d",
            desiredTemperature); // Form the message wich contains the value of the desired temperature
    lcdInstance.print(message); // Print the message on the LCD
}
