#include <Wire.h>


#define CONTACT_FROM_PI           170
#define RESET_COUNTS              153


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
bool hasRPiResponded = false;
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
  Serial.begin(115200);
  while(!hasRPiResponded)
    waitForRPi();
  //Serial.println("Im up!");
}

void waitForRPi(){
  Serial.write(byte(1));
  byte response = Serial.read();
  if(response != 1)
    hasRPiResponded = false;
  hasRPiResponded = true;
}

void loop() {
  /* Handle anything in the serial port
      Pi only sends single Bytes.
      if the MSB is a 1 then its a command.
          its either a 170 ( B10101010 ) used to request a set of data or
          a 153 (B10011001) used to Reset the Counts
      If the MSB is a 0 then the rest is 7 bit checksum.
  */
  //Handle anything in the serial port
  while (Serial.available()) {
    byte inByte = Serial.read();
    if (inByte > 127 ) { // if MSB is 1 or not / if command or not
      if (inByte == RESET_COUNTS) {
        resetCounts();
      }
      if (inByte == CONTACT_FROM_PI) {
        contactFromPi = true;
        //Serial.println("CONTACT_FROM_PI");
        send_uint32_in_halfByteArray(inputs);
        //digitalWrite(0,HIGH);
      }
    }
    else {
      expectingCheckSumResponse = false;
//      Serial.print("recieved    ---checkSum: ");
//      Serial.print(inByte,DEC);
//      Serial.print(" in: ");
//      Serial.println(millis() - previousMillis);
    }
  }

  //Make sure the PI is not unresponsive
  if (contactFromPi && expectingCheckSumResponse ) {
    if (millis() - previousMillis > responseFromPi_timeout) {
      noResponseTimeout();
    }
  }


  //Check inputs and send bytes if any changes
  if (checkInputs()) {
    //printBits(inputs, 16);
    send_uint32_in_halfByteArray(inputs);
  }

}

bool checkInputs() {
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
    return 1;
  }
  else
  {
    return 0;
  }
}

void printBits(uint32_t myByte, uint32_t numBits) {
  for (uint32_t mask = pow(2, numBits - 1); mask; mask >>= 1) {
    if (mask  & myByte)
      Serial.print("1");
    else
      Serial.print("0");
  }
  Serial.println();
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
  byte checkSum = uint32 % 128;
  uint8_t SerialOutBuffer[6] = {byte(0)};
  magicStatusByte = (1 << 7) | (watchdogTriggered << 6)  | (noResponseErr << 5) | ErrCount;

  SerialOutBuffer[0] = checkSum;
  SerialOutBuffer[1] = byte(uint32 & 0x0F);
  SerialOutBuffer[2] = byte((uint32 >> 4) & 0x0F);
  SerialOutBuffer[3] = byte((uint32 >> 8) & 0x0F);
  SerialOutBuffer[4] = byte((uint32 >> 12) & 0x0F);
  SerialOutBuffer[5] = byte(magicStatusByte);
  delay(1500);
  Serial.write(SerialOutBuffer, 6);
  delay(2000);
  Serial.print("transmitting---checkSum: ");
  Serial.println(checkSum);
  expectingCheckSumResponse = true;
  previousMillis = millis();
  //digitalWrite(1,LOW);
}

void noResponseTimeout() {
  Serial.print("noResponseTimeout()");
  noResponseErr = true;
  noResponseErrCount++;
  Serial.println(noResponseErrCount, DEC);
  ErrCount = noResponseErrCount;
  if (noResponseErrCount > noResponseErrLimit) {
    triggerWatchdog();
  }
}

void resetCounts() {
  Serial.println("resetCounts()");
  noResponseErrCount = 0;
  watchdogTriggered = false;
  noResponseErr = false;
  expectingCheckSumResponse = false;
}

void triggerWatchdog() {
  Serial.println("triggerWatchdog()");
  watchdogTriggered = true;
  resetCounts();
  //digitalWrite(0,LOW);
  //tell watchdog to reset the Pi
  //Wire.beginTransmission(44); // transmit to device #44 (0x2c)
  //Wire.write(byte(0x00));            // sends instruction byte
  // Wire.write(val);             // sends potentiometer value byte
  // Wire.endTransmission();     // stop transmitting
}
