#include "Heater.h"
#include <Arduino.h>

Heater::Heater(int id) : roomId{id}, heaterStatus{false}
{}

void Heater::setHeaterStatus(bool status)
{
    heaterStatus = status;
    if (heaterStatus == true){
        digitalWrite(13, HIGH);
    }
    else{
        digitalWrite(13, LOW);
    } 
    // Sæt pin til at være høj, hvis "setHeaterStatus" er true, og sættes til lav, hvis den er false
}