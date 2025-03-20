#include "TempSensor.h"
#include "I2C.h"

// Constants
#define LM75_BASE_ADDRESS 0b01001000
#define READ_MASK         0b00000001

TempSensor::TempSensor(int id) : roomId{id}, _16bitTemp{0}
{
}

// Reads the temperature register from specified sensor
// SensorAddress is between 0 and 7
void TempSensor::read()
{
    uint8_t highByte;
    uint8_t lowByte;
    uint16_t concatenatedValue = 0;

    i2c.start();
    i2c.write(((LM75_BASE_ADDRESS + 00000000)<<1) | READ_MASK); //same as 0b01001001 or 73dec
    // Read temperature high byte and ACK
    highByte = i2c.read(0);
    // Read temperature low byte and NACK
    lowByte = i2c.read(1);

    concatenatedValue = ((uint16_t)highByte << 8) | lowByte;

    i2c.stop();
    
    _16bitTemp=concatenatedValue;
}

uint16_t TempSensor::get16bitTemp()
{

    read();
    return _16bitTemp;
}