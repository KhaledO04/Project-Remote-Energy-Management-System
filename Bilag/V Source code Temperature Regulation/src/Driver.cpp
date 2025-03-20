#include "Driver.h"
#include <stdint.h>
#include <Arduino.h>

#define startByte 0xFF
#define endByte 0xFE
#define errorByte 0xFD
#define typeByteR 0b01110010 //regulationSignal type = 114dec (fra 2560)
#define typeByteI 0b01110011 //initiateSignal type = 115dec (fra raspi)
#define typeByteT 0b01110100 //tempOut type = 116dec (Fra 2560)
#define typeByteD 0b01110101 //regulationData type = 117dec (fra raspi)
#define typeByteG 0b01110110 //regulationToggler type = 118dec (fra raspi) // BRUGES IKKE

ArduinoDriver::ArduinoDriver(int port) : port{port}
{
    if (port < 0 || port > 3)
    {
        port = 0; // If port is out of range, set it to 0
    }

    Stream* serialPorts[] = {&Serial, &Serial1, &Serial2, &Serial3};
    serial = serialPorts[port];
}

uint8_t ArduinoDriver::calculateChecksum(uint8_t bytes[], int size)
{
    uint8_t checksum = 0;
    for (int i = 0; i < size; i++) {
        checksum += bytes[i];
    }
    return checksum;
}

void ArduinoDriver::read()
{
    int size = 0; //array size counter

    while(serial->available() == 0) {
        Serial.write("Buffer empty... \r\n"); // Waiting for input
        delay(500);
    }
    
    uint8_t firstByte = serial->read(); // Read the first byte

    if(firstByte == startByte) {
        Serial.write("\nStartbyte found.\n\r"); //Write to computer port
        bytes[size] = firstByte; // Add startByte to the array
        size++;
    }
    else {
        Serial.write("Startbyte not found. Bytes read:\n\r"); //Write to computer port

        while (serial->available() > 0) {
            // read the incoming byte:
            int incomingByte = serial->read();

            //write bytes read to computer port
            Serial.println(incomingByte);
            if (incomingByte == endByte) {
                break;
            }
        }

        serial->write(errorByte); // Send error byte if startByte is not found
        return; // If startByte is not found, return
    }

    while (true) { // Loop until endByte is read
        // Read the incoming byte:
        bytes[size] = serial->read(); //add to array

        // debugging
        Serial.write("Byte nr: ");
        Serial.println(size);
        Serial.write("signal: ");
        Serial.println(bytes[size]);
        size++;

        if (bytes[size-1]==endByte) {
            break; // If endByte is read, break the loop
        }
    }

    if (bytes[1] == size-2) { //trækker 2 fra i fordi checksum og endByte ikke skal tælles med.
        Serial.write("Bytecount MATCH: "); // Write to computer port
        Serial.println(size-2); // Write to computer port
    }
    else {
        Serial.write("Error: Incorrect number of bytes read:\n\r"); // Write to computer port
        Serial.write("Received count: ");
        Serial.println(bytes[1]);
        Serial.write("Actual count: "); // Write to computer port
        Serial.println(size-2);
        serial->write(errorByte); // Send error byte if the number of bytes read is incorrect

        for(int i = 0; i <= size; i++) {
            bytes[i] = 0; // Reset the array
        }
        
        return; // If the number of bytes read is incorrect, return
    }

    int checksum = calculateChecksum(bytes, size-2); //trækker 2 fra i fordi checksum og endByte ikke skal tælles med

    if ( bytes[size-2]== checksum) { //trækker 2 fra i fordi checksum og endByte ikke skal tælles med.
        Serial.write("Checksum MATCH: "); // Write to computer port
        Serial.println(checksum); // Write to computer port
    }
    else {
        Serial.write("Error: Checksum MISMATCH:\n\r"); // Write to computer port
        Serial.write("Calculated checksum: ");
        Serial.println(checksum);
        Serial.write("Received checksum: "); // Write to computer port
        Serial.println(bytes[size-2]);
        serial->write(errorByte); // Send error byte if the number of bytes read is incorrect

        for(int i = 0; i <= size; i++) {
            bytes[i] = 0; // Reset the array
        }
        
        return; // If the number of bytes read is incorrect, return
    }
    Serial.write("\n\n");

}

uint8_t* ArduinoDriver::getBytes()
{
    return bytes;
}

void ArduinoDriver::sendSignal(char type, uint8_t bytes[], int roomId)
{
    uint8_t size;
    uint8_t count;
    uint8_t ID = static_cast<uint8_t>(roomId);
    int checksum;
    uint8_t array[8] = {0};
    if (type=='t'){
        size=2+6; //16 bit temperature. Der adderes 6 bytes for startByte, byteCount, type, roomId, checksum og endByte
        count = size-2; //trækker 2 fra size fordi checksum og endByte ikke skal tælles med
        // StartByte, ByteCount, Type, RoomId, Data, Checksum, EndByte
        uint8_t tempArray[] = {startByte, count, typeByteT, ID, bytes[0], bytes[1], 0x00, endByte};
        memcpy(array, tempArray, sizeof(tempArray)); //kopierer tempArray til array
    }
    else if (type=='r'){
        size=1+6; //Der adderes 6 bytes for startByte, byteCount, type, roomId, checksum og endByte
        count = size-2; //trækker 2 fra size fordi checksum og endByte ikke skal tælles med2
        uint8_t tempArray[] = {startByte, count, typeByteR, ID, bytes[0], 0x00, endByte, endByte};
        memcpy(array, tempArray, sizeof(tempArray)); //kopierer tempArray til array
    }
    else {
        Serial.write(errorByte);
    }

    checksum = calculateChecksum(array, size-2); //trækker 2 fra size fordi checksum og endByte ikke skal tælles med
    array[size - 2] = checksum; //der trækkes 2 fra size fordi checksum skal indsættes på den næstsidste plads i arrayet
    serial->write(array, size);
    serial->flush();
    Serial.write("\nSignal "); // Write to computer port
    Serial.write(type); // Write to computer port
    Serial.write(" sent.\n\r"); // Write to computer port
}

void ArduinoDriver::resetBytes()
{
    for (int i = 0; i < 17; i++)
    {
        bytes[i] = 0; // Reset the array
    }
}