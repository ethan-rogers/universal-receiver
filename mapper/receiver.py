import serial
import serial.tools.list_ports

import time

from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem


BAUD_RATE = 9600


class Receiver(QRunnable):
    def __init__(self, mapper):
        super().__init__()
        self.conenct()
        self.data = None
        self.table = None
        self.mapper = mapper
    
    def set_table(self, table):
        self.table = table

    def conenct(self):
        # Get a list of all active serial ports
        ports = list(serial.tools.list_ports.comports())

        self.port = None
        self.ser  = None
        
        for p in ports:
            # Check description or manufacturer for 'arduino' (case-insensitive)
            description = p.description.lower()
            hwid = p.hwid.lower()
            
            if "arduino" in description or "usb-serial" in description or "ch340" in description:
                print(f"Found Arduino on port: {p.device} ({p.description})")
                self.port = p.device
                self.ser = serial.Serial(self.port, BAUD_RATE, timeout=1)
                
    @pyqtSlot()
    def run(self):
        while True:
            time.sleep(0.1)

            if self.ser.in_waiting > 0:
                raw_data = self.ser.readline()
                clean_data = raw_data.decode('utf-8').strip()
                
                if clean_data != '0':
                    self.data = clean_data
                    if self.table != None:

                        cell_item = self.table.item(0, 0)

                        if cell_item is not None:
                            # If the item exists, simply update its text value
                            cell_item.setText(clean_data)
                        else:
                            # If the cell is blank/None, initialize a new item and assign it
                            new_item = QTableWidgetItem(clean_data)
                            self.table.setItem(0, 0, new_item)

                    if self.mapper != None:
                        self.mapper.add_code(clean_data)

    def get_port(self):
        return self.port
    
    def get_data(self):
        return self.data
    
