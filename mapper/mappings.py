from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from uploader import Upload

import time

replacements = {

    "SP_MediaPause" : "pause",
    "SP_MediaPlay" : "play",
    "SP_MediaSeekBackward": "backward",
    "SP_MediaSeekForward" : "forward",
    "SP_MediaSkipBackward" : "skip <-",
    "SP_MediaSkipForward" : "skip ->",
    "SP_MediaStop" : "stop",
    "mute.png" : "mute", 
    "volume-down.png" : "vol +",
    "volume-up.png" : "vol -",
    "<-" :"backspace",
    "___" : "space",
    "^" : "up",
    "<" : "left",
    ">" : "right",
    " v ": "down"
}

class Mapping:
    def __init__(self):
        self.mapping = []
        self.code = None
        self.keys = []
        self.command = None
        self.table = None
        self.arduino = None
        self.threadpool = None
        self.upload = Upload()
        self.mapping_size = 8
    
    def set_command(self, command):
        self.command = command
    
    def set_arduino(self, arduino):
        self.arduino = arduino
        self.upload.set_arduino(arduino)
    
    def set_table(self, table):
        self.table = table

    def set_thread(self, threadpool):
        self.threadpool = threadpool

    def clear(self):
        self.keys = []
        self.code = None

        self.update_keys()
        self.update_code()

    def incomplete(self):
        return len(self.keys) == 0 or self.code == None

    def keys_to_string(self, keys):
        key_str = "" 

        for i, k in enumerate(keys):

            key_str += k

            if i != len(keys) - 1:
                key_str += " + "

        return key_str
    
    def get_keys(self):
        return self.keys_to_string(self.keys)
    
    def update_table(self):
        print(self.mapping)
        for i, m in enumerate(self.mapping):
            code, keys = m
            keys = self.keys_to_string(keys)

            cell_item = self.table.item(i, 1)
            if cell_item is not None:
                cell_item.setText(keys)
            else:
                new_item = QTableWidgetItem(keys)
                self.table.setItem(i, 1, new_item)

            cell_item = self.table.item(i, 0)
            if cell_item is not None:
                cell_item.setText(code)
            else:
                new_item = QTableWidgetItem(code)
                self.table.setItem(i, 0, new_item)
        
        mapping_count = len(self.mapping)
        for i in range(self.mapping_size - mapping_count):
            for j in range(2):
                cell_item = self.table.item(i + mapping_count, j)
                if cell_item is not None:
                    cell_item.setText("")
                else:
                    new_item = QTableWidgetItem("")
                    self.command.setItem(i + mapping_count, j, new_item)
            
    def update_keys(self):
        if self.command != None:
            cell_item = self.command.item(0, 1)
            if cell_item is not None:
                cell_item.setText(self.get_keys())
            else:
                new_item = QTableWidgetItem(self.get_keys())
                self.command.setItem(0, 1, new_item)

    def update_code(self):
        if self.command != None:

            cell_item = self.command.item(0, 0)

            if cell_item is not None:
                cell_item.setText(self.code)
            else:
                new_item = QTableWidgetItem(self.code)
                self.command.setItem(0, 0, new_item)

    def add_key(self, key):



        if key in replacements:
            key = replacements[key]
        if key not in self.keys:
            self.keys.append(key)
            self.update_keys()
    
    def remove_key(self):
        if len(self.keys) != 0:
            self.keys.pop()
            self.update_keys()

    def add_code(self, code):
        self.code = code
        self.update_code()

    def add_mapping(self):
        if not self.incomplete():
            
            for m in self.mapping:
                if m[0] == self.code:
                    m[1] = self.keys
                    self.clear()
                    self.update_table()
                    return

            self.mapping.append([self.code, self.keys])
            self.clear()
            self.update_table()
    
    def remove_mapping(self, index):
        if index < len(self.mapping):
            self.mapping.pop(index)
            self.update_table()

    def map_to_arduino(self):
        if self.arduino == None or self.threadpool == None:
            return

        print("Configuring")

        self.upload.reconfig(self.mapping)

        print("Closing")
        self.arduino.close(self.threadpool.start(self.upload))





    
