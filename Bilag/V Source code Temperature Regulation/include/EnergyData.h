#pragma once


class EnergyData{
private:
double currentPrice;
double _1hPrice;
double _2hPrice;
double currentConsumption;
double meanConsumption;
int timeOfHour;

public:
EnergyData();
void setCurrentPrice(double price);
void set1hPrice(double price);
void set2hPrice(double price);
void setCurrentConsumption(double consumption);
void setMeanConsumption(double mean);
void setTimeOfHour(int time);
double getCurrentPrice();
double get1hPrice();
double get2hPrice();
double getCurrentConsumption();
double getMeanConsumption();
int getTimeOfHour();
};