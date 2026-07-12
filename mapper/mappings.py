from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

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
    
    def set_command(self, command):
        self.command = command
    
    def set_table(self, table):
        self.table = table

    def clear(self):
        self.keys = []
        self.code = None

        self.update_keys()
        self.update_code()


    def get_keys(self):
        key_str = "" 

        for i, k in enumerate(self.keys):
            if k in replacements:
                key_str += replacements[k]
            else:
                key_str += k
            if i != len(self.keys) - 1:
                key_str += " + "

        return key_str
    
    def update_table(self):
        pass

    def update_keys(self):
        if self.command != None:
            print("attempting add")
            cell_item = self.command.item(0, 1)
            print("Recieved item: ", cell_item)
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
        self.mapping.append([self.code, self.keys])
        self.clear

    def map_to_arduino(self):
        print("Attempting Mapping")