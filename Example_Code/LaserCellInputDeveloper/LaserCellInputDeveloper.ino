uint8_t SerialOutBuffer[4]={0};
uint32_t inputs = 0;
uint32_t lastInputs = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial) {}  // wait for serial port to connect. Needed for native USB port only
  pinMode(2, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  pinMode(8, INPUT_PULLUP);
  pinMode(9, INPUT_PULLUP);
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(14, INPUT_PULLUP);
  pinMode(15, INPUT_PULLUP);
  pinMode(16, INPUT_PULLUP);
  pinMode(17, INPUT_PULLUP);
  pinMode(18, INPUT_PULLUP);
  pinMode(19, INPUT_PULLUP);
}

void loop() {
  if (checkInputs()) {
    printBytes(inputs);

  }
}

bool checkInputs() {
  static uint32_t lastInputs = 0;
  bitWrite(inputs, 0, !digitalRead(10));
  bitWrite(inputs, 1, !digitalRead(11));
  bitWrite(inputs, 2, !digitalRead(A5));
  bitWrite(inputs, 3, !digitalRead(A4));
  bitWrite(inputs, 4, !digitalRead(A3));
  bitWrite(inputs, 5, !digitalRead(A2));
  bitWrite(inputs, 6, !digitalRead(A1));
  bitWrite(inputs, 7, !digitalRead(A0));

  bitWrite(inputs, 8, !digitalRead(2));
  bitWrite(inputs, 9, !digitalRead(3));
  bitWrite(inputs, 10, !digitalRead(4));
  bitWrite(inputs, 11, !digitalRead(5));
  bitWrite(inputs, 12, !digitalRead(6));
  bitWrite(inputs, 13, !digitalRead(7));
  bitWrite(inputs, 14, !digitalRead(8));
  bitWrite(inputs, 15, !digitalRead(9));
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

void printBytes(uint32_t myByte) {
  SerialOutBuffer[0]=inputs&0xFF;
  SerialOutBuffer[1]=(inputs>>8)&0xFF;
  SerialOutBuffer[2]=(inputs>>16)&0xFF;
  SerialOutBuffer[3]=(inputs>>24)&0xFF;
  Serial.write(SerialOutBuffer,4);

}
