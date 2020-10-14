import processing.serial.*;

final int comPortIndex = 0;

Serial mySerial;  // Create object from Serial class
byte[] serialInBuffer = new byte[4];
int serialCount = 0;                 // A count of how many bytes we receive
boolean firstContact = false;        // Whether we've heard from the microcontroller

void setup() {
  size(200, 200);
  println("Pick the turntables com port by setting comPortIndex \nin beginning of program to the index on left. \n" );
  printArray(Serial.list());
  mySerial = new Serial(this, Serial.list()[comPortIndex], 115200);
  mySerial.buffer(4);
  println();
  delay(1500);
}

void draw() {

    
}


void serialEvent(Serial myPort) {
 printArray(binary(myPort.readBytes()));
}