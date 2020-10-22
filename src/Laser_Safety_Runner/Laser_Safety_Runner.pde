/// LIBRARIES
import processing.serial.*;

////////////////////////////////////////////////////////////////////////////////
// CONSTANTS
// --------- BYTES EXPECTED IN BUFFER FOR STATE ----------------- //////////
final int BUFFER_BYTES_TO_READ = 2;
// --------- MASKS ------------------ ////////////////////////////////////// 


final int LASER_FIRE_MASK = 0b1;
final int THRESHOLD_MASK = 0b10;
final int SHUTTER_MASK = 0b100;
final int PROGRAM_MASK = 0b1000;

final int ESTOP_MASK = 0b100000000;
final int SAFETY_CIRCUIT_MASK = 0b1000000000;
final int DEFEAT_SAFETY_MASK = 0b10000000000;
final int WARNING_MASK = 0b100000000000;

final int FAULT_MASK = 0b10000000000000000;
final int SLEEP_MASK = 0b100000000000000000;
final int FIBER_ERROR_MASK = 0b1000000000000000000;


// --------- IMAGES & PATH ------------ ///////////////////////////////////
final String IMG_PATH = "../resources/";
final String ESTOP_IMG = IMG_PATH + "estop_active.jpg";
final String SAFETY_CIRCUIT_IMG = IMG_PATH + "safety_circiut_error.jpg";
final String DEFEAT_SAFETY_IMG = IMG_PATH + "defeat_safety.jpg";
final String LASER_FIRE_IMG = IMG_PATH + "laser_fire.jpg";
final String PILOT_FIRE_IMG = IMG_PATH + "pilot_laser.jpg";
final String WARNING_IMG = IMG_PATH + "warning.jpg";
final String FIBER_ERROR_IMG = IMG_PATH + "fiber_error.jpg";
final String FAULT_IMG = IMG_PATH + "fault.jpg";
final String SLEEP_IMG = IMG_PATH + "sleep.jpg";
final String NO_LOAD_IMG = IMG_PATH + "noload.jpg";
/// COMMUNICATION PORT FOR PROGRAM TO LOOK FOR AND OPEN ///
final String COM_PORT = "COM5";
////////////////////////////////////////////////////////////////////////////////

// GLOBAL OBJECTS
PImage img;                       // image object for setting an image file to for rendering
Serial port;                      // Serial object for USB serial communications
HashMap<Integer, Boolean> states; // states hash table to store whether a state's bit was set or not

// GLOBAL VARS
int inputState = 1; // variable for holding direct serial inputs
int currState = -1; // var for saving current state
int serialCount = 0;

/*
 * Name: setup
 * Description: Needed initialization method to set up the program before calling the draw method.
 *              Sets default image and the size of said image before calling draw 
 */
void setup() {
  // initialize window size for image rendering
  size(960, 540);
  // make sure COM_PORT exists
  for(String com : Serial.list()){
    if(com.equals(COM_PORT)){ // found COM_PORT so initialize com port, buffer size, and the initial image to render
      // open COM_PORT
      try {
        port = new Serial(this, COM_PORT, 9600);
        // sets number of bytes to read at a time
        port.buffer(BUFFER_BYTES_TO_READ);
        // define image dimensions
        // set initial image to draw
        img = loadImage(ESTOP_IMG); 
        return;
      } catch(Exception ex){
        println("Port " + COM_PORT + " failed to open. Port could be busy.");
        exit();       
      }
    }
  }  
  // Didn't find the right communication port, so msg, available ports, and exit the program 
  println("Laser_Safety_Runner.pde setup(): Serial list doesn't contain communication port " + COM_PORT);
  for(String com: Serial.list())
    println("Serial list: " + com);
  exit();
}

/*
 * Name: parseBytes
 * Description: Not sure if this method is needed, but returns an integer built up from 4 bytes
*/
int parseBytes(byte[] bytes){
  return bytes[0] + bytes[1] << 1 + bytes[2] << 2 +bytes[3] << 3;
}

/*
 * Name: serialEvent
 * Description: Needed method for listening to a serial port for input. After initializing up the buffer in setup,
                this method acts as the event listener for the serial port opened during initialization. 
*/
void serialEvent(Serial port) {
  // get input state if enough bytes are in the buffer
  if(port.available() >= 2) {  
    inputState = port.read();
  } else { // not enough available bytes, so return
   println("port.available() < 2");
   return;
  }
  
  // DEBUGGING CODE
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

/*
 * Name: hashInputStates
 * Description: takes input state and hashes a boolean with each state's mask to indicate whether that state's bit was set
 */
void parseInputState(int inputState){
    states = new HashMap();
    // ESTOP
    states.put(ESTOP_MASK, ((inputState & ESTOP_MASK) >= 1));
    // SAFETY CIRCUIT
    states.put(SAFETY_CIRCUIT_MASK, ((inputState & SAFETY_CIRCUIT_MASK) >= 1));
    // DEFEAT SAFETY
    states.put(DEFEAT_SAFETY_MASK, ((inputState & DEFEAT_SAFETY_MASK) >= 1));
    // LASER FIRE
    states.put(LASER_FIRE_MASK, ((inputState & LASER_FIRE_MASK) >= 1));
    // WARNING
    states.put(WARNING_MASK, ((inputState & WARNING_MASK) >= 1));
    // FIBER ERROR
    states.put(FIBER_ERROR_MASK, ((inputState & FIBER_ERROR_MASK) >= 1));
    // THRESHOLD
    states.put(THRESHOLD_MASK, ((inputState & THRESHOLD_MASK) >= 1));
    // SHUTTER
    states.put(SHUTTER_MASK, ((inputState & SHUTTER_MASK) >= 1));
    // FAULT
    states.put(FAULT_MASK, ((inputState & FAULT_MASK) >= 1));  
    // SLEEP
    states.put(SLEEP_MASK, ((inputState & SLEEP_MASK) >= 1));   
    // PROGRAM
    states.put(PROGRAM_MASK, ((inputState & PROGRAM_MASK) >= 1)); 
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
      img = loadImage(ESTOP_IMG); //<>//
      println("ESTOP");
      
    } else if(states.get(SAFETY_CIRCUIT_MASK)){
      img = loadImage(SAFETY_CIRCUIT_IMG);
      println("SAFETY_CIRCUIT");
      
    } else if(states.get(DEFEAT_SAFETY_MASK)){
      img = loadImage(DEFEAT_SAFETY_IMG);
      println("DEFEAT_SAFETY");
      
    } else if(states.get(LASER_FIRE_MASK)){ //sign needs to be designated if threshold is on or off in case pilot laser is fired
      if (states.get(THRESHOLD_MASK))
         img = loadImage(PILOT_FIRE_IMG);               
      else
         img = loadImage(LASER_FIRE_IMG);       
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
    if(states.get(PROGRAM_MASK)){
       rectMode(CORNER);  // Default rectMode is CORNER
       fill(255, 0, 0);  // Set fill to white
       rect(315, 465, 330, 45);
     
       textSize(32);
       fill(255);
       text("PROGRAM RUNNING", 325, 500); 
    }
                
    if(states.get(SHUTTER_MASK)){
       rectMode(CORNER);  // Default rectMode is CORNER
       fill(255, 0, 0);  // Set fill to white
       rect(665, 418, 265, 45);
     
       textSize(32);
       fill(255);
       text("SHUTTER OPEN", 675, 455);   
    }
                
    if(states.get(THRESHOLD_MASK)){
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
}
