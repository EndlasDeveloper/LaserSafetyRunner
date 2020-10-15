/// LIBRARIES
import processing.serial.*;

////////////////////////////////////////////////////////////////////////////////
// CONSTANTS
// --------- BYTES EXPECTED IN BUFFER FOR STATE ----------------- //////////
final int BUFFER_BYTES_TO_READ = 4;
// --------- MASKS ------------------ ////////////////////////////////////// 
final int ESTOP_MASK = 0b1;             // 00000000001 (1)
final int SAFETY_CIRCUIT_MASK = 0b10;   // 00000000010 (2)
final int DEFEAT_SAFETY_MASK = 0xb100;  // 00000000100 (4)
final int LASER_FIRE_MASK = 0xb1000;    // 00000001000 (8)
final int WARNING_MASK = 0b10000;       // 00000010000 (16)
final int FIBER_ERROR_MASK = 0b100000;  // 00000100000 (32)
final int THRESHOLD_MASK = 0b1000000;   // 00001000000 (64)
final int SHUTTER_MASK = 0b10000000;    // 00010000000 (128)
final int FAULT_MASK = 0b100000000;     // 00100000000 (256)
final int SLEEP_MASK = 0b1000000000;    // 01000000000 (512)
final int PROGRAM_MASK = 0b10000000000; // 10000000000 (1024)
// --------- IMAGES & PATH ------------ ///////////////////////////////////
final String IMG_PATH = "../resources/";
final String ESTOP_IMG = IMG_PATH + "estop_active.jpg";
final String SAFETY_CIRCUIT_IMG = IMG_PATH + "safety_circiut_error.jpg";
final String DEFEAT_SAFETY_IMG = IMG_PATH + "defeat_safety.jpg";
final String LASER_FIRE_IMG = IMG_PATH + "danger_prog.jpg";
final String WARNING_IMG = IMG_PATH + "ready_2_fire_warning.jpg";
final String FIBER_ERROR_IMG = IMG_PATH + "fiber_error.jpg";
final String FAULT_IMG = IMG_PATH + "fault.jpg";
final String SLEEP_IMG = IMG_PATH + "sleep.jpg";
////////////////////////////////////////////////////////////////////////////////

// STATE MAP //
HashMap<Integer, Boolean> states;

// GLOBAL OBJECTS
PImage img;
Serial myPort;

// GLOBAL VARS
int inputState = 1;
int currState = -1;
int serialCount = 0;
byte[] serialInBuffer = new byte[BUFFER_BYTES_TO_READ];
String inString;

/*
 * Name: setup
 * Description: Needed initialization method to set up the program before calling the draw method.
 *              Sets default image and the size of said image before calling draw 
 */
void setup() {
  // no communication devices connected, so return
  if(Serial.list().length == 0){
    println("setup: no serial communication devices detected.");
    return;
  }
  // make sure COM5 exists
  boolean hasCOMPort = false;
  for(String com : Serial.list()){
    // println(com);
    if(com.equals("COM5")){ // found COM5 so set flag
      hasCOMPort = true; 
    }
  }  
  // return if no COM5
  if(!hasCOMPort){
   println("setup: Serial list doesn't contain COM5.");
   return;
  }
  // open COM5
  myPort = new Serial(this, "COM5", 9600);
  
  // sets number of bytes to read at a time
  myPort.buffer(BUFFER_BYTES_TO_READ);
  // define image dimensions
  size(960, 540);
  // set initial image to draw
  img = loadImage(ESTOP_IMG);
  // delay(1500);
}

int parseBytes(byte[] bytes){
  return bytes[0] + bytes[1] << 1 + bytes[2] << 2 +bytes[3] << 3;
}

/*
 * Name: serialEvent
 * Description: Needed method for listening to a serial port for input. After initializing up the buffer in setup,
                this method acts as the event listener for the serial port opened during initialization. 
*/
void serialEvent(Serial myPort) {
    // println("");
    inputState = myPort.read();
    // println("myPort.read() = " + inputState);
    //if(inputState <= 512){
    //  inputState <<= 1;
    //} else {
    //  inputState = 1;
    //}
    
    println("");
    println("int state: " + inputState);
    println("binary state: " + binary(inputState));
    println("serial event index:" + serialCount++);
    println("");
}

/*
 * Name: draw
 * Description: Needed method to render the image / output the inString
*/
void draw() {
  image(img, 0, 0, width, height);
  loop();
}

void parseInputState(int inputState){
    states = new HashMap();
    // set local var
    // ESTOP
    int s = inputState & ESTOP_MASK;
    states.put(ESTOP_MASK, (s >= 1));
    
    // SAFETY CIRCUIT
    s = inputState & SAFETY_CIRCUIT_MASK;
    states.put(SAFETY_CIRCUIT_MASK, (s >= 1));
    
    // DEFEAT SAFETY
    s = inputState & DEFEAT_SAFETY_MASK;
    states.put(DEFEAT_SAFETY_MASK, (s >= 1));
    
    // LASER FIRE
    s = inputState & LASER_FIRE_MASK;
    states.put(LASER_FIRE_MASK, (s >= 1));
    
    // WARNING
    s = inputState & WARNING_MASK;
    states.put(WARNING_MASK, (s >= 1));
    
    // FIBER ERROR
    s = inputState & FIBER_ERROR_MASK;
    states.put(FIBER_ERROR_MASK, (s >= 1));
    
    // THRESHOLD
    s = inputState & THRESHOLD_MASK;
    states.put(THRESHOLD_MASK, (s >= 1));
    
    // SHUTTER
    s = inputState & SHUTTER_MASK;
    states.put(SHUTTER_MASK, (s >= 1));
    
    // FAULT
    s = inputState & FAULT_MASK;
    states.put(FAULT_MASK, (s >= 1));
    
    // SLEEP
    s = inputState & SLEEP_MASK;
    states.put(SLEEP_MASK, (s >= 1));
    
    // PROGRAM
    s = inputState & PROGRAM_MASK;
    states.put(PROGRAM_MASK, (s >= 1)); 
}

/*
 * Name: loop
 * Description: infinite loop method for continually checking the state of the system  
 */
void loop() {
 
  
  // if the input doesn't match the curr state
  if(currState != inputState){
    parseInputState(inputState);
    // set curr state to the input state
    currState = inputState;
    
    if(states.get(ESTOP_MASK)){
      img = loadImage(ESTOP_IMG);
      println("ESTOP");
      
    } else if(states.get(SAFETY_CIRCUIT_MASK)){
      img = loadImage(SAFETY_CIRCUIT_IMG);
      println("SAFETY_CIRCUIT");
      
    } else if(states.get(DEFEAT_SAFETY_MASK)){
      img = loadImage(DEFEAT_SAFETY_IMG);
      println("DEFEAT_SAFETY");
      
    } else if(states.get(LASER_FIRE_MASK)){ //sign needs to be designated if threshold is on or off in case pilot laser is fired
      if (states.get(THRESHOLD_MASK)){
         img = loadImage("../resources/pilot_laser.jpg");
         draw();
         println("LASER_FIRE");
      }              
      else
         img = loadImage("../resources/laser_fire.jpg");
         draw(); 
         println("LASER_FIRE");
      
    } else if(states.get(WARNING_MASK)){
      img = loadImage(WARNING_IMG);
      println("WARNING");
      
    } else if(states.get(FIBER_ERROR_MASK)){
      img = loadImage(FIBER_ERROR_IMG);
      println("FIBER_ERROR");
      
    } else if(states.get(FAULT_MASK)){
      img = loadImage(FAULT_IMG);
      println("FAULT");
      
    } else if(states.get(SLEEP_MASK)){
      img = loadImage(SLEEP_IMG);
      println("SLEEP"); //<>//
      
      //Note: removed threshold, shutter, and program checks.
    } else { // TODO: consider whether this code block should throw an exception or is an acceptable possibility
      println("All flags in states map are false.");
      println("state: " + currState);
    }
    draw();
}
    
  if (states.get(PROGRAM_MASK)){
     rectMode(CORNER);  // Default rectMode is CORNER
     fill(255, 0, 0);  // Set fill to white
     rect(315, 465, 330, 45);
     
     textSize(32);
     fill(255);
     text("PROGRAM RUNNING", 325, 500); 
  }
                
  if (states.get(SHUTTER_MASK)){
     rectMode(CORNER);  // Default rectMode is CORNER
     fill(255, 0, 0);  // Set fill to white
     rect(665, 418, 265, 45);
     
     textSize(32);
     fill(255);
     text("SHUTTER OPEN", 675, 455);   
  }
                
  if (states.get(THRESHOLD_MASK)){
     rectMode(CORNER);  // Default rectMode is CORNER
     fill(255, 0, 0);  // Set fill to white
     rect(665, 465, 265, 45);
     
     textSize(32);
     fill(255);
     text("THRESHOLD ON", 675, 500); 
  } 
  // nothing changed in the state, so do not draw anthing
  return;
}
