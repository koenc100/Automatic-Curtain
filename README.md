# Automatic-curtain

This repository contains all the code, 3D prints and the raspberry pi pin layout to make an automatic curtain for your bedroom! The curtain has two main features, it can open and close when it detects a double clap in the room, so you can simply close or open your curtains from anywhere in the room. That is not all; with the use of the LCD screen and keypad, you can set an alarm to wake up to a bright room the next day. All I can say: the future is here.

In the first section, the required software libraries and hardware components are listed. right after, I briefly explain the pin layout including components, mechanics and the code. Finally, I touch upon some improvements. Enjoy reading!

The software was coded in Python 3.7.3 on RasberryOS in the Thonny Python IDE. 

The required libraries are listed below:
- time (Python 3.7.3)
- datetime (3.2)
- RPi.GPIO (0.7.1) module to control the GPIO on a Raspberry Pi, these are the in- and output pins.
- threading (Python 3.7.3)
- pygame (1.94)
- contextlib (Python 3.7.3)
- rpi_lcd (Python 3.7.3)

The used/required hardware electronics is listed below:
- Raspberry pi (I used model 4B)
- Sound sensor (KY-038)
- Stepper motor (28byj-48)
- LCD screen (1602 with i2c)
- 16-key membrane (Arduino)
- Power supply breadboard (KW-1851, included 5V battery)
- Driver board (ULN2003)
- speakers with aux input (I used Logitech model)
- Breadboard (optional but useful)

The required mechanical hardware is listed below:
- 3D printed parts (from repository: Automatic-curtain/parts)
- three pulleys (+ attachment)
- thread/thin rope 
- strong glue (either glue gun or superglue)
- 2 bolts, 2 nuts and 4 sheer-metal rings (2 mm)
- 4 screws (5 mm)

The complete system is wired as seen in the picture below. In the figure, the power supply is not depicted since it was not in the software package. 

# mechanics
The mechanics are relatively simple. The stepper motor is connected to a drum which takes in thread when turning either clockwise or counterclockwise. When turning clockwise, the curtain is closed due to the placement of the pulleys. When turning counterclockwise, the curtain is opened, naturally. In the schematic picture below the mechanics can be seen. This setup is only applicable for a two-curtain setup where both curtains move in the opposite direction, or with one curtain after some simplification. There are some drawbacks to this setup which will be explained at in the final section. 


![image](https://user-images.githubusercontent.com/73174827/201544926-d9e7e161-2569-4e73-92ee-2b99edbd5088.png)


# code
The main script is the 'curtain_complete.py' To run headless (without monitor) this script runs on boot with the use of rc.local. The script a continuous while loop where it checks for either buttons to be pressed or double claps to be detected. The file 'multitimer_me' is imported into the main script hence needs to be in the same folder. Furthermore, the wakeup-music is and .mp3 file which needs to be located in the script by filling in the path. The other code files are predecessors of the 'curtain_complete' where you can independently test all the components.

Combining the code with the breadboard leads to the following complete setup:
![WhatsApp Image 2022-11-13 at 10 26 21 PM](https://user-images.githubusercontent.com/73174827/201545389-346c96aa-932f-46da-9820-42681a13d0d3.jpeg)

# Improvements
To improve, the stepper motor should have more torque. For my curtain, the 28BYJ-48 just barely gets the job done. An upgrade to a NEMA 17 or so would do the job. Also, since the mechanics do not have some sort of spring or contra mass mechanism, the thread is not always string. If you could insert a spring onto the thread, it would tighten and be more reliable. Furthermore, it works just fine!

Thanks for reading






