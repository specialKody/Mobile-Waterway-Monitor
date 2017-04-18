#include <SoftwareSerial.h>

SoftwareSerial fona = SoftwareSerial(2,3);  //substitute your rx and tx pins

void setup()
{
  Serial.begin(9600);
  fona.begin(9600);
}

void loop()
{
  if (Serial.available())
    fona.write(Serial.read());
  if (fona.available())
    Serial.write(fona.read());
}
