# Automatic-curtain

This repository contains all the code, 3D prints and the rasberry pi pin layout to make an automatic curtain. The curtain has two main features, it can open and close when it detects a double clap in the room. Besides, you can set an alarm to wake up to a bright room the next day. In the following section, the required hardwareand software libraries are listed. rightafter, the mechanics and the code are briefly explained. Finally, I touch upon some improvements. Enjoy reading!

The software was coded in Python 3.7.3 on RasberryOS in the Thonny Python IDE. 

The required libraries are listed below:
- time (Python 3.7.3)
- datetime (3.2)
- RPi.GPIO (0.7.1) module to control the GPIO on a Raspberry Pi, these are the in- and output pins.
- threading (Python 3.7.3)
- pygame (1.94)
- contextlib (Python 3.7.3)
- rpi_lcd (Python 3.7.3)

The used/required hardware is listed below:
- Rasberry pi (I used model 4B)
- Sound sensor (KY-038)
- Stepper motor (28byj-48)
- LCD screen (1602 with i2c)
- 16-key membrance (Arduino)
- power supply breadboard (KW-1851, included 5V battery)
- driver board (ULN2003)
- breadboard (optional but usefull)








