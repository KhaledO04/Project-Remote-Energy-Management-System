#pragma once

class Heater{
private:
    int roomId;
    bool heaterStatus;
public:
    Heater(int id);
    void setHeaterStatus(bool status);
};