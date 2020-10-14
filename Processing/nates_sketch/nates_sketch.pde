/// LIBRARIES
import processing.serial.*;

////////////////////////////////////////////////////////////////////////////////
// CONSTANTS
// --------- BYTES EXPECTED IN BUFFER FOR STATE ----------------- //////////
final int BUFFER_BYTES_TO_READ = 1;
// --------- MASKS ------------------ ////////////////////////////////////// 
final int ESTOP = 1;
final int SAFETY_CIRCUIT = 2;
final int DEFEAT_SAFETY = 4;
final int LASER_FIRE = 8;
final int WARNING = 16;
final int FIBER_ERROR = 32;
final int THRESHOLD = 64;
final int SHUTTER = 128;
final int FAULT = 256;
final int SLEEP = 512;
final int PROGRAM = 1024;
// --------- IMAGES & PATH ------------ ///////////////////////////////////
final String IMG_PATH = "../resources/";
final String ESTOP_IMG = IMG_PATH + "estop_active.jpg";
final String SAFETY_CIRCUIT_IMG = IMG_PATH + "safety_circiut_error.jpg";
final String DEFEAT_SAFETY_IMG = IMG_PATH + "defeat_safety.jpg";
final String LASER_FIRE_IMG = IMG_PATH + "danger_prog.jpg";
final String WARNING_IMG = IMG_PATH + "ready_2_fire_warning.jpg";
final String FIBER_ERROR_IMG = IMG_PATH + "fiber_error.jpg";
/// NO IMAGES FOR THESE YET
final String THRESHOLD_IMG = "";
final String SHUTTER_IMG = "";
final String FAULT_IMG = "";
final String SLEEP_IMG = "";
final String PROGRAM_IMG = "";
////////////////////////////////////////////////////////////////////////////////

// STATE MAP //
HashMap<Integer, Boolean> states = new HashMap();

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
  size(1000, 1000);
  // set initial image to draw
  img = loadImage(ESTOP_IMG);
  // delay(1500);
}

int parseBytes(byte[] bytes){
  int zeroByte, oneByte, twoByte, threeByte;
  zeroByte = bytes[0];
  oneByte = bytes[1] << 8;
  twoByte = bytes[2] << 16;
  threeByte = bytes[3] << 24;
  return zeroByte + oneByte + twoByte + threeByte;
}

/*
 * Name: serialEvent
 * Description: Needed method for listening to a serial port for input. After initializing up the buffer in setup,
                this method acts as the event listener for the serial port opened during initialization. 
*/
void serialEvent(Serial myPort) {
    println("");
    println("int state: " + inputState);
    println("binary state: " + binary(inputState));
    println("serial event index:" + serialCount++);
    println("");
    if(inputState < 1024){
      inputState <<= inputState;
    } else {
      inputState = 1;
    }
}

/*
 * Name: draw
 * Description: Needed method to render the image / output the inString
*/
void draw() {
  image(img, 0, 0);
  loop();
}

void parseInputState(int inputState){
    // set local var
    // ESTOP
    int s = inputState & ESTOP;
    states.put(ESTOP, (s >= 1));
    
    // SAFETY CIRCUIT
    s = inputState & SAFETY_CIRCUIT;
    states.put(SAFETY_CIRCUIT, (s >= 1));
    
    // DEFEAT SAFETY
    s = inputState & DEFEAT_SAFETY;
    states.put(DEFEAT_SAFETY, (s >= 1));
    
    // LASER FIRE
    s = inputState & LASER_FIRE;
    states.put(LASER_FIRE, (s >= 1));
    
    // WARNING
    s = inputState & WARNING;
    states.put(WARNING, (s >= 1));
    
    // FIBER ERROR
    s = inputState & FIBER_ERROR;
    states.put(FIBER_ERROR, (s >= 1));
    
    // THRESHOLD
    s = inputState & THRESHOLD;
    states.put(THRESHOLD, (s >= 1));
    
    // SHUTTER
    s = inputState & SHUTTER;
    states.put(SHUTTER, (s >= 1));
    
    // FAULT
    s = inputState & FAULT;
    states.put(FAULT, (s >= 1));
    
    // SLEEP
    s = inputState & SLEEP;
    states.put(SLEEP, (s >= 1));
    
    // PROGRAM
    s = inputState & PROGRAM;
    states.put(PROGRAM, (s >= 1)); 
}

/*
 * Name: loop
 * Description: infinite loop method for continually checking the state of the system  
 */
void loop() {
  // if the input doesn't match the curr state
  if(currState != inputState){ //<>//
    parseInputState(inputState);
    // set curr state to the input state
    currState = inputState;
    
    if(states.get(ESTOP)){
      img = loadImage(ESTOP_IMG);
      println("ESTOP");
      
    } else if(states.get(SAFETY_CIRCUIT)){
      img = loadImage(SAFETY_CIRCUIT_IMG);
      println("SAFETY_CIRCUIT");
      
    } else if(states.get(DEFEAT_SAFETY)){
      img = loadImage(DEFEAT_SAFETY_IMG);
      println("DEFEAT_SAFETY");
      
    } else if(states.get(LASER_FIRE)){
      img = loadImage(LASER_FIRE_IMG);
      println("LASER_FIRE");
      
    } else if(states.get(WARNING)){
      img = loadImage(WARNING_IMG);
      println("WARNING");
      
    } else if(states.get(FIBER_ERROR)){
      img = loadImage(FIBER_ERROR_IMG);
      println("FIBER_ERROR");
      
    } else if(states.get(FAULT)){
      println("FAULT");
    } else if(states.get(SLEEP)){
      println("SLEEP");
    } else if(states.get(PROGRAM)){
      println("PROGRAM");
    } else if(states.get(THRESHOLD)){
      println("THRESHOLD");
    } else if(states.get(SHUTTER)){
      println("SHUTTER");
    } else {
      println("all states are off");
      println("state: " + currState);
    }
    draw();
  }
}
