#include<SoftwareSerial.h> //Included SoftwareSerial Library
SoftwareSerial s(3,1);

void setup() {
  //Serial S Begin at 9600 Baud
  s.begin(9600);
}

void loop() {
  //Write '123' to Serial
  s.write(123);
  delay(1000);
}
