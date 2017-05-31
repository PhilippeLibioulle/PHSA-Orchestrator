#include "Adafruit_NeoPixel.h"
#ifdef __AVR__
  #include <avr/power.h>
#endif

/*
Fixed length messages, 10 bytes long

Byte    Description

0       Always 0x02   (= begin of message)
1       Command
2-9     Parameters


Command     Description       Parameters

0x10        All OFF           None (all 00)
0x20        Selftest          None (all 00)
0x30        Setup one led     Position, Color 
0x40        ProgressBar       Progress, Color 
0x50        Set brightness    Brightness 


Position = 1 byte (1 = the first LED, starting from the left)
Color =  3 bytes (R, G & B)
Brightness = 1 byte, percentage, between 0 and 100
Progress = 1 byte, percentage between 0 and 100


Examples

0x02 0x30 0x04 0x00 0xFF 0x00 0x00 0x00 0x00 0x00     = turn LED 4 to 100% green
0x02 0x40 0x50 0xFF 0x00 0x00 0x00 0x00 0x00 0x00     = show 50% progress bar (i.e 4 LEDs) in 100% red  

*/

const int LEDCOUNT = 8;   // LED 7 is the first one on the left, LED 0 is the first one on the right
const int ARRAYSIZE = 10;
const int TIMEOUT = 2000; //in millisec  

int inByte[ARRAYSIZE]= {0,0,0,0,0,0,0,0,0,0};    // for storing incoming serial bytes
int startByte = 0x02;                            // Every message begins with this
int i = 0;              

Adafruit_NeoPixel leds = Adafruit_NeoPixel(8, 5, NEO_GRB + NEO_KHZ800);

void printRawData(byte b, int index)
{
  Serial.print(F("Index = "));
  Serial.print(index);
  Serial.print(F(" Value = ["));
  Serial.print(b, HEX);   
  Serial.println(F("]"));  
}

void resetArray()
{ 
   // Serial.println(F("Reset array"));
   for(int j=0;j<ARRAYSIZE;j++) 
   { 
      // Serial.print(j);
       inByte[j] = 0;
   };
   // Serial.println(F("Reset array completed"));
} 

int receiveMessageFromDragon()
{
   long start_time = millis();  
   int currentIndex = 0;     
   resetArray(); 
   byte currentByte;     
      
   while (true)
   {
      if ((millis() - start_time) > TIMEOUT)  // we should get a complete message in a short period of time
      {
        Serial.println(F("Error - communication lost..."));
	      return 2;
      };
      if (Serial.available() > 0)
      {
         currentByte = Serial.read();
         inByte[currentIndex] = currentByte;
                          
         printRawData(currentByte, currentIndex);
         
         if (currentIndex == 0 && currentByte != startByte)  // a new message should always start with the specified start byte
         {
            Serial.println(F("Error - message should start with 0x02..."));
	          return 2;
         }; 
         if (currentIndex > (ARRAYSIZE - 1) )   // message looks longer than expected
         {
            Serial.println(F("Error - message looks longer than expected..."));
            return 4; 
         };       
         if (currentIndex == (ARRAYSIZE - 1) ) // message has been received as expected
         {
            Serial.println(F("Message received..."));
            return 0;  // full message received
         }; 
         currentIndex = currentIndex + 1;  // just keep going with parsing         
      };
   };   
}

void ledsTest()
{  
  Serial.println(F("LED self test"));  
  for (int i=7; i>=0; i--)
  {  
     leds.setPixelColor(i, 0x00FF00);    // Full green 
     leds.show();
     delay(50);	 
  };
  for (int i=7; i>=0; i--)
  {  
     leds.setPixelColor(i, 0x000000);    // Full green 
     leds.show();    	 
  };    
}

void ledsReset()
{  
  Serial.println(F("LED reset"));
  for (int i=7; i>=0; i--)
  {  
     leds.setPixelColor(i, 0x000000);   // all OFF     	 
  }  
  leds.show();
}

void setupOneLed()
{  
  Serial.println(F("Setup one single LED"));
  leds.setPixelColor(inByte[2],inByte[3],inByte[4],inByte[5]);  // first parameter is between 0 and 9 and indicates which LED you are setting.
                                                                // next 3 parms are red/green/blue that vary between 0 (off) and 255 (full on)
  leds.show();  
} 

void showProgress()
{  
  Serial.println(F("Progress bar"));
  for (int i=7; i>=0; i--)
  {  
     leds.setPixelColor(i, 0x000000);   // all OFF     	 
  } 
  int upTo = map(inByte[2], 0, 100, 0, 7) - 1; 
  // Serial.println(upTo); 
  for (int i=7; i>=upTo; i--)
  {  
     leds.setPixelColor(i, inByte[3], inByte[4], inByte[5]);   
  }   
  leds.show();
} 

void setBrigthness() 
{
  leds.setBrightness(inByte[2]);
  leds.show();
}

void processCommand()
{  
   switch (inByte[1])
   {  
      case 0x10:  // all OFF
	       ledsReset();
         break;
	    case 0x20:  // test all LEDs
	       ledsTest();
         break;
	    case 0x30:  // control a single LED
	       setupOneLed();
         break;
	    case 0x40:  //  control LED array as a it was a progress bar
	       showProgress();		
         break;
      case 0x50:  // set brightness
         setBrigthness();
         break;   
      default:
         Serial.println(F("Unknown command..."));	  
   };  
}

void setup()
{  
   Serial.begin(9600);        
   Serial.println(F("Begin of setup."));  
   leds.begin();
   leds.setBrightness(50);
   leds.show();
   ledsTest();   
   delay(1000);  
   Serial.println(F("Setup completed, now waiting for new messages..."));   
}

void loop()
{  
   while (Serial.available() > 0)       
   {      
     if (receiveMessageFromDragon() == 0) // message received and compliant with message type definition
     {
        processCommand();  
        resetArray();     
     };          
  };
}
