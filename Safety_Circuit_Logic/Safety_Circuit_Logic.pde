// Define 
#define program 1 
#define estop 2
#define safecircuit 3
#define threshold 4
#define shutter 5
#define laserfire 6
#define warning 7
#define fault 8
#define sleep 9 
#define fibererror 10

PImage img;

void setup() {
  
  pinMode(estop,INPUT); // set pin 2 as input
  pinMode(safecircuit,INPUT); // set pin 2 as input
  pinMode(defeatsafety, INPUT); // set pin X as input
  pinMode(threshold,INPUT); // set pin 2 as input
  pinMode(shutter,INPUT); // set pin 2 as input
  pinMode(laserfire,INPUT); // set pin 2 as input
  pinMode(warning,INPUT); // set pin 2 as input
  pinMode(fault,OUTPUT); // set pin 2 as input
  pinMode(sleep INPUT); // set pin 2 as input
  pinMode(fibererror, INPUT);  // sets the digital pin 13 as input
  pinMode(program, INPUT);    // sets the digital pin 7 as input
}



//Main loop
void loop() 
{
  s = safetyflag; //run safety circuit check, flag inputs, faults, or estops
  
  if s == 1 //estop flag
  {
    img = loadImage("estop active.jpg");
    draw();
    digitalWrite(fault, high);
  }
  
  else if s == 2 //defeatable entry flag
  {
    img = loadImage("defeatsafety.jpg");
    draw();
    digitalWrite(fault, high);
  }
  
  else if s == 3 //safety circuit broken
  {
    img = loadImage("safetycircuitbroken.jpg");
    draw();
    digitalWrite(fault, high);
  }

  //check to see if laser is ready to fire, only if no flag is active
  else if s ==0
  {      
    r = ready2fire; //ready check
    
    if r == 1 
    {
      p = programrun; //check if program is currently running
      
      while p == 1 || r =1 //send laser firing signal if both checks are passed
      {
        digitalWrite(laserfire, high);
        img = loadImage("DANGERLASERON.jpg");
        draw();
        
        p = programrun();
        r = ready2fire();
      }  
      
      img = loadImage("Ready2FireWarning.jpg");
      draw();
    }
    
    else
    {
      img = loadImage(".jpg");// error image? not sure how this thread occurs
      draw();
    }
  }             
  
  else
  {
    img = loadImage("Safety Circuit Error.jpg"); // General issue with the safety circuit that cannot be determined
    draw();
    digitalWrite(fault, high);
  }
}





// draw image stored in img
void draw() {
  image(img, 0, 0);
}



// safety circuit/estop loop - find way to set this as its own command so it can be referenced while laser is firing.
int safetyflag() {
  
  stat = digitalRead(estop); //read input pin
  
  if stat == high;
    {
      //return flag value
      return 1;
    }
    
  stat = digitalRead(defeatsafety); //read input pin
  
  if stat == high
    {
      //return flag value
      return 2;
    }
  
  stat = digitalRead(safecircuit); //read input pin
  
  if stat == low
    {
      //return flag value
      return 3;
    }
      
  return 0; //pass through if no errors
)




// check to see if laser is ready to fire
int ready2fire()
{

  stat = digitalRead(threshold); //read input pin
  
  if stat == low;
    {
      check1 = 1; //pass check and set 1/3 to fire laser
    }

  stat = digitalRead(shutter); //read input pin
  
  if stat == low;
    {
      check2 = 1; //pass check and set 2/3 to fire laser
    }

  stat = digitalRead(fiber); //read input pin
  
  if stat == high;
    {
      check3 = 1; //pass check and set 3/3 to fire laser
    }

  if check1 || check2 || check3 == 1 //three locks to open the door
    {
    return 1;
    }
      
  return 0; //return false value if not ready to go
}
