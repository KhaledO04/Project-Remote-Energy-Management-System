#pragma once
#include <Arduino.h>
#include "Room.h"
#include "EnergyData.h"
#include "Driver.h"

class LavTemperatur {
private:
    double priceCap;
    EnergyData energyData;
    RoomArray rooms;
    ArduinoDriver driver;
    uint8_t tempBytes[2];

public:
    LavTemperatur(double priceCap);
    void regulateTemp(int roomId);
    void tempOutInitIn(int roomId);
    void regulateOutDataIn(bool regulating, int roomId);
    void addRoom(int roomId);
    void waitUntill(uint8_t hours);
    double getPriceCap();
    Room& getRoom(int roomId);
    
};
