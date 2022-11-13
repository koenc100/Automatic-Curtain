# This program allows a user to enter a
# Code. If the C-Button is pressed on the
# keypad, the input is reset. If the user
# hits the A-Button, the input is checked.

import RPi.GPIO as GPIO
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1

input = ""
wakeup_time = None

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)
  
def A_pressed_func():
    
    global input
    global wakeup_time
    
    A_pressed = False
    
    # A, set alarm to sunrise
    GPIO.output(L1, GPIO.HIGH)
    
    if (GPIO.input(C4) == 1):
        print(f"Your alarm for tomorrow is set to sunrise")
        input = ""
        A_pressed = True
      
    GPIO.output(L1, GPIO.LOW)
    
    return A_pressed
    
    
def B_pressed_func():
    
    global input
    global wakeup_time
    
    # B not pressed yet
    B_pressed = False
    
    GPIO.output(L2, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        print("enter your preferred wake-up time \n4-digid **:** ")
        B_pressed = True
    
    GPIO.output(L2, GPIO.LOW)
    GPIO.output(L4, GPIO.HIGH)
    
    # If B is not pressed and # is pressed, enter the wake up time
    if (not B_pressed and GPIO.input(C3) == 1):
        
        # check the input 
        if len(input) == 4:
            wakeup_time = str(input)
            print(f"Your alarm for tomorrow is set at {wakeup_time[:2]}:{wakeup_time[-2:]}")
            
        else:
            print("Invalid wake-up time, please enter again")
            
        B_pressed = True

    GPIO.output(L4, GPIO.LOW)

    if B_pressed:
        input = ""

    return B_pressed

def C_pressed_func():
    
    global wakeup_time
    C_pressed = False
    
    # C, check current alarm 
    GPIO.output(L3, GPIO.HIGH)
    
    if (GPIO.input(C4) == 1):
        if wakeup_time != None:
            print(f"current alarm is set for {wakeup_time[:2]}:{wakeup_time[-2:]}, tomorrow")
        else:
            print("No alarm set")
            
        C_pressed = True
    
    GPIO.output(L3, GPIO.LOW)
    
    return C_pressed
    
def D_pressed_func():
    
    global input
    global wakeup_time
    
    D_pressed = False
    
     # D, turn off alarm
    GPIO.output(L4, GPIO.HIGH)
    
    if (GPIO.input(C4) == 1):
        print("All alarms are deleted")
        wakeup_time = None
        D_pressed = True
        input = ""
 
    GPIO.output(L4, GPIO.LOW)
    
    return D_pressed
# reads the columns and appends the value, that corresponds
# to the button, to a variable

def readLine(line, characters):
    global input
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        input = input + characters[0] 
    if(GPIO.input(C2) == 1):
        input = input + characters[1]
    if(GPIO.input(C3) == 1):
        input = input + characters[2]
    if(GPIO.input(C4) == 1):
        input = input + characters[3]
    
    GPIO.output(line, GPIO.LOW)

try:
    while True:
        
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
                
        # Otherwise, just read the input
        else: 

            if A_pressed_func():
                time.sleep(0.1)
                
            elif C_pressed_func():
                time.sleep(0.1)
                
            elif D_pressed_func():
                time.sleep(0.1)
                
            elif not B_pressed_func():
                readLine(L1, ["1","2","3","A"])
                readLine(L2, ["4","5","6","B"])
                readLine(L3, ["7","8","9","C"])
                readLine(L4, ["*","0","#","D"])
                time.sleep(0.1)
  
            else:
                time.sleep(0.1)

except KeyboardInterrupt:
    print("\nApplication stopped!")