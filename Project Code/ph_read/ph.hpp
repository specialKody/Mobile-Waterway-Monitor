/**************************************************************************************/
// Authors: Kody Stribrny
// Department: CIDSE
// Semester: Fall 2016
// Course Number and Name: CSE 492/493 Honors Thesis
// Supervisors: Dr. Carole-Jean Wu & Dr. Sarma Vrudhula
/**************************************************************************************/

#include "Arduino.h"

#ifndef ph_hpp
#define ph_hpp

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

extern phClass ph;

#endif
