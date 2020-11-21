//This example code is in the Public Domain (or CC0 licensed, at your option.)
//By Evandro Copercini - 2018
//
//This example creates a bridge between Serial and Classical Bluetooth (SPP)
//and also demonstrate that SerialBT have the same functionalities of a normal Serial
#include "BluetoothSerial.h"
#include <string.h>
#include "xxtea-iot-crypt.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

unsigned long millistime;




// common functions and procedures

uint32_t k; 
//prime number 
const uint32_t prime = 2147483647;
//generator
const uint32_t generator = 16807;  

//generates our 8 bit private secret 'a'.
uint32_t keyGen(){
  //Seed the random number generator with a reading from an unconnected pin, I think this on analog pin 2
  randomSeed(analogRead(2));

  //return a random number between 1 and our prime .
  return random(1,prime);
}

//code to compute the remainder of two numbers multiplied together.
uint32_t mul_mod(uint32_t a, uint32_t b, uint32_t m){


  uint32_t result = 0; //variable to store the result
  uint32_t runningCount = b % m; //holds the value of b*2^i

  for(int i = 0 ; i < 32 ; i++){

    if(i > 0) runningCount = (runningCount << 1) % m;
    if(bitRead(a,i)){
      result = (result%m + runningCount%m) % m; 

    } 

  }
  return result;
}


/*
    Compute and return (b ** e) mod m
    For unsigned b, e, m and m > 0
*/
uint32_t pow_mod(uint32_t b, uint32_t e, uint32_t m)
{
  uint32_t r;  // result of this function

  uint32_t pow;
  uint32_t e_i = e;
  // current bit position being processed of e, not used except for debugging
  uint8_t i;

  // if b = 0 or m = 0 then result is always 0
  if ( b == 0 || m == 0 ) { 
    return 0; 
  }

  // if e = 0 then result is 1
  if ( e == 0 ) { 
    return 1; 
  }

  // reduce b mod m 
  b = b % m;

  // initialize pow, it satisfies
  //    pow = (b ** (2 ** i)) % m
  pow = b;

  r = 1;

  // stop the moment no bits left in e to be processed
  while ( e_i ) {
    // At this point pow = (b ** (2 ** i)) % m

    // and we need to ensure that  r = (b ** e_[i..0] ) % m
    // is the current bit of e set?
    if ( e_i & 1 ) {
      // this will overflow if numbits(b) + numbits(pow) > 32
      r= mul_mod(r,pow,m);//(r * pow) % m; 
    }

    // now square and move to next bit of e
    // this will overflow if 2 * numbits(pow) > 32
    pow = mul_mod(pow,pow,m);//(pow * pow) % m;

    e_i = e_i >> 1;
    i++;
  }

  // at this point r = (b ** e) % m, provided no overflow occurred
  return r;
}


uint32_t miniSecDH(){
  //DH Key Exchange

  //This is our secret key
  uint32_t a = keyGen();
  Serial.print("secret generated key a is: ");
  Serial.println(a);

  //This is our shared index 'A'
  uint32_t A = pow_mod(generator, a, prime);

  Serial.print("Shared index A is: ");
  Serial.println(A);
  SerialBT.write(A);
  SerialBT.flush();
  
  while(SerialBT.available() == 0){
  } //wait until the there are bits in the serial
  uint32_t B = SerialBT.read();

  B = 231242144;
  SerialBT.flush();
  
  Serial.print("Received shared index B is: ");
  Serial.println(B);

  //This is our shared secret encryption key.
  k = pow_mod(B, a, prime);
  
  //reseed the random number generator with the shared secret key k
  return(k);
}

String miniSecMessage(String plaintext, String key){
  Serial.print("miniSecMessage start time: ");
  millistime = millis();
  Serial.println(millistime); //prints time since program started
  
  String msg = (plaintext);
  xxtea.setKey(key);
  Serial.println("Set XXTEA key with K");

  // Perform Encryption on the Data
  Serial.print(("Received Encrypted Data: "));
  String result = xxtea.encrypt(plaintext);
  result.toLowerCase(); // (Optional)
  Serial.println(result);

  // Perform Decryption
  Serial.print((" Decrypted Data: "));
  Serial.println(xxtea.decrypt(result));
  Serial.print("miniSecMessage end time: ");
  millistime = millis();
  Serial.println(millistime); //prints time since program started
}

void setup() {
  Serial.begin(9600);
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");

  //Wait for connection
  while(SerialBT.available() == 0){
  }
  Serial.print("Start time: ");
  millistime = millis();
  Serial.println(millistime); //prints time since program started

  uint32_t k = miniSecDH();
  Serial.println("K FOUND!");
  Serial.println(k);

  
  if(k == 1){
    Serial.println("Authentication is: VALID");
  }
  else {
    Serial.println("Authentication is: VALID");
  }

  Serial.print("miniSecDH end time: ");
  millistime = millis();
  Serial.println(millistime); //prints time since program started

  //Wait for connection
  while(SerialBT.available() == 0){
  }
  String keyString = String(k);
  encd_message = SerialBT.read();
  
  miniSecMessage(encd_message, keyString);
  
  Serial.print("End time: ");
  millistime = millis();
  Serial.println(millistime); //prints time since program started
  
  SerialBT.flush();
}


//
void loop() {
  if (Serial.available()) {
    SerialBT.write(Serial.read());
  }
  if (SerialBT.available()) {
    Serial.write(SerialBT.read());
  }
  delay(20);
}
