import processing.serial.*;

final static int COM_PORT_INDEX = 1;
final static byte CONTACT_TO_ARD=(byte)170;
final static byte RESET_COUNTS=(byte)153;

Serial myPort;                       // The serial port
int[] serialInBuffer = new int[10];    // Where we'll put what we receive
int serialCount = 0;                 // A count of how many bytes we receive
int inputsFromArd = 0;
long lastMillis = 0;
int checkArd_timeout=1000;

void setup() {
  size(256, 256);  // Stage size
  // Print a list of the serial ports, for debugging purposes:
  printArray(Serial.list());
  myPort = new Serial(this, Serial.list()[COM_PORT_INDEX], 115200);
  myPort.write(RESET_COUNTS);
  myPort.write(CONTACT_TO_ARD);
  println();
}

void draw() {
  if (millis() - lastMillis > checkArd_timeout) {
    myPort.write(CONTACT_TO_ARD);
  }
}



// arduino splits up the data int, only using 4LSB in transmission (0-15)of every byte
// any ones in the 4 MSB (16-255)indicates end of packet and contains arduino status
void serialEvent(Serial myPort) {
  while ( myPort.available() > 0) {
    serialInBuffer[serialCount]= myPort.read();
    if (serialInBuffer[serialCount] > 127 && serialCount >= 5) {//status byte from arduino means end of packet
      //println((byte)serialInBuffer[serialCount]& 0x0F);

      if ((serialInBuffer[serialCount] & (1<<6))>0) { //if 2nd MSB is flipped
        println("Arduino triggered the watchdog!");
        //myPort.write(RESET_COUNTS);
      }
      if ((serialInBuffer[serialCount] & (1<<5))>0) { //if 3rd MSB is flipped
        println("Arduinos reporting an error occured at least once!");
      }
      inputsFromArd=serialInBuffer[serialCount-1]<<12 |
        serialInBuffer[serialCount-2]<<8 | 
        serialInBuffer[serialCount-3]<<4 | 
        serialInBuffer[serialCount-4];
      if(serialInBuffer[serialCount-5]==inputsFromArd % 128){
        myPort.write(serialInBuffer[serialCount-5]);
      } else{
        println("CheckSum didnt Match!");
      }
      println(binary(inputsFromArd));
      serialCount=0;
    } else {
      serialCount++;
    }
  }
  lastMillis = millis();
}
