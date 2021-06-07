#include <RH_ASK.h>
#include <SPI.h>

#define TIMEOUT 5 // Number of seconds the connection between sensor modules and control module can be inactive
#define RELAY_PIN 7 // Define the pin that connects to relay
#define RECEIVER_PIN 4 // Define the pin that connects to receiver

RH_ASK receiver(2000, RECEIVER_PIN); // Set the speed of data transfer (2000 bits/second) and the RX pin

int commandModule1 = 0; // Initialize the variable which stores the command from the first sensor
int commandModule2 = 0; // Initialize the variable which stores the command from the second sensor
int timeFirstModuleSent = 0; // Initialize the variable which stores time when first module sent the last command
int timeSecondModuleSent = 0; // Initialize the variable which stores time when second module sent the last command

void setup() {
    pinMode(RELAY_PIN, OUTPUT); // Set the operation mode of the relay pin
    digitalWrite(RELAY_PIN, HIGH); // During initialization of the control module, the heating is turned off
    Serial.begin(9600);

    if (!receiver.init()) // Initialization of the communication
        Serial.println("Initialization failed!");
}

void loop() {
    unsigned char dataPackage[3];
    uint8_t dataPackageLength = sizeof(dataPackage); // Save the length of data package
    if (receiver.recv(dataPackage, &dataPackageLength)) {
        dataPackage[2] = '\0'; // Mark the end of the string
        int dataPackageInt = atoi((char *) dataPackage); // Convert the string to int

        if ((dataPackageInt / 10) == 1) { // Verify if the message was received from the first sensor module
            commandModule1 = dataPackageInt % 10; // Extract the value of command sent by the first sensor module
            timeFirstModuleSent = millis() / 1000; // Save the time when the command was received
        } else {
            commandModule2 = dataPackageInt % 10; // Extract the value of command sent by the second sensor module
            timeSecondModuleSent = millis() / 1000; // Save the time when the command was received
        }

        if (commandModule1 == 1 || commandModule2 == 1) {
            digitalWrite(7, LOW); // If both sensor modules send the ON command, the heating must be turned ON
        } else if (commandModule1 == 0 && commandModule2 == 0) {
            digitalWrite(7, HIGH); // If both sensor modules send the OFF command, the heating must be turned OFF
        }
    }

    // Treat situations in which timeout occurs 
    if ((((millis() / 1000) - timeFirstModuleSent) >= TIMEOUT &&
         ((millis() / 1000) - timeSecondModuleSent) >= TIMEOUT)) {
        digitalWrite(RELAY_PIN, HIGH); // If both sensor modules timed out, then the heating must be turned off
        commandModule1 = 0; // Set the command variable for first  module to 0
        commandModule2 = 0; // Set the command variable for second  module to 0
    } else if (((millis() / 1000) - timeFirstModuleSent) >= TIMEOUT && commandModule2 == 0) {
        digitalWrite(RELAY_PIN,
                     HIGH); // Turn off the heating if first module timed out and second module sent command to stop the heating
        commandModule1 = 0; // Set the command variable for first module to 0 
    } else if (((millis() / 1000) - timeSecondModuleSent) >= TIMEOUT && commandModule1 == 0) {
        digitalWrite(RELAY_PIN,
                     HIGH); // Turn off the heating if second module timed out and first module sent command to stop the heating
        commandModule2 = 0; // Set the command variable for second module to 0
    }
}
