import processing.serial.*;

PImage img;
int INPUT = 9;
int input = 2;

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

void setup() {
  
  size(1000, 1000);
  img = loadImage("../resources/estop_active.jpg");
  draw();
  
  /*
  GPIO SETUP
  */
  
  
}

void draw() {
  image(img, 0, 0);
  loop();
}

void loop() {

  if(input != INPUT){ //<>//
    input = INPUT;
    switch(INPUT) {
     case ESTOP:
       img = loadImage("../resources/estop_active.jpg");
       draw();
       break;
     case SAFETY_CIRCUIT:
       img = loadImage("../resources/safety_circiut_error.jpg");
       draw();
       break;
     case DEFEAT_SAFETY:
       size(1000, 1000);
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
