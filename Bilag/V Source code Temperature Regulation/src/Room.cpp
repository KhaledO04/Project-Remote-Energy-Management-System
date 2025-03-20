#include "Room.h"
#include <stdio.h>
#include "Arduino.h"

Room::Room(int id) : roomId(id), tempSensor(id), heater(id), 
                   tempMarker1(19.0), tempMarker2(16.0), goalTemp(22.0){}

int Room::getId()
{
    return roomId;
}

void Room::updateTemp()
{
    Serial.write("Updating temp.\n\r");
    uint8_t high;
    uint8_t low;
    decomposeUint16Temp(&high, &low);

    currentTemp = calculateTemp(high, low);
    Serial.write("Temp updated.\n\r");
}

double Room::getCurrentTemp(){
    updateTemp();
    return currentTemp;
}

double Room::getTempMarker1()
{
    return tempMarker1;
}

double Room::getTempMarker2()
{
    return tempMarker2;
}

double Room::getGoalTemp()
{
    return goalTemp;
}

void Room::setGoalTemp(double temp)
{
    goalTemp = temp;
}

void Room::setTempMarker1(double temp)
{
    tempMarker1 = temp;
}

void Room::setTempMarker2(double temp)
{
    tempMarker2 = temp;
}

void Room::decomposeUint16Temp(uint8_t *MSB, uint8_t *LSB)
{
    uint16_t value = tempSensor.get16bitTemp(); // Get the 16-bit value
    *MSB = (value >> 8) & 0xFF; // Extract the high byte
    *LSB = value & 0xFF;         // Extract the low byte
}

double Room::calculateTemp(uint8_t MSB, uint8_t LSB)
{
    double decimal = 0.0;
    int sign = 1;
    //signed values:
    uint8_t msbMSB = MSB >> 7;
    uint8_t msbLSB = LSB >> 7;

    // Check if MSB is set (1)
    if (msbMSB) {
        sign = -1;
        MSB = ~MSB + 1; // 2's complement
    } 
    if (msbLSB){
        decimal = 0.5;
    }
    return sign*(MSB + decimal);
}

double Room::deltaTemp()
{
    return goalTemp - currentTemp;
}

void Room::heatUpRoom(){
    Serial.write("Heating up room...\n");
    heater.setHeaterStatus(true);
    while(deltaTemp()>0){
        //Foretager intet her. Venter blot på at temperaturen er OK.
    }
    heater.setHeaterStatus(false);
    Serial.write("Done heating up room.\n");
}

RoomArray::RoomArray(int size) : size_{ size }, current_size{ 0 }, realloc_size{ 2 }
//current_size is the current size of the array.
//realloc_size is the size that the array will be increased by when it is full.
{
	array_ = new Room*[size_];
}

RoomArray::~RoomArray()
{
    for (int i = 0; i < current_size; i++)
    {
	    delete array_[i];
    }

    delete[] array_;
}

void RoomArray::push_back(const Room &roomId)
{
    if (current_size == size_) //If array is filled up...
    {
        auto* tempArray{ new Room*[size_ + realloc_size] }; //New temporary array
        for (int i = 0; i < size_; i++)
        {
            tempArray[i] = array_[i]; //Copy elements from array_ to the new temp
        }
        size_ += realloc_size; //Update the size of the array
        delete[] array_; //Deallocate array_. This releases the address for all instances of the address
        //meaning that if there was a tempArray that array_ was pointing at, the address will still be released for tempArray as well.
        array_ = tempArray; //Point array_ to the new temp
    }
    array_[current_size++] = new Room(roomId);//Add a new room to the array
    }

Room& RoomArray::getRoom(int roomId) {
    for (int i = 0; i < current_size; i++) { //Searching for roomId room.
        if (array_[i]->getId() == roomId) { //Checking if ID==roomId
            return *array_[i]; // Return a reference to the Room object
        }
    }
    //return default room (0) if none are found.
    return *array_[0];
}

int RoomArray::getId(int arrayPlace) {
        return array_[arrayPlace]->getId();
}