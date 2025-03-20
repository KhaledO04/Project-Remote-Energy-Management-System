#pragma once
#include <stdint.h>
#include <wire.h>
#include "I2C.h"

class TempSensor{
private:
    int roomId;
    uint16_t _16bitTemp;
    I2C i2c;
public:
    TempSensor(int id);
    uint16_t get16bitTemp();
    void read();
};