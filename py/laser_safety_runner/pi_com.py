import byte_manip as b_manip
import serial

COM_PORT_INDEX = 1
CONTACT_TO_ARD = b'170'
RESET_COUNTS = b'153'

serial_in_buffer = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
serial_count = 0
inputs_from_ard = 0
last_millis = 0
check_ard_timeout = 1000


##################################################
# Name: serial_event
# Description: TODO implement!
##################################################
def serial_event():
    pass

# // arduino splits up the data int, only using 4LSB in transmission (0-15)of every byte
# // any ones in the 4 MSB (16-255)indicates end of packet and contains arduino status
# void serialEvent(Serial myPort) {
#   while ( myPort.available() > 0) {
#     serialInBuffer[serialCount]= myPort.read();
#     if (serialInBuffer[serialCount] > 127 && serialCount >= 5) {//status byte from arduino means end of packet
#       //println((byte)serialInBuffer[serialCount]& 0x0F);
#
#       if ((serialInBuffer[serialCount] & (1<<6))>0) { //if 2nd MSB is flipped
#         println("Arduino triggered the watchdog!");
#         //myPort.write(RESET_COUNTS);
#       }
#       if ((serialInBuffer[serialCount] & (1<<5))>0) { //if 3rd MSB is flipped
#         println("Arduinos reporting an error occured at least once!");
#       }
#       inputsFromArd=serialInBuffer[serialCount-1]<<12 |
#         serialInBuffer[serialCount-2]<<8 |
#         serialInBuffer[serialCount-3]<<4 |
#         serialInBuffer[serialCount-4];
#       if(serialInBuffer[serialCount-5]==inputsFromArd % 128){
#         myPort.write(serialInBuffer[serialCount-5]);
#       } else{
#         println("CheckSum didnt Match!");
#       }
#       println(binary(inputsFromArd));
#       serialCount=0;
#     } else {
#       serialCount++;
#     }
#   }
#   lastMillis = millis();
# }
