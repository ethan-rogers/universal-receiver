import serial
import serial.tools.list_ports

import time

from PyQt6.QtCore import QRunnable, QThreadPool, QTimer, pyqtSlot



BAUD_RATE = 9600


class Receiver(QRunnable):
    def __init__(self, mapper, threadpool):
        super().__init__()
        
        self.data = None
        self.table = None
        self.mapper = mapper
        self.open = False
        self.threadpool = threadpool
        self.setAutoDelete(False)

        self.on_close = None

        #self.connect()


    def connect(self):
        # Get a list of all active serial ports
        print("Connecting")
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
                self.ser = serial.Serial(self.port, BAUD_RATE, timeout=5)
                print("Opened")
                self.open = True

                if self.threadpool != None:
                    print("Running Thread")
                    self.threadpool.start(self)
                    print("Thread running")

                
                
    @pyqtSlot()
    def run(self):
        while self.open:
            time.sleep(0.1)

            if self.ser.in_waiting > 0:
                raw_data = self.ser.readline()
                clean_data = raw_data.decode('utf-8').strip()
                
                if clean_data != '0':
                    if self.mapper != None:
                        self.mapper.add_code(clean_data)
        print("Closing")
        print(self.ser)
        self.ser.close()
        
        if (self.on_close != None):
            self.on_close()

    def get_port(self):
        return self.port
    
    def get_data(self):
        return self.data

    def close(self, on_close):
        self.open = False
        self.on_close = on_close
    
