#include <avr/io.h>
#include "I2C.h"

void I2C::init()
{
  // TWI prescaler = 1 (same as default)
  TWSR = 0;
  // LM75 clock has be to be lower than 400 kHz (according to LM75 data sheet)
  // We choose 2-wire clock ~ 216 kHz (when fCPU = 16 MHz)
  // The TWBR must be at least 10 in master mode (AVR data book)
  // SCL frequency = fCPU / (16 + 2*TWBR*1), when prescaler = 1
  TWBR = 29;
}

void I2C::start()
{
  TWCR = (1<<TWINT) | (1<<TWSTA) | (1<<TWEN); //Sætter TWI Control Register til at starte en I2C-startbetingelse. TWINT sættes for at rydde flaget, TWSTA for at sende startbetingelsen, og TWEN for at aktivere TWI.
  while ((TWCR & (1<<TWINT)) == 0) //Venter indtil startbetingelsen er sendt ved at tjekke TWINT-flaget.
  {}
}

void I2C::write(unsigned char data)
{
  TWDR = data; //Lægger dataen, der skal sendes, i TWI Data Register.
  TWCR = (1<<TWINT) | (1<<TWEN); //Sætter TWI Control Register til at starte en dataoverførsel. TWINT sættes for at rydde flaget, og TWEN for at aktivere TWI.
  while ((TWCR & (1<<TWINT)) == 0) //Venter indtil dataen er blevet sendt ved at tjekke TWINT-flaget.
  {}
}

unsigned char I2C::read (unsigned char isLast)
{
  // If this is not the last byte to read
  if (isLast == 0) // Hvis dette ikke er den sidste byte, der skal læses, sættes TWEA (TWI Enable Acknowledge Bit) for at sende en ACK efter modtagelse.
    TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWEA); //Starter en læsning og sender en ACK
  // If this is the last byte to read 	
  else //Hvis dette er den sidste byte, der skal læses, sendes en NACK efter modtagelse.
    TWCR = (1<<TWINT) | (1<<TWEN); //Starter en læsning uden at sende en ACK.
  while ((TWCR & (1<<TWINT)) == 0) //Venter indtil dataen er modtaget ved at tjekke TWINT-flaget.
  {}
  return TWDR;
}

void I2C::stop()
{
  TWCR = (1<<TWINT) | (1<<TWEN) | (1<<TWSTO); //TWINT sættes for at rydde flaget, TWEN for at aktivere TWI, og TWSTO for at sende stopbetingelsen.
}