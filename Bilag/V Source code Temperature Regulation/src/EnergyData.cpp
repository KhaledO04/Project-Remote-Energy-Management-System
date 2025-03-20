#include "EnergyData.h"

EnergyData::EnergyData() : currentPrice{300}, _1hPrice{200}, _2hPrice{100}, 
                            currentConsumption{100}, meanConsumption{0}, timeOfHour{0}
{}

void EnergyData::setCurrentPrice(double price)
{
    currentPrice = price;
}
void EnergyData::set1hPrice(double price){
    _1hPrice = price;
}
void EnergyData::set2hPrice(double price){
    _2hPrice = price;
}
void EnergyData::setCurrentConsumption(double consumption){
    currentConsumption = consumption;
}
void EnergyData::setMeanConsumption(double mean){
    meanConsumption = mean;
}
void EnergyData::setTimeOfHour(int time)
{
    timeOfHour = time;
}
double EnergyData::getCurrentPrice()
{
    return currentPrice;
}
double EnergyData::get1hPrice(){
    return _1hPrice;
}
double EnergyData::get2hPrice(){
    return _2hPrice;
}
double EnergyData::getCurrentConsumption(){
    return currentConsumption;
}
double EnergyData::getMeanConsumption(){
    return meanConsumption;
}
int EnergyData::getTimeOfHour(){
    return timeOfHour;
}
