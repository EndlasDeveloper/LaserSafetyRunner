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
  } catch(Exception ex){
    println("Failed to open a port.\nMake sure there is an available port.");
    continue;
  }
 }
 // no open ports, so exit program
 exit();
}
int byteIndex = 0;
void loop(){
  // wait a second, then write the next byte package
  delay(1000);
  println("bytes to write: " + binary(bytesToWrite[1]) + binary(bytesToWrite[0]));
  port.write(bytesToWrite);
  bytesToWrite[byteIndex] <<= 1;
  if(bytesToWrite[byteIndex] == 0) {
    if(byteIndex == 0){
      byteIndex = 1;
    } else {
      delay(1000);
      println("bytes to write: " + binary(bytesToWrite[1]) + binary(bytesToWrite[0]));
      port.write(bytesToWrite);
      byteIndex = 0;
    }
    bytesToWrite[byteIndex] = 1;
  } 
  loop();
}
