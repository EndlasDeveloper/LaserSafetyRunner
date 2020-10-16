/// LIBRARIES
import processing.serial.*;

////////////////////////////////////////
// CONSTANTS
// -------------------------------- // 
final int BUFFER_BYTES_TO_READ = 3;
// -------------------------------- // 
final int ESTOP = 0;
final int SAFETY_CIRCUIT = 1;
final int DEFEAT_SAFETY = 2;
final int LASER_FIRE = 3;
final int WARNING = 4;
final int FAULT = 5;
final int SLEEP = 6;
final int FIBER_ERROR = 7;
////////////////////////////////////////

// GLOBAL OBJECTS
PImage img;
Serial myPort;

// GLOBAL PRIMITIVES
int inputState = 8;
int currState = -1;

int PROGRAM = 0;
int SHUTTER = 0;
int THRESHLD = 0;

String inString;

/*
 * Name: setup
 * Description: Needed initialization method to set up the program before calling the draw method.
 *              Sets default image and the size of said image before calling draw 
 */
void setup() {
  //myPort = new Serial(this, Serial.list()[0], 9600);
  // sets number of bytes
  //myPort.buffer(BUFFER_BYTES_TO_READ);
  size(960, 540);
  img = loadImage("../resources/load.jpg");
  draw();
  loop();
}

/*
 * Name: serialEvent
 * Description: Needed method for listening to a serial port for input. After initializing up the buffer in setup,
                this method acts as the event listener for the serial port opened during initialization. 

void serialEvent(Serial p) { 
  inString = p.readString(); 
} 


 * Name: draw
 * Description: Needed method to render the image / output the inString
*/
void draw() {
  image(img, 0, 0, width, height);
  //background(0);
  //text("Received: " + inString, 10, 50);
  loop();
}

/*
 * Name: loop
 * Description: infinite loop method for continually checking the state of the system  
 */
void loop() {
  
  //write text box if program, shutter, or threshold inputs are detected
  if (PROGRAM == 1){
     rectMode(CORNER);  // Default rectMode is CORNER
     fill(255, 0, 0);  // Set fill to white
     rect(315, 465, 330, 45);
     
     textSize(32);
     fill(255);
     text("PROGRAM RUNNING", 325, 500); 
                }
                
  if (SHUTTER == 1){
     rectMode(CORNER);  // Default rectMode is CORNER
     fill(255, 0, 0);  // Set fill to white
     rect(665, 418, 265, 45);
     
     textSize(32);
     fill(255);
     text("SHUTTER OPEN", 675, 455);   
                }
                
  if (THRESHLD == 1){
     rectMode(CORNER);  // Default rectMode is CORNER
     fill(255, 0, 0);  // Set fill to white
     rect(665, 465, 265, 45);
     
     textSize(32);
     fill(255);
     text("THRESHOLD ON", 675, 500); 
                } 
  /*
  if (inputState == -99){
     img = loadImage("../resources/load.jpg");
     draw();
  }
  
  
  if (currState == LASER_FIRE){
     if (THRESHLD == 0){
        img = loadImage("../resources/laser_fire.jpg");
        draw();
     }              
     else
        img = loadImage("../resources/pilot_laser.jpg");
        draw();
  }
  */
  
  // if the input doesn't match the curr state // What if there is multiple input states?
  if (currState != inputState){   //<>//
      
     //set current state indicator to input state
     currState = inputState;
     switch(inputState) {
         case ESTOP:
             img = loadImage("../resources/estop_active.jpg");
             draw();
             break;
         case SAFETY_CIRCUIT:
             img = loadImage("../resources/safety_circiut_error.jpg");
             draw();
             break;              
         case DEFEAT_SAFETY:
             img = loadImage("../resources/defeat_safety.jpg");
             draw();
             break;            
         case LASER_FIRE:
             if (THRESHLD == 0){
               img = loadImage("../resources/laser_fire.jpg");
               draw();
               break;
             }              
             else if (THRESHLD == 1){
               img = loadImage("../resources/pilot_laser.jpg");
               draw();
               break;
             }             
         case WARNING:
             img = loadImage("../resources/warning.jpg");
             draw();
             break;               
         case FAULT:
             img = loadImage("../resources/error.jpg");
             draw();
             break;              
         case SLEEP:
             img = loadImage("../resources/sleep.jpg");
             draw();
             break;              
         case FIBER_ERROR:
             img = loadImage("../resources/fiber_error.jpg");
             draw();
             break;
         default:
             img = loadImage("../resources/load.jpg");
             draw();
             break;
      }
  }  
                
      // print in console which states are being tested
      println("---");
      println("Input State is " + inputState);
      println("Shutter is " + SHUTTER);
      println("Threshold is " + THRESHLD);    
     
      // Set time delay between signs
      delay(500);
       
      // Randomize input to simulate multiple inputs and run through issue cases
      inputState = int(random(0, 9));
      PROGRAM = int(random(0, 4));
      SHUTTER = int(random(0, 4));
      THRESHLD = int(random(0, 4));
     
}
