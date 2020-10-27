#define MAGIC_BYTE 15
#define NUMBER_OF_BYTES 5
#define HANDSHAKE 0xFF
#define BAUD_RATE 115200

static const int DELAY = 1500;
static uint8_t bytesToWrite[5] = {1, 0, 0, 0, 240};
static bool isPiReady = false;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(BAUD_RATE); 
  while (!Serial) {} // wait for serial port to connect

}

static uint32_t numChecks = 0;
void checkIfPiIsReady(){
  if(Serial) {
    Serial.write(HANDSHAKE);
    byte reply = Serial.read();
    Serial.print(reply);
    if(reply != 0) {
      isPiReady = true;
      delay(DELAY);
    }
  }
}
  
  void loop() {
  if(!isPiReady) {
    checkIfPiIsReady();
  } else {
    writeToSerial();
    delay(DELAY);
  }
  delay(DELAY / 4);
}

static uint32_t index = 0;
void writeToSerial(){
  Serial.write(bytesToWrite,5);

  if(bytesToWrite[index] < 8){
    bytesToWrite[index] <<= 1;
  }else if(index == 0){
    bytesToWrite[index] = 0;
    index++;
    bytesToWrite[index] = 1;
  } else if(index == 1) {
    bytesToWrite[index] = 0;
    index++;
    bytesToWrite[index] = 1;
  } else if(index == 2) {
    bytesToWrite[index] = 0;
    index++;
    bytesToWrite[index] = 1;
  }else if(index == 3) {
    bytesToWrite[index] = 0;
    index = 0;
    bytesToWrite[index] = 1;
  }
  bytesToWrite[4] = 240;
}
