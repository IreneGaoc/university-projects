section:CMPUT 274 A2
Project Title: Snake Game Arduino
Team members: Irene(Zihan) Gao and Gaoping Zhou
referencce:https:Arduino library--
(//www.arduino.cc/en/Tutorial/JoystickMouseControl)
(https://www.arduino.cc/en/Reference/TFTLibrary)

Preparation:
Arduino megaboard
breadboard
tft lcd, leds
3 potentiometers
joystick
pushbutton
USB
wires.

Wiring instructions:
for the TFT LCD:
GND to BB GND bus
VCC to BB positive bus
RESET to Pin 8
D/C (Data/Command) to Pin 7
CARD_CS (Card Chip Select) to Pin 5
TFT_CS (TFT/screen Chip Select) to Pin 6
MOSI (Master Out Slave In) to Pin 51
SCK (Clock) to Pin 52
MISO (Master In Slave Out) to 50
LITE (Backlite) to BB positive bus

for the Joystick:
VCC to BB positive bus
VERT to Pin A0
HOR to Pin A1
SEL to Pin 9
GND to BB GND bus

for the leds and resistors and pushbuttons:
Arduino DigitalPin 2<-->Longer LED lead |LED|(1st RED) shorter LED lead<-->560 ohm Resistor<-->Arduino GND
Arduino DigitalPin 3<-->Longer LED lead |LED|(2nd RED) shorter LED lead<-->560 ohm Resistor<-->Arduino GND
Arduino DigitalPin 4<-->Longer LED lead |LED|(3rd RED) shorter LED lead<-->560 ohm Resistor<-->Arduino GND
Arduino DigitalPin 10<-->pushbutton<--> Arduino GND
Arduino 5V<--> the supply voltage of bus strips on the breadboard

Assumption:
none

procedure:
unzip the file
open the file with an IDE
make sure you select the right board and port
Check the procedures are accurate
Connect the USB cable to the computer and the mega board
make upload
follow the instructions
finish

Instructions:
you can click the joystick to enter the game. Also, when the game is over, you can click the joystick to restart. When playing the game, you can push the pushbutton to quit.
use the joystick to control the movement and eat the food, also, you need to avoid the blocks and be careful do not touch the wall and eat your tail.
