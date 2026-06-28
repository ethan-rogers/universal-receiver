#include <IRremote.hpp>
//#include "Keyboard.h"

#include <HID-Project.h>                    //include HID_Project library
#include <HID-Settings.h>
#define ir_pin 4

const uint32_t up = 0xE718FF00;
const uint32_t down = 0xAD52FF00;
const uint32_t left = 0xF708FF00;
const uint32_t right = 0xA55AFF00;

// center
uint32_t remote_keys[] = {0xE31CFF00};
uint32_t keyboard_keys[] = {32};
const int COUNT = 1;


uint32_t current_key = 0;

int pressed = 0;

void setup(){
  // turn off RX and TX LED pins  
  pinMode(LED_BUILTIN_RX, INPUT);
  pinMode(LED_BUILTIN_TX, INPUT);

  // init media
  Consumer.begin(); 
  Keyboard.begin();
  IrReceiver.begin(ir_pin);
  Serial.begin(9600);
}

void loop() {
  if (IrReceiver.decode()) {
    uint32_t  data = IrReceiver.decodedIRData.decodedRawData;
    IrReceiver.resume();
    if (data != 0) current_key = data;
    
    

    if(!pressed){
      for (int i = 0; i < COUNT; i++){
        if (remote_keys[i] == current_key){
          Keyboard.press(keyboard_keys[i]);
          pressed = 1;
          Serial.print("Pressed: ");
          Serial.println(keyboard_keys[i]);

          break; 
        }
      }
    }

    switch (current_key){
      case up:
        Consumer.write(MEDIA_VOLUME_UP);
        break;
      case down:
        Consumer.write(MEDIA_VOLUME_DOWN);
        break;
      case left:
        Consumer.write(MEDIA_PREVIOUS); 
        break;
      case right:
        Consumer.write(MEDIA_NEXT);
        break;
    }   
  }else{
    if(pressed){
      Keyboard.releaseAll();
      pressed = 0;
    }

    current_key = 0;
  }

  delay(150);
}
