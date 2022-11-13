# Author : Koen Ceton
# Date : 15/09/2022
# Explanation : Script runs automatic curtains which react to double clap.
# Script also runs keypad and lcd screen to set wake up alarms

import RPi.GPIO as GPIO
import time
from rpi_lcd import LCD
import datetime as datetime
from threading import Timer
from multitimer_me import MultiTimer
import contextlib
with contextlib.redirect_stdout(None):
    import pygame

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# keypad lines (4) and columns(4)
L1 = 5
L2 = 6
L3 = 13
L4 = 19
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# microphone pin
sound_pin = 4

# stepper motor pins
in1 = 17
in2 = 18
in3 = 27
in4 = 22

# define keypad IN/OUT, columns use the internal pull-down resistors
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# define microphone
GPIO.setup( sound_pin, GPIO.IN )

# define stepper motor pins
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )

# initialize pygame mixer
pygame.mixer.init()
pygame.mixer.music.load('/home/pi/Music/awakening.mp3')

## CODE ON LCD SCREEN
lcd = LCD()

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1
input = ""
wakeup_time = ''

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

## CODE ON STEPPER MOTOR

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002

step_count = 4096 * 7 # 5.625*(1/64) per step, 4096 steps is 360°

close = False # Turning clockwise is closing, counter-clockwise is opening. Curtains start open !

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# initialize stepper motor
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;

## CODE ON SOUND SENSOR
claps = list()

## FUNCTIONS

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()

def to_move_or_not_to_move(move):
    
    global close
    
    # switch direction for every double clap
    if move == 'both':
        close = not close
        turn_stepper()

    elif move == 'open' and close == True:
        close = False
        turn_stepper()
        
    elif move == 'close' and close == False:
        close = True
        turn_stepper()
        
    else:
        None
        
def turn_stepper():

    global motor_step_counter
    global close
        
    i = 0
    
    # for every step in a 360 round
    for i in range(step_count):
        
        # for every pin connected (int1, int2, int3, int4)
        for pin in range(0, len(motor_pins)):
            
            # for every pin, output the row in squence and the right pin out of that row
            GPIO.output( motor_pins[pin], step_sequence[motor_step_counter][pin] )
            
        # if clockwise, calculate new motor step counter
        if close==True:
            motor_step_counter = (motor_step_counter - 1) % 8
            
        # if anti clockwise, calculate new moter step counter 
        elif close==False:
            motor_step_counter = (motor_step_counter + 1) % 8
            
        else: # defensive programming
            print( "uh oh... direction should *always* be either True or False" )
            cleanup()
            exit( 1 )
            
        time.sleep( step_sleep )

  
def detected(sound_pin):
    
    global count
    
    nowtime = datetime.datetime.now()
    claps.append(nowtime)
    
    # if there is only one input, no delta needed
    if len(claps) == 1:
        deltastep = claps[0]
    
    # get difference between two measurements
    else:
        deltastep = claps[-1] - claps[-2]
    
    # to float and seconds
    deltastep = float(str(deltastep)[-9:-1])
     
    # if difference is equal to clap difference and more than one sample
    if 0.4 > deltastep > 0.2 and len(claps) != 1:
        to_move_or_not_to_move('both')
        
    return nowtime
        
# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)
    
def set_alarm(wakeup_time):
    
    global nowtime
    
    hours, minutes = [int(nowtime[:2]), int(nowtime[2:4])]
    
    if hours + 8 >= 24:
        hours += -15
    else:
        hours += 9
         
    if minutes + 30 >= 60:
        minutes += -30   
    else:
        minutes += 30

    wakeup_time = f"{hours}{minutes}"
      
    return wakeup_time

def A_pressed_func():
    
    global wakeup_time
    
    # A, set alarm to sunrise
    GPIO.output(L1, GPIO.HIGH)
    
    if (GPIO.input(C4) == 1):
        wakeup_time = set_alarm(wakeup_time)
        lcd.text("Wake in 8H 30M", 1)
        lcd.text(f"     {wakeup_time[:2]}:{wakeup_time[-2:]}    ", 2)
      
    GPIO.output(L1, GPIO.LOW)
    
# B not pressed yet
B_pressed = False
    
def B_pressed_func():
    
    global input
    global wakeup_time
    global B_pressed
    
    GPIO.output(L2, GPIO.HIGH)

    if (GPIO.input(C4) == 1):
        lcd.text("Enter Time:", 1)
        lcd.text("     **:**        ", 2)
        B_pressed = True
        input = ''
    
    GPIO.output(L2, GPIO.LOW)
    GPIO.output(L4, GPIO.HIGH)
    
    # If B is not pressed and # is pressed, enter the wake up time
    if (B_pressed and len(input) == 4):
        wakeup_time = str(input)
        lcd.text("Wake-up tomorrow:", 1)
        lcd.text(f"     {wakeup_time[:2]}:{wakeup_time[-2:]}    ", 2)
        B_pressed = False
        input = ''

    GPIO.output(L4, GPIO.LOW)

    return B_pressed

def C_pressed_func():
    
    global wakeup_time
    
    # C, check current alarm 
    GPIO.output(L3, GPIO.HIGH)
    
    if (GPIO.input(C4) == 1):
        if wakeup_time != '':
            lcd.text(f"Current wake-up:", 1)
            lcd.text(f"     {wakeup_time[:2]}:{wakeup_time[-2:]}    ", 2)
        else:
            lcd.text("No wake-up set", 1)
            lcd.text("", 2)
               
    GPIO.output(L3, GPIO.LOW)
    
def D_pressed_func():
    
    global wakeup_time
    
     # D, turn off alarm
    GPIO.output(L4, GPIO.HIGH)
    
    if (GPIO.input(C4) == 1):
        lcd.text("Wake-up deleted", 1)
        lcd.text("", 2)
        wakeup_time = ''
 
    GPIO.output(L4, GPIO.LOW)
 
def play_music():
    pygame.mixer.music.play(-1)
    time.sleep(0.1)

# make multitimer object, start music 10 minutes after curtains open
t = MultiTimer(interval = 600, function=play_music, count=1, runonstart=False) 

def goodnight():
    
     # D, turn off alarm
    GPIO.output(L4, GPIO.HIGH)
    
    if (GPIO.input(C1) == 1):
        lcd = LCD()
        lcd.text("Goodmorning", 1)
        lcd.text("Goodnight", 2)
        time.sleep(1)
        lcd.clear();

    GPIO.output(L4, GPIO.LOW)

def alarm_off():
    
    global t
    
     # D, turn off alarm
    GPIO.output(L4, GPIO.HIGH)
    
    if (GPIO.input(C3) == 1):
        t.stop()
        pygame.mixer.music.stop()
        
    GPIO.output(L4, GPIO.LOW)

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

    # If the sound pin is triggered by rising value, run detected function
    GPIO.add_event_detect(sound_pin, GPIO.RISING, callback=detected)
    
    
    while True:
        
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
                
        nowtime = datetime.datetime.now().strftime('%H%M%S')
        
        # if now time is wakeup_time
        if nowtime == wakeup_time+'01': # to the second
            time.sleep(0.1)
            to_move_or_not_to_move('open') # second time this happens 10 times in 0.1 second ... ?
            t.start()
              
        else:
            # run through the button fuctions
            A_pressed_func()
            C_pressed_func()
            D_pressed_func() 
            goodnight()   
            alarm_off()
        
            # if B is True, start to read the input
            if B_pressed_func():
                readLine(L1, ["1","2","3","A"])
                readLine(L2, ["4","5","6","B"])
                readLine(L3, ["7","8","9","C"])
                readLine(L4, ["*","0","#","D"])
                time.sleep(0.1)
  
            else:
                time.sleep(0.1)


except KeyboardInterrupt:
    print("\nApplication stopped!")
    cleanup()
    lcd.clear()

