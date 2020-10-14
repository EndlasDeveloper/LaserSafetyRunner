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
final int THRESHOLD = 3;
final int SHUTTER = 4;
final int LASER_FIRE = 5;
final int WARNING = 6;
final int FAULT = 7;
final int SLEEP = 8;
final int FIBER_ERROR = 9;
final int PROGRAM = 10;
////////////////////////////////////////

// GLOBAL OBJECTS
PImage img;
Serial myPort;

// GLOBAL PRIMITIVES
int inputState = 2;
int currState = -1;
String inString;

/*
 * Name: setup
 * Description: Needed initialization method to set up the program before calling the draw method.
 *              Sets default image and the size of said image before calling draw 
 */
void setup() {
  myPort = new Serial(this, Serial.list()[0], 9600);
  // sets number of bytes
  myPort.buffer(BUFFER_BYTES_TO_READ);
  size(1000, 1000);
  img = loadImage("../resources/estop_active.jpg");
  draw();
}

/*
 * Name: serialEvent
 * Description: Needed method for listening to a serial port for input. After initializing up the buffer in setup,
                this method acts as the event listener for the serial port opened during initialization. 
*/
void serialEvent(Serial p) { 
  inString = p.readString(); 
} 

/*
 * Name: draw
 * Description: Needed method to render the image / output the inString
*/
void draw() {
  image(img, 0, 0);
  //background(0);
  //text("Received: " + inString, 10, 50);
  loop();
}

/*
 * Name: loop
 * Description: infinite loop method for continually checking the state of the system  
 */
void loop() {
  // if the input doesn't match the curr state
  if(currState != inputState){ //<>//
      // set curr state to the input state
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
          case THRESHOLD:
              println("THRESHOLD");
              break;
          case SHUTTER:
              println("SHUTTER");
              break;
          case LASER_FIRE:
              img = loadImage("../resources/danger_prog.jpg");
              draw();
              break;
          case WARNING:
              img = loadImage("../resources/ready_2_fire_warning.jpg");
              draw();
              break;
          case FAULT:
              println("FAULT");
              break;
          case SLEEP:
              println("SLEEP");
              break;
          case FIBER_ERROR:
              img = loadImage("../resources/fiber_error.jpg");
              draw();
              break;
          case PROGRAM:
              println("PROGRAM");
              break;
          default:
             println("default");
             break;
      }
  }
}