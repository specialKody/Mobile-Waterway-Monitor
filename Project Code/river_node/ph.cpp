/**************************************************************************************/
// Project: Mobile Waterway Monitor
// Authors: Kody Stribrny
// Department: CIDSE
// Semester: Fall 2016/Spring 2017
// Course Number and Name: CSE 492/493 Honors Thesis
// Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
// File Description:
// 		C++ file which impelements ph class functionality.
/**************************************************************************************/

#include "ph.hpp"

//Default constructor with pin 0 assumed as well as a perfectly balanced ph
phClass::phClass(){
  this->pin = 0;
  this->value = 7.00;
}

//Setup method which overrides the input/output pin
void phClass::phSetup(uint8_t pin){
  this->pin = pin;
}

//Reads several values from the pH meter, averages, and then sets the private
//ph value data member.
void phClass::phRead(){
  int buf[10];					//Integer buffer used to average store 10 reads
  int temp;						//Integer for later sorting
  unsigned long int avgValue;	//Unprocessed average pH value from pH meter

  for(int i=0; i<10; i++){		//Reads in 10 pH values with a 10ms delay between each read
    buf[i] = analogRead(pin);
    delay(10);
  }
  //Selection sort which orders the 10 values from smallest to largest
  for(int i=0;i<9;i++){
    for(int j=i+1;j<10;j++){
      if(buf[i]>buf[j]){
        temp=buf[i];
        buf[i]=buf[j];
        buf[j]=temp;
      }
    }
  }
  avgValue=0;					//Clears the average value
  for(int i=2; i<8; i++)		//Sums the middle 6 values
    avgValue += buf[i];

  //Processes the large integer into a floating point representation which is stored in value
  value = (float)avgValue * 17.5/1024/6;
}

float phClass::getPH(){
  return this->value;
}

void phClass::setPH(float phValue){
  this->value = phValue;
}

//Instantiates the extern ph object delared in the header file
phClass ph = phClass();
