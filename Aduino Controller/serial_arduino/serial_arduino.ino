#include <Servo.h>

#define numOfValsRec 2
#define digitsPerValRec 3

int valsRec[numOfValsRec];
int stringLength = numOfValsRec * digitsPerValRec + 1;
int counter = 0;
bool counterStart = false;
String receivedString;
Servo myservoUD;
Servo myservoLR;
int pos = 0;   

void setup() {
  myservoUD.attach(10); 
  myservoLR.attach(9); 
  pinMode(13, OUTPUT);
  Serial.begin(9600);
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
//  if (valsRec[0] == 255){
//    digitalWrite(13, HIGH);
//  }
//  else {
//    digitalWrite(13, LOW);
//  }
//  for (pos = 0; pos <= 180; pos += 1) { 
//    myservoUD.write(pos); 
//    myservoLR.write(pos);             
//    delay(15);                       
//  }
//  for (pos = 180; pos >= 0; pos -= 1) { 
//    myservoUD.write(pos); 
//    myservoLR.write(pos);             
//    delay(15);                      
//  }

  
  myservoLR.write(valsRec[0]);
  myservoUD.write(valsRec[1]);  
  

  

}
