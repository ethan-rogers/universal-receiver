
media_codes = {

    "pause"  : "MEDIA_PAUSE",
    "play" : "MEDIA_PLAY_PAUSE",
    "backward" : "MEDIA_REWIND",
    "forward" : "MEDIA_FAST_FORWARD",
    "skip <-" : "MEDIA_NEXT",
    "skip ->" : "MEDIA_PREVIOUS",
    "stop" : "MEDIA_STOP",
    "mute" : "MEDIA_VOLUME_MUTE", 
    "vol +" : "MEDIA_VOLUME_UP",
    "vol -" : "MEDIA_VOLUME_DOWN",

}

keyboard_keycodes = {
    "esc" : "KEY_ESC",
    "F1" : "KEY_F1", 
    "F2" : "KEY_F2", 
    "F3" : "KEY_F3", 
    "F4" : "KEY_F4", 
    "F5" : "KEY_F5", 
    "F6" : "KEY_F6", 
    "F7" : "KEY_F7", 
    "F8" : "KEY_F8", 
    "F9" : "KEY_F9", 
    "F10" : "KEY_F10", 
    "F11" : "KEY_F11", 
    "F12" : "KEY_F12", 
    "del" : "KEY_DELETE", 
    "backspace" : "KEY_BACKSPACE",
    "tab" : "KEY_TAB",
    "caps" : "KEY_CAPS_LOCK",
    "enter" : "KEY_RETURN",
    "shift" : "KEY_LEFT_SHIFT",
    "ctrl" : "KEY_LEFT_CTRL",
    "alt" : "KEY_LEFT_ALT",
    "wdw" : "KEY_LEFT_GUI",
    "up" : "KEY_UP_ARROW",
    "left" : "KEY_LEFT_ARROW",
    "right" : "KEY_RIGHT_ARROW",
    "down" : "KEY_DOWN_ARROW"
}

typed_keycodes = {
    "space" : "' '",
    "\\" : "'\\\\'",

}

# Note: The difference is in the Arduino library some keys have to be stored as Keycode type while others have to be types.

keyboard_codes = {}

keyboard_keys = {}

def reconfig(mapping):
    print("Attempting")
    replace_keyboard_keys = "{"
    replace_keyboard_keys_typed  = "{"
    replace_media_keys = "{"

    replace_remote_keyboard = "{"
    replace_remote_keyboard_typed  = "{"
    replace_remote_media = "{"

    for m in mapping:
        code, keys = m
        print(code,keys)
        for key in keys:
            if key in media_codes:
                replace_media_keys += media_codes[key] + ", "
                replace_remote_media += "0x" + code + ", "
            elif key in keyboard_keycodes:
                replace_keyboard_keys += keyboard_keycodes[key] + ", "
                replace_remote_keyboard += "0x" + code + ", "
            elif key in typed_keycodes:
                replace_keyboard_keys_typed += typed_keycodes[key] + ", "
                replace_remote_keyboard_typed += "0x" + code + ", "
            else:
                replace_keyboard_keys_typed += key + ", "
                replace_remote_keyboard_typed += "0x" + code + ", "

    if replace_keyboard_keys != '{':
        replace_keyboard_keys = replace_keyboard_keys[:-2]

    if replace_keyboard_keys_typed != '{':
        replace_keyboard_keys_typed = replace_keyboard_keys_typed[:-2]

    if replace_media_keys != '{':
        replace_media_keys = replace_media_keys[:-2]

    replace_keyboard_keys += '}'
    replace_keyboard_keys_typed += '}'
    replace_media_keys += '}'

    if replace_remote_keyboard != '{':
        replace_remote_keyboard = replace_remote_keyboard[:-2]

    if replace_remote_keyboard_typed != '{':
        replace_remote_keyboard_typed = replace_remote_keyboard_typed[:-2]

    if replace_remote_media != '{':
        replace_remote_media = replace_remote_media[:-2]

    replace_remote_keyboard += '}'
    replace_remote_keyboard_typed += '}'
    replace_remote_media += '}'
    code = ""

    print("Opening Files")

    with open("mapper/remote_boiler.ino", "r") as file:
        print("Boiler Opened")
        code = file.read()
        code = code.replace("replace_remote_keyboard", replace_remote_keyboard)
        code = code.replace("replace_remote_typed", replace_remote_keyboard_typed)
        code = code.replace("replace_remote_media", replace_remote_media)

        code = code.replace("replace_keyboard_keys", replace_keyboard_keys)
        code = code.replace("replace_keyboard_typed", replace_keyboard_keys_typed)
        code = code.replace("replace_media_keys", replace_media_keys)
    
    with open("remote/remote.ino", "w") as file:
        print("Reak Opened")
        file.write(code)
        










def upload():
    pass