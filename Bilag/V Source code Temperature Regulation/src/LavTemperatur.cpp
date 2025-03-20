
#include "LavTemperatur.h"

#define typeByteT 0b01110100 //tempOut type = 116dec (Fra 2560)
#define typeByteR 0b01110010 //regulationSignal type = 114dec (fra 2560)
#define typeByteI 0b01110011 //initiateSignal type = 115dec (fra raspi)
#define typeByteD 0b01110101 //regulationData type = 117dec (fra raspi)
#define typeByteG 0b01110110 //regulationToggler type = 118dec (fra raspi)

//constructor

LavTemperatur::LavTemperatur(double priceCap) : priceCap{priceCap}, energyData{EnergyData()}, 
                                                rooms{RoomArray(3)}, driver{1}, tempBytes{0}
{}

void LavTemperatur::regulateTemp(int roomId)
{
    Serial.write("\nRegulating temperature...\n\r");
    Room &room = rooms.getRoom(roomId);
    double deltaTemp;
    double currentTemp;
    while (true)
    {              
        room.updateTemp();                       // Update temp                           
        tempOutInitIn(roomId); // Measure temp // send to hub
        deltaTemp = room.deltaTemp();         // Compare temp
        currentTemp = room.getCurrentTemp();
        Serial.write("Delta Temp: ");
        Serial.println(deltaTemp);
        Serial.print("Current Temp: ");
        Serial.println(currentTemp);
        if (deltaTemp > 0.00)
        {
            break;
        }
        delay(120E3); // Wait 2 minutes
    }

    /*****TEMP TOO LOW*****/
    // Her sendes et reguleringssignal til hub
    Serial.write("\nTemp too low.\n\r");
    regulateOutDataIn(true, roomId);

    double currentPrice = energyData.getCurrentPrice();
    double goalTemp = room.getGoalTemp();
    double tempMarker1 = room.getTempMarker1();
    double tempMarker2 = room.getTempMarker2();
    uint8_t regulatingByte = 0;

    // Price OK? : YES
    if (currentPrice <= priceCap)
    {
        Serial.write("Price OK.\n\r");
        room.heatUpRoom();
        driver.sendSignal('r', 0, roomId); // Regulation: OFF
        return;
    }
    // Price OK? : NO
    Serial.write("Price NOT OK.\n\r");
    if (deltaTemp <= goalTemp-tempMarker1)
    {
        Serial.write("deltaTemp<=tempMarker1\n\r");
        driver.sendSignal('r', &regulatingByte, roomId); // Regulation: OFF
        return;
    }                                                                 // deltaTemp<=tmarker1
    else if ((deltaTemp > goalTemp-tempMarker1) && (deltaTemp <= goalTemp-tempMarker2)) // tmarker1<deltaTemp<=tmarker2?
    {
        Serial.write("deltaTemp>tmarker1 && deltaTemp<=tmarker2\n\r");
        // Consumption<mean? : YES
        if (energyData.getCurrentConsumption() < energyData.getMeanConsumption())
        {
            Serial.write("Consumption<mean\n\r");
            room.heatUpRoom();
            driver.sendSignal('r', &regulatingByte, roomId); // Regulation: OFF
            return;
        }
        // Consumption<mean? : NO
        else
        {
            Serial.write("Consumption>mean\n\r");
            // Fortsætter til næste del af koden som svarer til deltaTemp>tmarker2
        }
    }
    // deltaTemp>tmarker2
    double _1hrPrice = energyData.get1hPrice();
    double _2hrPrice = energyData.get2hPrice();

    // Price(t) is lowest
    if (currentPrice <= _1hrPrice && currentPrice <= _2hrPrice)
    {
        Serial.write("Price(t) is lowest\n\r");
        room.heatUpRoom();
        driver.sendSignal('r', &regulatingByte, roomId); // Regulation: OFF
        return;
    }

    // Price(t+1h) is lowest
    else if (_1hrPrice <= currentPrice && _1hrPrice <= _2hrPrice)
    {
        Serial.write("Price(t+1h) is lowest.\n\r");
        waitUntill(1);
        room.heatUpRoom();
        driver.sendSignal('r', &regulatingByte, roomId); // Regulation: OFF
        return;
    }

    // Price(t+2h) is lowest
    else
    {
        Serial.write("Price(t+2h) is lowest\n\r");
        waitUntill(2);
        room.heatUpRoom();
        driver.sendSignal('r', &regulatingByte, roomId); // Regulation: OFF
        return;
    }
}    

void LavTemperatur:: tempOutInitIn(int roomId){
    /*****TEMP OUT*****/
    Room &room = rooms.getRoom(roomId);
    //uint8_t tempBytes[2];
    room.decomposeUint16Temp(&tempBytes[0], &tempBytes[1]);
    driver.sendSignal('t', tempBytes, roomId);
    
    delay(1000);//venter 1 sekund

    /*****INITIATION IN*****/
    Serial.write("Getting initiateSignal... \r\n");
    driver.read();
    uint8_t typeByte = driver.getBytes()[2]; // Get typeByte
    if (typeByte == typeByteI) {
        Serial.write("Received: initiate signal.\n\r");
    }
    else if (typeByte == typeByteD) {
        Serial.write("Error: Received: regulationData signal.\n\r");
        return;
    }
    else if(typeByte == typeByteG) {
        Serial.write("Error: Received: regulationToggler signal.\n\r");
        return;
    }
    else {
        Serial.write("Incorrect type: "); // Write to computer port
        Serial.println(typeByte);
        return; // If type is incorrect, return
    }

    if (driver.getBytes()[3] != roomId) {
        Serial.write("Error: Incorrect roomId: "); // Write to computer port
        Serial.println(driver.getBytes()[3]);
        Serial.write("Expected: "); // Write to computer port
        Serial.println(roomId);
        return; // If roomId is incorrect, return
    }
    Serial.write("Correct roomId.\n\r"); // Write to computer port
    priceCap = driver.getBytes()[4]+0.01*driver.getBytes()[5]; // Update priceCap
    room.setGoalTemp(room.calculateTemp(driver.getBytes()[6], driver.getBytes()[7])); // Update goalTemp
    room.setTempMarker1(room.calculateTemp(driver.getBytes()[8], driver.getBytes()[9])); // Update tempMarker1
    room.setTempMarker2(room.calculateTemp(driver.getBytes()[10], driver.getBytes()[11])); // Update tempMarker2
    Serial.write("Initiation data updated.\n\r"); // Write to computer port

    // Print data
    Serial.print("Price Cap: ");
    Serial.println(priceCap);
    Serial.print("Goal Temp: ");
    Serial.println(room.getGoalTemp());
    Serial.print("Temp Marker 1: ");
    Serial.println(room.getTempMarker1());
    Serial.print("Temp Marker 2: ");
    Serial.println(room.getTempMarker2());
    Serial.write("\n\n");

    driver.resetBytes(); // Reset the bytes array

}

void LavTemperatur::regulateOutDataIn(bool regulating, int roomId)
{
    /*****REGULATE OUT*****/
    uint8_t regulatingByte = regulating ? 1 : 0;
    driver.sendSignal('r', &regulatingByte, roomId);

    delay(1000);//venter 1 sekund

    /*****DATA IN*****/
    Serial.write("Getting regulationData signal... \r\n");
    driver.read();
    uint8_t typeByte = driver.getBytes()[2]; // Get typeByte
    if (typeByte == typeByteD) {
        Serial.write("Received: regulationData signal.\n\r");
    }
    else if (typeByte == typeByteI) {
        Serial.write("Error: Received: initiateSignal signal.\n\r");
        return;
    }
    else if(typeByte == typeByteG) {
        Serial.write("Error: Received: regulationToggler signal.\n\r");
        return;
    }
    else {
        Serial.write("Incorrect type: "); // Write to computer port
        Serial.println(typeByte);
        return; // If type is incorrect, return
    }
    if (driver.getBytes()[3] != roomId) {
        Serial.write("Error: Incorrect roomId: "); // Write to computer port
        Serial.println(driver.getBytes()[3]);
        Serial.write("Expected: "); // Write to computer port
        Serial.println(roomId);
        return; // If roomId is incorrect, return
    }
    Serial.write("Correct roomId.\n\r"); // Write to computer port
    energyData.setTimeOfHour(driver.getBytes()[4]); // Update minutesTillNextHour
    energyData.setCurrentPrice(driver.getBytes()[5]+0.01*driver.getBytes()[6]); // Update currentPrice
    energyData.set1hPrice(driver.getBytes()[7]+0.01*driver.getBytes()[8]); // Update 1hPrice
    energyData.set2hPrice(driver.getBytes()[9]+0.01*driver.getBytes()[10]); // Update 2hPrice
    energyData.setCurrentConsumption(driver.getBytes()[11]+0.01*driver.getBytes()[12]); // Update currentConsumption
    energyData.setMeanConsumption(driver.getBytes()[13]+0.01*driver.getBytes()[14]); // Update meanConsumption
    Serial.write("Regulation data updated.\n\r"); // Write to computer port

    // Print data
    Serial.print("Minutes till next hour: ");
    Serial.println(energyData.getTimeOfHour());
    Serial.print("Current Price: ");
    Serial.println(energyData.getCurrentPrice());
    Serial.print("1h Price: ");
    Serial.println(energyData.get1hPrice());
    Serial.print("2h Price: ");
    Serial.println(energyData.get2hPrice());
    Serial.print("Current Consumption: ");
    Serial.println(energyData.getCurrentConsumption());
    Serial.print("Mean Consumption: ");
    Serial.println(energyData.getMeanConsumption());
    Serial.write("\n\n");

    driver.resetBytes(); // Reset the bytes array

}

void LavTemperatur:: addRoom(int roomId){
    rooms.push_back(Room(roomId));
}

void LavTemperatur::waitUntill(uint8_t hours)
{
    Serial.write("Waiting...\n\r");
    int minutesLeft = static_cast<int>(hours*60 - energyData.getTimeOfHour()); //begrener antal minutter tilbage af den gældende time
    Serial.print("Minutes left: ");
    Serial.println(minutesLeft);
    int minutesInMs = minutesLeft*6E5; // Cast minutesLeft to int
    minutesInMs = minutesInMs < 0 ? -minutesInMs : minutesInMs; // If minutesInMs is negative, set it to 0
    Serial.println(minutesInMs);
    delay(minutesInMs); //Venter
}

double LavTemperatur::getPriceCap()
{
    return priceCap;
}

Room &LavTemperatur::getRoom(int roomId)
{
    return rooms.getRoom(roomId);
}
