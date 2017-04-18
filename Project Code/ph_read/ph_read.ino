/**************************************************************************************/
// Authors: Kody Stribrny
// Department: CIDSE
// Semester: Fall 2016
// Course Number and Name: CSE 492/493 Honors Thesis
// Supervisors: Dr. Carole-Jean Wu & Dr. Sarma Vrudhula
/**************************************************************************************/

#include "ph.hpp"

/**************************************************************************************/
// Defined Values
/**************************************************************************************/
#define SensorPin 0          //pH meter Analog output to Arduino Analog Input 0
unsigned long int avgValue;  //Store the average value of the sensor feedback
float b;
int buf[10],temp;

/**************************************************************************************/
// Setup
/**************************************************************************************/
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  ph.phSetup(SensorPin);

}

/**************************************************************************************/
// Main Loop
/**************************************************************************************/
void loop() {
  // put your main code here, to run repeatedly
  ph.phRead();
  Serial.println(ph.getPH(),2);
  delay(5000);
}

float readPh(){
   
}

