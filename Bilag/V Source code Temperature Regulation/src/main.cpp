#include "LavTemperatur.h"
#include "Heater.h"
#include "TempSensor.h"
#include "Room.h"
#include "Driver.h"
#include "EnergyData.h"
#include "I2C.h"
#define BAUD_RATE 19200

void setup() {
  // initialize both serial ports:
  Serial.begin(BAUD_RATE);
  Serial1.begin(BAUD_RATE);
  Serial2.begin(BAUD_RATE); 
  Serial3.begin(BAUD_RATE);
  I2C i2c;
  i2c.init();
  pinMode(13, OUTPUT);
}
  bool complete = false;
  LavTemperatur controller(0.2);
  double currentTemp = 0;

void loop() {
  controller.addRoom(7);
  currentTemp = controller.getRoom(7).getCurrentTemp();
  Serial.print("Current Temp: ");
  Serial.println(currentTemp);

  while (!complete) {
    controller.regulateTemp(7);
    delay(120E3); // Vent 2 minutter
  }

  delay(5000);
  controller.getRoom(7).updateTemp();
  currentTemp = controller.getRoom(7).getCurrentTemp();
  Serial.print("Current Temp: ");
  Serial.println(currentTemp);

  return;
}