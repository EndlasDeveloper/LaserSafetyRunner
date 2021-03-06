#include <Wire.h>

#define CONTACT_FROM_PI           170
#define RESET_COUNTS              153

#define HW_ADD              0x30
#define RELOAD_ADD          0x00
#define RELOAD_KEY          0xCA
#define WRITE_INTERVAL_ADD  0x01
#define READ_INTERVAL_ADD   0x03

bool contactFromPi = false;
bool expectingCheckSumResponse = false;
long responseFromPi_timeout = 20;
long previousMillis = 0;
/*MagicStatusByte used as unique byte type to indcate the end of a data packet.
  MagicStatusByte also used to indicate arduino status.
  the MSB must be 1.
  currently, the next 3 MSB's are set aside for flags
  the 4 LSBs are used to send the error count.
*/
uint8_t magicStatusByte = (1 << 7);
uint8_t noResponseErrCount = 0;
uint8_t noResponseErrLimit = 3;
bool noResponseErr = false;
bool watchdogTriggered = false;

uint32_t inputs = 0; //where the inputs are stored
uint8_t ErrCount = 0; // the 4 LSBs of the magic Status byte containing the err count of interest

void setup() {
  pinMode(A5, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  for (uint8_t pin = 4; pin < 14 ; pin++) {
    pinMode(pin, INPUT_PULLUP);
  }
  Wire.begin();
  Serial.begin(500000);
  //Serial1.begin(250000);
  //Serial1.println("Im up!");
}

void loop() {
  checkUSBdata();
  checkPiResponseTimeout();
  checkInputs();
}

/* Handle anything in the serial port
      Pi only sends single Bytes.
      if the MSB is a 1 then its a command.
          its either a 170 ( B10101010 ) used to request a set of data or
          a 153 (B10011001) used to Reset the Counts
      If the MSB is a 0 then the rest is 7 bit checksum.
*/
void checkUSBdata() {
  while (Serial.available()) {
    byte inByte = Serial.read();
    if (inByte > 127 ) { // if MSB is 1 or not / if command or not
      if (inByte == RESET_COUNTS) {
        resetCounts();
      }
      if (inByte == CONTACT_FROM_PI) {
        contactFromPi = true;
        //Serial1.println("CONTACT_FROM_PI");
        send_uint32_in_halfByteArray(inputs);
        //digitalWrite(0,HIGH);
      }
    }
    else {
      expectingCheckSumResponse = false;
      //Serial1.print("recieved    ---checkSum: ");
      //Serial1.print(inByte,DEC);
      //Serial1.print(" in: ");
      //Serial1.println(millis() - previousMillis);
    }
  }

}

void checkPiResponseTimeout() {   //Make sure the PI is not unresponsive
  if (contactFromPi && expectingCheckSumResponse ) {
    if (millis() - previousMillis > responseFromPi_timeout) {
      noResponseTimeout();
    }
  }
}

void checkInputs() {    //Check inputs and send bytes if any changes
  static uint32_t lastInputs = 0;
  bitWrite(inputs, 0, !digitalRead(A0));
  bitWrite(inputs, 1, !digitalRead(A1));
  bitWrite(inputs, 2, !digitalRead(4));
  bitWrite(inputs, 3, !digitalRead(5));
  bitWrite(inputs, 4, !digitalRead(6));
  bitWrite(inputs, 5, !digitalRead(7));
  bitWrite(inputs, 6, !digitalRead(8));
  bitWrite(inputs, 7, !digitalRead(9));
  bitWrite(inputs, 8, !digitalRead(10));
  bitWrite(inputs, 9, !digitalRead(11));
  bitWrite(inputs, 10, !digitalRead(12));
  bitWrite(inputs, 11, !digitalRead(13));
  bitWrite(inputs, 12, !digitalRead(A2));
  bitWrite(inputs, 13, !digitalRead(A3));
  bitWrite(inputs, 14, !digitalRead(A4));
  bitWrite(inputs, 15, !digitalRead(A5));
  if (inputs != lastInputs) {
    lastInputs = inputs;
    send_uint32_in_halfByteArray(inputs);
  }
}

/* Packets are sent with the first byte containing A simple 7bit checksum (uint32 % 128)

    In order to have a unique kind of byte to indicate the end of data transmission,
    all of the actual payload is transmitted in half bytes, with 0's in the 4 MSB, so
    our 16 bits to send are transmitted in the first 4 LSB of the next 4 bytes.

    Data must be buffered and reassembled when recieved, putting the 4 LSB's of
    each incomming byte into a single int by groups of 4 in ascending order.

    the last(6th) byte is the MagicStatusByte with a one in the MSB.
    All bytes containing desired data (16 input states) will have a value 0-15,
    and any MagicStatusByte will be >127.
*/
void send_uint32_in_halfByteArray(uint32_t uint32) {
  uint8_t checkSum = uint32 % 128;
  uint8_t SerialOutBuffer[6] = {0};
  magicStatusByte = (1 << 7) | (watchdogTriggered << 6)  | (noResponseErr << 5) | ErrCount;

  SerialOutBuffer[0] = checkSum;
  SerialOutBuffer[1] = uint32 & 0x0F;
  SerialOutBuffer[2] = (uint32 >> 4) & 0x0F;
  SerialOutBuffer[3] = (uint32 >> 8) & 0x0F;
  SerialOutBuffer[4] = (uint32 >> 12) & 0x0F;
  SerialOutBuffer[5] = magicStatusByte;
  Serial.write(SerialOutBuffer, 6);

  expectingCheckSumResponse = true;
  previousMillis = millis();
  //Serial1.print("transmitting---checkSum: ");
  //Serial1.println(checkSum);
}

void noResponseTimeout() {
  //Serial1.print("noResponseTimeout()");
  noResponseErr = true;
  noResponseErrCount++;
  //Serial1.println(noResponseErrCount, DEC);
  ErrCount = noResponseErrCount;
  if (noResponseErrCount > noResponseErrLimit) {
    triggerWatchdog();
  }
}

void resetCounts() {
  //Serial1.println("resetCounts()");
  noResponseErrCount = 0;
  ErrCount = 0;
  watchdogTriggered = false;
  noResponseErr = false;
  expectingCheckSumResponse = false;
}

void triggerWatchdog() {    //tell watchdog to reset the Pi by setting period to low value
  //Serial1.println("triggerWatchdog()");
  watchdogTriggered = true;
  uint16_t WDTperiod = 0;
  WDTperiod = getWDTperiod();
  if (WDTperiod < 2) {
    WDTperiod = 2;
  }
  setWDTperiod(WDTperiod / 2);
}

uint16_t getWDTperiod() {
  uint8_t i2cBufferPos = 0;
  uint8_t i2cBuffer[2] = {0};
  Wire.beginTransmission(HW_ADD);
  Wire.write(READ_INTERVAL_ADD);            // sends instruction byte
  Wire.endTransmission();     // stop transmitting
  Wire.requestFrom(HW_ADD, 2);    // request 2 bytes from slave device
  while (Wire.available()) { // slave may send less than requested
    i2cBuffer[i2cBufferPos] = Wire.read(); // receive a byte
    i2cBufferPos++;
  }
  return ((i2cBuffer[1] << 8) | (i2cBuffer[0]));
}

uint8_t setWDTperiod(uint16_t val) {
  uint16_t newPeriod = 65001;
  if (val > 1) {
    newPeriod = val;
  }
  uint8_t outBuffer[3] = {WRITE_INTERVAL_ADD, newPeriod & 0xFF, (newPeriod >> 8) & 0xFF};
  Wire.beginTransmission(HW_ADD);
  Wire.write(outBuffer, 3);
  return Wire.endTransmission();
}

uint8_t setWDTreload() {
  uint8_t outBuffer[2] = {RELOAD_ADD, RELOAD_KEY};
  Wire.beginTransmission(HW_ADD);
  Wire.write(outBuffer, 2);
  return Wire.endTransmission();
}
