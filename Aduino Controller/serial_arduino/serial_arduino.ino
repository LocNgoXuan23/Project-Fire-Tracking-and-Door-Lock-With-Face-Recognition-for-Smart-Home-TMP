#include <Servo.h>

#define numOfValsRec 3
#define digitsPerValRec 3

int red_light_pin= 5;
int green_light_pin = 6;
int blue_light_pin = 7;

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1;
int counter = 0;
bool counterStart = false;
String receivedString;

Servo myservoUD;
Servo myservoLR;
int pos = 0;  
int LRPos = 90;
int UDPos = 90; 

void setup() {
  pinMode(red_light_pin, OUTPUT);
  pinMode(green_light_pin, OUTPUT);
  pinMode(blue_light_pin, OUTPUT);
  myservoUD.attach(10); 
  myservoLR.attach(9); 
  pinMode(13, OUTPUT);
  Serial.begin(9600);
}

void RGB_color(int red_light_value, int green_light_value, int blue_light_value)
 {
  analogWrite(red_light_pin, red_light_value);
  analogWrite(green_light_pin, green_light_value);
  analogWrite(blue_light_pin, blue_light_value);
}

void receiveData() {
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '$') {
      counterStart = true;
    }
    if (counterStart) {
      if (counter < stringLength) {
        receivedString = String(receivedString + c);
        counter ++;
      }
      if (counter >= stringLength) {
        for (int i = 0; i < numOfValsRec; i++) {
          int num = (i * digitsPerValRec) + 1;
          valsRec[i] = receivedString.substring(num, num + digitsPerValRec).toInt();

        }
        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}



void loop() {
  receiveData(); 
  
  if (valsRec[0] == 0) {
    LRPos = LRPos;
  }
  if (valsRec[0] == 1) {
    if (LRPos < 180) {
      LRPos = LRPos + 1;
    }
  }
  if (valsRec[0] == 2) {
    if (LRPos > 0) {
      LRPos = LRPos -1;
    }
  }

  if (valsRec[1] == 0) {
    UDPos = UDPos;
  }
  if (valsRec[1] == 1) {
    if (UDPos < 180) {
      UDPos = UDPos + 1;
    }
  }
  if (valsRec[1] == 2) {
    if (LRPos > 0) {
      UDPos = UDPos -1;
    }
  }

  if (valsRec[2] == 0) {
    RGB_color(0, 255, 0);
  }
  if (valsRec[2] == 1) {
    RGB_color(255, 0, 0);
  } 
  
//  Serial.print(LRPos);
//  Serial.print("-");
//  Serial.print(UDPos);
//  Serial.print("\n");

  Serial.print(valsRec[0]);
  Serial.print("-");
  Serial.print(valsRec[1]);
  Serial.print("-");
  Serial.print(valsRec[2]);
  Serial.print("-");
  Serial.print("\n");

  myservoLR.write(LRPos);
  myservoUD.write(UDPos); 

  delay(50);
  

}
