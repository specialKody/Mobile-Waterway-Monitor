/**************************************************************************************/
// Authors: Kody Stribrny
// Department: CIDSE
// Semester: Fall 2016
// Course Number and Name: CSE 492/493 Honors Thesis
// Supervisors: Dr. Carole-Jean Wu & Dr. Sarma Vrudhula
/**************************************************************************************/

#include "ph.hpp"

phClass::phClass(){
  this->pin = 0;
  this->value = 7.00;
}

void phClass::phSetup(uint8_t pin){
  this->pin = pin;
}

void phClass::phRead(){
  int buf[10];
  int temp;
  unsigned long int avgValue;

  for(int i=0; i<10; i++){
    buf[i] = analogRead(pin);
    delay(10);
  }
  for(int i=0;i<9;i++){        //sort the analog from small to large
    for(int j=i+1;j<10;j++){
      if(buf[i]>buf[j]){
        temp=buf[i];
        buf[i]=buf[j];
        buf[j]=temp;
      }
    }
  }
  avgValue=0;
  for(int i=2; i<8; i++)
    avgValue += buf[i];

  value = (float)avgValue * 17.5/1024/6;
}

float phClass::getPH(){
  return this->value;
}

void phClass::setPH(float phValue){
  this->value = phValue;
}

phClass ph = phClass();
