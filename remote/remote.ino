#include <IRremote.hpp>

#include <HID-Project.h>                  
#include <HID-Settings.h>
#define ir_pin 4


uint32_t remote_keyboard[] = {0xF708FF00, 0xA55AFF00};
KeyboardKeycode   keyboard_keys[] = {KEY_LEFT_ARROW, KEY_RIGHT_ARROW};

uint32_t remote_keyboard_typed[] = {0xE31CFF00};
char keyboard_keys_typed[] = {' '};

uint32_t remote_media[] = {0xE718FF00, 0xAD52FF00};
ConsumerKeycode media_keys[] = {MEDIA_VOLUME_UP, MEDIA_VOLUME_DOWN};

uint32_t current_key = 0;

int pressed = 0;

#define KEYBOARD_COUNT (sizeof(remote_keyboard) / sizeof(remote_keyboard[0]))
#define KEYBOARD_TYPED_COUNT (sizeof(remote_keyboard_typed) / sizeof(remote_keyboard_typed[0]))
#define MEDIA_COUNT    (sizeof(remote_media)    / sizeof(remote_media[0]))

void setup(){
  pinMode(LED_BUILTIN_RX, INPUT);
  pinMode(LED_BUILTIN_TX, INPUT);


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
    
    Serial.println(data, 16);

    if(!pressed){
      for (int i = 0; i < KEYBOARD_COUNT; i++){
        if (remote_keyboard[i] == current_key){
          Keyboard.press(keyboard_keys[i]);
          pressed = 1; 
          break; 
        }
      }

      for (int i = 0; i < KEYBOARD_TYPED_COUNT; i++){
        if (remote_keyboard_typed[i] == current_key){
          Keyboard.press(keyboard_keys_typed[i]);
          pressed = 1; 
          break; 
        }
      }


      for (int i = 0; i < MEDIA_COUNT; i++){
        if (remote_media[i] == current_key) {
          Consumer.write(media_keys[i]);
          break;
        }
      }
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