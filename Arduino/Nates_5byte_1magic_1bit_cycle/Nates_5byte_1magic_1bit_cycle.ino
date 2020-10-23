#define MAGIC_BYTE 240
#define NUMBER_OF_BYTES 5;

static int output = 1;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {

 delay(1000);
 Serial.print("states: " + output);
 Serial.write(output);
 if((output << 1) > 0)
  output <<= 1;
 else 
  output = 1;
 
}
