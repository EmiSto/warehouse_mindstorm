#include <SoftwareSerial.h>

const int rxpin = 19;
const int txpin = 18;
char k = 'L';
SoftwareSerial bluetooth(rxpin, txpin);

void setup()
{
  pinMode(7, OUTPUT);
  bluetooth.begin(9600);
}

void loop()
{
  if(bluetooth.available()){
    k = bluetooth.read();
  }
  if( k == 'H' ){
    digitalWrite(7, HIGH);
  }
  else if (k == 'L')  {
    digitalWrite(7, LOW);
  }
   delay(10);
}
