#define MAGIC_BYTE 15
#define NUMBER_OF_BYTES 5

static const int DELAY = 1000;
static uint8_t bytes[5] = {0b1, 0, 0, 0, 0b11110000};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200); 
  while (!Serial) {} // wait for serial port to connect

}

void loop() {
  Serial.write(bytes, 5);
  if((bytes[0] << 1) <= 0)
    bytes[0] = 0b1;
  else
    bytes[0] <<= 1;
  delay(1000);
}

void writeToSerial(){
  // Serial.write(1);

    Serial.write(bytes,5);
    
}
