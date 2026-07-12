# Universal Receiver

 Maps keyboard keys and media controls to any IR remote with an Arduino receiver. I made it to watch YT on my monitor in bed. 

 ## Hardware

The Arduino acts as a USB keyboard, so once the keys are mapped it will work plug and play with any computer. 

### Components

* Arduino Pro Micro
* KY-022 infrared sensor

### Schematic

TODO: add schematic

### Physical Prototype

Here is my prototype that I use. Made with a perfboard. 

![](images/prototype.jpg)

## Software

### Functionality

The software allows you to map any IR signal to a combination of keys and media controls. It automatically connects to the Arduino and supports up to 8 combinations.

### UI


![](images/ui.png)

### Setup

To run the software you must have Python installed and the packages `pyqt6` and `pyserial`.