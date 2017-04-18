/**************************************************************************************/
// Project: Mobile Waterway Monitor
// Authors: Kody Stribrny
// Department: CIDSE
// Semester: Fall 2016/Spring 2017
// Course Number and Name: CSE 492/493 Honors Thesis
// Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
// File Description:
// 		Header file for ph class. The ph class contains all functionality needed to 
//		successfully read data, store data, and setup the pH probe.
/**************************************************************************************/

#include "Arduino.h"

#ifndef ph_hpp
#define ph_hpp

//Defines the phClass type whic hcontains several public functions along which manipulate
//private data.
class phClass{
  public:
    phClass();
    void phSetup(uint8_t pin);
    void phRead();
    float getPH();
    void setPH(float phValue);
  private:
    float value;
    uint8_t pin;
};

//Declares an external ph object which can be used where this file is included
extern phClass ph;

#endif
