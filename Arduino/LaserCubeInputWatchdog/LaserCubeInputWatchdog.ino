#include <Wire.h>


#define CONTACT_FROM_PI           170
#define GOOD_RESPONSE_FROM_PI     85
#define PACKET_END_BYTE           170


long previousMillis = 0;
long contactfromPi_timeout = 1000;
bool contactfromPi = false;
bool expectingResponsefromPi = false;

uint32_t inputs = 0;

void setup() {
  pinMode(0, OUTPUT);
  pinMode(1, OUTPUT);
  pinMode(A5, INPUT_PULLUP);
  pinMode(A4, INPUT_PULLUP);
  pinMode(A3, INPUT_PULLUP);
  pinMode(A2, INPUT_PULLUP);
  pinMode(A0, INPUT_PULLUP);
  pinMode(A1, INPUT_PULLUP);
  for (uint8_t pin = 4; pin < 14 ; pin++) {
    pinMode(pin, INPUT_PULLUP);
  }
  Wire.begin();
  Serial.begin(500000);
}

void loop() {

  //Handle anything in the serial port
  while (Serial.available()) {
    byte inByte = Serial.read();
    if (inByte == CONTACT_FROM_PI) {
      contactfromPi = true;
      sendBytes(inputs);
      digitalWrite(0,HIGH);
    }
    if (inByte == GOOD_RESPONSE_FROM_PI) {
      expectingResponsefromPi = false;
      digitalWrite(1,HIGH);
    }

  }

  //Make sure the PI is not unresponsive
  if (contactfromPi && expectingResponsefromPi) {
    if (millis() - previousMillis > contactfromPi_timeout) {
      noResponseTimeout();
    }
  }


  //Check inputs and send bytes if any changes
  if (checkInputs()) {
    //printBits(inputs, 16);
    sendBytes(inputs);
  }

}

bool checkInputs() {
  static uint32_t lastInputs = 0;
  bitWrite(inputs, 0, !digitalRead(A0));
  bitWrite(inputs, 1, !digitalRead(A1));
  bitWrite(inputs, 2, !digitalRead(4));
  bitWrite(inputs, 3, !digitalRead(5));
  bitWrite(inputs, 4, !digitalRead(6));
  bitWrite(inputs, 5, !digitalRead(7));
  bitWrite(inputs, 6, !digitalRead(8));
  bitWrite(inputs, 7, !digitalRead(9));
  bitWrite(inputs, 8, !digitalRead(10));
  bitWrite(inputs, 9, !digitalRead(11));
  bitWrite(inputs, 10, !digitalRead(12));
  bitWrite(inputs, 11, !digitalRead(13));
  bitWrite(inputs, 12, !digitalRead(A2));
  bitWrite(inputs, 13, !digitalRead(A3));
  bitWrite(inputs, 14, !digitalRead(A4));
  bitWrite(inputs, 15, !digitalRead(A5));
  if (inputs != lastInputs) {
    lastInputs = inputs;
    return 1;
  }
  else
  {
    return 0;
  }
}

void printBits(uint32_t myByte, uint32_t numBits) {
  for (uint32_t mask = pow(2, numBits - 1); mask; mask >>= 1) {
    if (mask  & myByte)
      Serial.print("1");
    else
      Serial.print("0");
  }
  Serial.println();
}

void sendBytes(uint32_t uint32num) {
  uint8_t SerialOutBuffer[3] = {0};
  SerialOutBuffer[0] = uint32num & 0xFF;
  SerialOutBuffer[1] = (uint32num >> 8) & 0xFF;
  SerialOutBuffer[2] = PACKET_END_BYTE;
  Serial.write(SerialOutBuffer, 3);
  expectingResponsefromPi = true;
  previousMillis = millis();
  digitalWrite(1,LOW);
}

void noResponseTimeout() {
  digitalWrite(0,LOW);
  //tell watchdog to reset the Pi
  //Wire.beginTransmission(44); // transmit to device #44 (0x2c)
  //Wire.write(byte(0x00));            // sends instruction byte
 // Wire.write(val);             // sends potentiometer value byte
 // Wire.endTransmission();     // stop transmitting

}
