int ESTOP, SAFETY_CIRCUIT,DEFEAT_SAFETY,THREHOLD,SHUTTER, LASER_FIRE, WARNING, FAULT, SLEEP, FIBER_ERROR, PROGRAM;
int high, low;

import processing.io.*;

PImage img;
  
/*
Name: Setup
Function: initialization function before loop. Sets size of output image.
*/
void setup() {
  size(1000,1000);
  img = loadImage("estopactive.JPG");
  draw();
  //GPIO.pinMode(ESTOP, GPIO.INPUT); // set pin 2 as input
  //GPIO.pinMode(SAFETY_CIRCUIT,GPIO.INPUT); // set pin 2 as input
  //GPIO.pinMode(DEFEAT_SAFETY, GPIO.INPUT); // set pin X as input
  //GPIO.pinMode(THREHOLD, GPIO.INPUT); // set pin 2 as input
  //GPIO.pinMode(SHUTTER, GPIO.INPUT); // set pin 2 as input
  //GPIO.pinMode(LASER_FIRE, GPIO.INPUT); // set pin 2 as input
  //GPIO.pinMode(WARNING, GPIO.INPUT); // set pin 2 as input
  //GPIO.pinMode(FAULT, GPIO.OUTPUT); // set pin 2 as input
  //GPIO.pinMode(SLEEP, GPIO.INPUT); // set pin 2 as input
  //GPIO.pinMode(FIBER_ERROR, GPIO.INPUT);  // sets the digital pin 13 as input
  //GPIO.pinMode(PROGRAM, GPIO.INPUT);    // sets the digital pin 7 as input
}


/*Name:Loop
Function: Main continuous loop that checks safety circuits and sees changes in laser state.
*/
void loop() 
{

  int s = safetyflag(); //run safety circuit check, flag inputs, FAULTs, or ESTOPs
  s=1;
  if (s == 1) //ESTOP flag
  {
    img = loadImage("estopactive.JPG");
    //draw();
    //GPIO.digitalWrite(2, GPIO.HIGH);
  }
  
  else if (s == 2) //defeatable entry flag
  {
    img = loadImage("DEFEAT_SAFETY.jpg");
    draw();
    //GPIO.digitalWrite(FAULT, GPIO.LOW );
  }
  
  else if (s == 3) //safety circuit broken
  {
    img = loadImage("safetycircuitbroken.jpg");
    draw();
    //GPIO.digitalWrite(FAULT, GPIO.HIGH);
  }

  //check to see if laser is ready to fire, only if no flag is active
  else if (s == 0)
  {      
    int r = ready2fire(); //ready check
    
    if (r == 1) //THREHOLD is on
    {
      img = loadImage("pilotlaser.jpg");
      draw();
      //GPIO.digitalWrite(FAULT, GPIO.HIGH);
    }
      
    else if (r == 2) //shutter is open
    {
      img = loadImage("shutteropen.jpg");
      draw();
      //GPIO.digitalWrite(FAULT, GPIO.HIGH);
    }
    
    else if (r == 3) //there is a fiber error
    {
      img = loadImage("fibererror.jpg");
      draw();
      //GPIO.digitalWrite(FAULT, GPIO.HIGH);
    }
        
    if (r == 4)
    {
      int p = programrun(); //check if program is currently running
      
      while (p == 1 || r == 1) //send laser firing signal if both checks are passed
      {
        //GPIO.digitalWrite(LASER_FIRE, GPIO.HIGH);
        img = loadImage("DANGERPROG.jpg");
        draw();
        
        p = programrun();
        r = ready2fire();
      }  
      
      img = loadImage("Ready2FireWarning.jpg");
      draw();
    }
    
    else
    {
      img = loadImage("error.jpg");// error image? not sure how this thread occurs
      draw();
    }
  }             
  
  else
  {
    img = loadImage("SafetyCircuitError.jpg"); // General issue with the safety circuit that cannot be determined
    draw();
    //GPIO.digitalWrite(FAULT, high);
  }
}


/* Name: draw
Brief: draw image stored in img variable
*/
void draw() {
  image(img,0,0);
}


/*
Name: safetyflag
Brief:safety circuit/ESTOP loop - find way to set this as its own command so it can be referenced while laser is firing. 
*/
int safetyflag() 
{
  int stat = 1;
  stat = 1;//GPIO.digitalRead(ESTOP); //read input pin
  if (stat == 1)//GPIO.HIGH)
  {
    //return flag value
    return 1;
  }
    
  stat = 1;//GPIO.digitalRead(DEFEAT_SAFETY); //read input pin
  if (stat == 0)//GPIO.HIGH)
  {
    //return flag value
    return 2;
  }
  
  stat = 1;//GPIO.digitalRead(SAFETY_CIRCUIT); //read input pin
  if (stat == 1)//GPIO.LOW)
  {
    //return flag value
    return 3;
  }
  
  return 0; //pass through if no errors  
}


/* Name: ready2fire
Brief: check to see if laser is ready to fire
*/

int ready2fire()
{
  int check1, check2, check3;
  int THRESHOLDS = 0, SHUTTER = 0, FIBER = 0;
  
  int stat = 1;//GPIO.digitalRead(THRESHOLDS); //read input pin
  
  if (stat == 0)//GPIO.LOW)
  {
    check1 = 1; //pass check and set 1/3 to fire laser
  }
  
  else
      return 1;

  stat = 1;//GPIO.digitalRead(SHUTTER); //read input pin
  
  if (stat == 0)//GPIO.LOW)
  {
    check2 = 1; //pass check and set 2/3 to fire laser
  }
  
  else
    return 2;
    
  stat = 1;//GPIO.digitalRead(FIBER); //read input pin
  
  if (stat == 0)//GPIO.HIGH)
  {
    check3 = 1; //pass check and set 3/3 to fire laser
  }
  
  else
    return 3;
    
  if ((check1 & check2 & check3) == 1) //three locks to open the door
  {
    return 4;
  }
  
  return 0; //return false value if not ready to go
}

/*Name:programrun
Brief: 
*/
int programrun() {
  return 0;
}
