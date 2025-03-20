#pragma once
#include <Wire.h>

class I2C{
public:
    void init();
    void start();
    void write(unsigned char data);
    unsigned char read (unsigned char isLast);
    void stop();
};