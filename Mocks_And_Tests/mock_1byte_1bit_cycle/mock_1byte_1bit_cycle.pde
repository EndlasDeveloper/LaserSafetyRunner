/**
 * Testing sketch: Opens a port and writes 2 bytes every second. Each write sends all zeros except for 1 bit that is set.
                   This bit cycles through bits 0 through 7, disappears, then starts the cycle again at bit 0. This simulates
                   potential inputs for the Laser Safety Runner application.
 */
 
import processing.serial.*;

byte[] bytesToWrite = {1, 0};
Serial port; 

void setup() 
{
 // Just finds an available port and opens it
 for(String com : Serial.list()){
  // open COM_PORT
  try { 
    port = new Serial(this, com, 9600);
    loop();
  } catch(Exception ex){ continue; }
 }
 // no open ports, so exit program
 exit();
}

void loop(){
  // wait a second, then write the next byte package
  delay(1000);
  println("bytes to write[0]: " + binary(bytesToWrite[0]));
  port.write(bytesToWrite);
  if(bytesToWrite[0] == 0) {
    bytesToWrite[0] = 1;
    loop();
  }
  bytesToWrite[0] <<= 1;
  loop();
}
