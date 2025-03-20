#pragma once
#include "TempSensor.h"
#include "Heater.h"

class Room{
private:
    int roomId;
    TempSensor tempSensor;
    Heater heater;
    double currentTemp;
    double tempMarker1; 
    double tempMarker2;
    double goalTemp;
    
public:
    Room(int id);
    int getId();
    void updateTemp();
    double getCurrentTemp();
    double getTempMarker1();
    double getTempMarker2();
    double getGoalTemp();
    void setGoalTemp(double temp);
    void setTempMarker1(double temp);
    void setTempMarker2(double temp);
    void decomposeUint16Temp(uint8_t *MSB, uint8_t *LSB);
    void heatUpRoom();
    double calculateTemp(uint8_t MSB, uint8_t LSB);
    double deltaTemp();
};

class RoomArray {
    Room** array_{};
    int size_;
	int current_size;
	const int realloc_size;
public:
	RoomArray(int size);
	~RoomArray();
	void push_back(const Room &room);
    Room& getRoom(int roomId);
    int getId(int arrayPlace);
};