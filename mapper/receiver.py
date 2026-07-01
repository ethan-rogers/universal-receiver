import serial
import serial.tools.list_ports


def init():
    # Get a list of all active serial ports
    ports = list(serial.tools.list_ports.comports())
    
    for p in ports:
        # Check description or manufacturer for 'arduino' (case-insensitive)
        description = p.description.lower()
        hwid = p.hwid.lower()
        
        if "arduino" in description or "usb-serial" in description or "ch340" in description:
            print(f"Found Arduino on port: {p.device} ({p.description})")
            return p
            

    print("Not found")
    return None


def get_data():
    pass