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

uint32_t inputs = 0; //where the inputs are stored
uint8_t ErrCount = 0; // the 4 LSBs of the magic Status byte containing the err count of interest

void setup() {
  Serial.begin(115200);
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
  pinMode(15, INPUT_PULLUP);
  pinMode(16, INPUT_PULLUP);
  pinMode(17, INPUT_PULLUP);
  pinMode(18, INPUT_PULLUP);
  pinMode(19, INPUT_PULLUP);
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
        
      }
    }
    else {
      expectingCheckSumResponse = false;
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
  bitWrite(inputs, 0, !digitalRead(10));
  bitWrite(inputs, 1, !digitalRead(11));
  bitWrite(inputs, 2, !digitalRead(A5));
  bitWrite(inputs, 3, !digitalRead(A4));
  bitWrite(inputs, 4, !digitalRead(A3));
  bitWrite(inputs, 5, !digitalRead(A2));
  bitWrite(inputs, 6, !digitalRead(A1));
  bitWrite(inputs, 7, !digitalRead(A0));

  bitWrite(inputs, 8, !digitalRead(2));
  bitWrite(inputs, 9, !digitalRead(3));
  bitWrite(inputs, 10, !digitalRead(4));
  bitWrite(inputs, 11, !digitalRead(5));
  bitWrite(inputs, 12, !digitalRead(6));
  bitWrite(inputs, 13, !digitalRead(7));
  bitWrite(inputs, 14, !digitalRead(8));
  bitWrite(inputs, 15, !digitalRead(9));
  if (inputs != lastInputs) {
    lastInputs = inputs;
    return 1;
  }
  else
  {
    return 0;
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
    //triggerWatchdog();
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
