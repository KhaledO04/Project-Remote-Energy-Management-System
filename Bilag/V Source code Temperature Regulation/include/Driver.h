#ifndef ARDUINO_DRIVER_H
#define ARDUINO_DRIVER_H

#include <stdint.h>
#include <Arduino.h>

class ArduinoDriver {
    int port; // UART port number
    Stream* serial; // Serial object
    uint8_t bytes[17]; // Bytes hentet
public:
    ArduinoDriver(int port); // Constructor
    uint8_t calculateChecksum(uint8_t bytes[], int size); // Calculate checksum
    void read(); // Read data from UART port
    uint8_t* getBytes(); // Get the bytes read
    void sendSignal(char type, uint8_t bytes[], int roomId); // send and receive signal
    void resetBytes(); // Reset the bytes array
};


#endif // ARDUINO_DRIVER_H
