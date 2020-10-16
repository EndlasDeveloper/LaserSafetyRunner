// safety circuit/estop loop - find way to set this as its own command so it can be referenced while laser is firing.
int safetyflag() 
{
  
  int stat = digitalRead(estop); //read input pin
  
  if (stat == high);
    {
      //return flag value
      return 1;
    }
    
  stat = digitalRead(defeatsafety); //read input pin
  
  if (stat == high)
    {
      //return flag value
      return 2;
    }
  
  stat = digitalRead(safecircuit); //read input pin
  
  if (stat == low)
    {
      //return flag value
      return 3;
    }
      
  return 0; //pass through if no errors
}
