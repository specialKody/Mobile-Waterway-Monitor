/**************************************************************************************/
// Project: Mobile Waterway Monitor
// Authors: Kody Stribrny
// Department: CIDSE
// Semester: Fall 2016/Spring 2017
// Course Number and Name: CSE 492/493 Honors Thesis
// Supervisors: Dr. Sarma Vrudhula & Dr. Carole-Jean Wu
// File Description:
//      Arduino sketch which controls the Mobile Waterway Monitor node
/**************************************************************************************/

// Inspired by the code from Tony DiCola and Marco Schwartz
// Released under a MIT license:
// https://opensource.org/licenses/MIT

// Libraries
#include <SoftwareSerial.h>
#include <Adafruit_SleepyDog.h>
#include <Adafruit_FONA.h>
#include <Adafruit_MQTT.h>
#include <Adafruit_MQTT_FONA.h>
#include "ph.hpp"

const int ph_sensor_pin = 0;    //pH meter analog pin
uint8_t txFailures = 0;         //Counts number of sequential publish failures
int timeSlept;                  //Record the time slept at each iteration
#define DEBUG_SKETCH    0       //If set to 1 print statements are activated

//Latitude & longitude for distance measurement
float latitude, longitude, speed_kph, heading, altitude;
//Battery value
uint16_t vbat;

//FONA pins configuration
//Note - Addtional pins can be defined for increased functionality
#define FONA_RX              2   //FONA serial RX pin
#define FONA_TX              3   //FONA serial TX pin
#define FONA_RST             4   //FONA reset pin

//FONA GSM infromation
#define FONA_APN             "epc.tmobile.com"  //APN used by cell data service (leave blank if unused)
#define FONA_USERNAME        ""                 //Username used by cell data service (leave blank if unused).
#define FONA_PASSWORD        ""                 //Password used by cell data service (leave blank if unused).

//Adafruit IO configuration
#define AIO_SERVER           "io.adafruit.com"                  //Adafruit IO server (io.adafruit.com)
#define AIO_SERVERPORT       1883                               //Adafruit IO port (always 1883)
#define AIO_USERNAME         "specialKody"                      //Adafruit IO username (user specific)
#define AIO_KEY              "72ee9687c081435b8c8cdd653cc8381a" //Adafruit IO key (user specific)

//Configuring the FONA instance
SoftwareSerial fonaSS = SoftwareSerial(FONA_TX, FONA_RX);     //FONA software serial connection.
Adafruit_FONA fona = Adafruit_FONA(FONA_RST);                 //FONA library connection.

//Create the MQTT FONA fobject by supplying FONA class and Adafruit IO info
Adafruit_MQTT_FONA mqtt(&fona, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

//Adafruit IO data feeds parameters
#define LOCATION_PH_FEED_NAME      "RIVER_NODE_LOCATION_PH" //Feed which logs river node location and pH value
#define MAX_TX_FAILURES      3                              //Maximum number of sequential publish failures before resetting

//Adafruit IO data feeds
Adafruit_MQTT_Publish location_ph_feed = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/" LOCATION_PH_FEED_NAME "/csv");
Adafruit_MQTT_Publish battery_feed = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/battery");

//Initializes the GSM and FONA connections. Also readies the watchdog timer along with the pH meter.
void setup() {
  Serial.begin(115200);                                             //Initialize serial output at the specified baud rate
  #if DEBUG_SKETCH 
    Serial.println(F("River Node Setting Up"));
  #endif
  ph.phSetup(ph_sensor_pin);                                        //Sets up the pH meter connection

  Watchdog.enable(10000);                                           //Set watchdog timeout for 10 seconds (FONA connection <10s)
  Watchdog.reset();                                                 //Reset watchdog countdown
  

  // Initialize the FONA module
  #if DEBUG_SKETCH
    Serial.println(F("Initializing FONA....(may take 10 seconds)"));
  #endif
  fonaSS.begin(4800);                       //FONA serial connection baud rate
  if (!fona.begin(fonaSS)) {                //If no connection could be made, halt until watchdog reset
    halt(F("Couldn't find FONA"));          //Print error message when halting                                  
  }
  fonaSS.println("AT+CMEE=2");              //Send command to FONA
  #if DEBUG_SKETCH
    Serial.println(F("FONA is OK"));
  #endif
  Watchdog.reset();                         //Reset watchdog countdown

  #if DEBUG_SKETCH
    Serial.println(F("Checking for network..."));                   //Print debug status
  #endif
  while(!(fona.getNetworkStatus())) {                               //While fona isn't connected
   delay(500);                                                      //Delay half a second and try again
  }

  Watchdog.reset();                             //Reset the watchdog countdown
  fona.enableGPS(true);                         //Enable GPS
  fona.setGPRSNetworkSettings(F(FONA_APN));     //Start the GPRS data connection.
  delay(2000);                                  //Delay 2 seconds once the GPRS connection parameters are set
  Watchdog.reset();                             //Reset the watchdog countdown
  #if DEBUG_SKETCH
    Serial.println(F("Disabling GPRS"));
  #endif
  fona.enableGPRS(false);                       //Don't know if GPRS is enabled or enabled, default to disabled
  delay(2000);                                  //Delay another 2 seconds once GPRS module disabled
  Watchdog.reset();                             //Reset the watchdog countdown
  #if DEBUG_SKETCH
    Serial.println(F("Enabling GPRS"));
  #endif
  if (!fona.enableGPRS(true)) {                         //Reenable GPRS. Halt if enable fails
    halt(F("Failed to turn GPRS on, resetting..."));
  }
  #if DEBUG_SKETCH
    Serial.println(F("Connected to Cellular!"));
  #endif

  Watchdog.reset();                             //Reset the watchdog countdown
  delay(3000);                                  //Delay to stabilize connection

  int8_t ret = mqtt.connect();                  //Now attempt to make connection with stable network
  if (ret != 0) {                               //If connection didn't work, reset
   #if DEBUG_SKETCH
    Serial.println(mqtt.connectErrorString(ret));
   #endif
    halt(F("MQTT connection failed, resetting..."));
  }
  #if DEBUG_SKETCH
    Serial.println(F("MQTT Connected!"));
  #endif
  Watchdog.reset();                             //Reset the watchdog countdown
  
}

//Loop will now continually read and transmit values to the MQTT server
void loop() {
  Watchdog.reset();     //Reset the watchdog countdown (just in case setup->loop transition takes longer than expected)
  
  //If not connected or too many transmit failures, wait for watchdog reset
  if (!fona.TCPconnected() || (txFailures >= MAX_TX_FAILURES)) {        
    halt(F("Connection lost, resetting..."));
  }
  
  ph.phRead();                                                                          //Read in the PH value
  bool gpsFix = fona.getGPS(&latitude, &longitude, &speed_kph, &heading, &altitude);    //Get GPS reading
  fona.getBattPercent(&vbat);                                                           //Get battery percent

  log_ph_loc(ph.getPH(),latitude, longitude, altitude, location_ph_feed);               //Log PH & location to pH_Location feed
  logBatteryPercent(vbat, battery_feed);                                                //Log battery life to battery feed
  
  timeSlept = Watchdog.sleep(5000);                                                     //Sleep system and watchdog for 5 seconds
}

//Publishes battery life percentage to battery feed
void logBatteryPercent(uint32_t indicator, Adafruit_MQTT_Publish& publishFeed) {
  #if DEBUG_SKETCH
    Serial.print(F("Publishing battery percentage: "));
    Serial.println(indicator);
  #endif
  if (!publishFeed.publish(indicator)) {                    //Publish failed, increment failed count
    #if DEBUG_SKETCH
        Serial.println(F("Publish failed!"));
    #endif
    txFailures++;
  }
  else {                                                    //Publish succeeded, reset to zero
    #if DEBUG_SKETCH
        Serial.println(F("Publish succeeded!"));
    #endif
    txFailures = 0;
  }
  
}

//Publishes pH and location information to pH/Location feed.
//Message sends data in CSV format.
void log_ph_loc(float phVal,float latitude, float longitude, float altitude, Adafruit_MQTT_Publish& publishFeed){
  char sendBuffer[120];                             //Stores the message to be send
  memset(sendBuffer, 0, sizeof(sendBuffer));        //Clear the entire buffer
  int index = 0;                                    //Reset index to buffer head
  
  //pH value is sent as first value in CSV list
  dtostrf(phVal, 4, 3, &sendBuffer[index]);         //Appends float characters to buffer (4 character excluding period with three after decimal)
  index += strlen(&sendBuffer[index]);              //Move the index forward by the appended length
  sendBuffer[index++] = ',';                        //Append a comma and move index forward one space
  
  //Similar pattern as above for latitude, longtitude, and altitude
  dtostrf(latitude, 2, 6, &sendBuffer[index]);
  index += strlen(&sendBuffer[index]);
  sendBuffer[index++] = ',';
  dtostrf(longitude, 3, 6, &sendBuffer[index]);
  index += strlen(&sendBuffer[index]);
  sendBuffer[index++] = ',';
  dtostrf(altitude, 2, 6, &sendBuffer[index]);

  //Send the character buffer to the website over the connection
  #if DEBUG_SKETCH
      Serial.print(F("Publishing location: "));
      Serial.println(sendBuffer);
  #endif
  if (!publishFeed.publish(sendBuffer)) {                   //If publish failed, increment failed counter
    #if DEBUG_SKETCH
        Serial.println(F("Publish failed!"));
    #endif
    txFailures++;
  }
  else {                                                    //Else, reset counter to zero
    #if DEBUG_SKETCH
    Serial.println(F("Publish succeeded!"));
    #endif
    txFailures = 0;
  }
}

// Halt function called when an error occurs. Relies upon watchdog reset.
void halt(const __FlashStringHelper *error) {
  #if DEBUG_SKETCH
    Serial.println(error);                  //Prints the passed in message
  #endif
  while(1);                                 //Busy loop until watchdog reset
}
