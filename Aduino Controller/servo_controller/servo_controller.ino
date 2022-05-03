#include <Servo.h>

Servo myservoUD;
Servo myservoLR;
int pos = 0;   

void setup() {
  myservoUD.attach(10); 
  myservoLR.attach(9); 
}

void loop() {
  for (pos = 0; pos <= 180; pos += 1) { 
    myservoUD.write(pos); 
    myservoLR.write(pos);             
    delay(15);                       
  }
  for (pos = 180; pos >= 0; pos -= 1) { 
    myservoUD.write(pos); 
    myservoLR.write(pos);             
    delay(15);                      
  }
}
