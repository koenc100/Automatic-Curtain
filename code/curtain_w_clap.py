# Author : Koen Ceton

import RPi.GPIO as GPIO
import time
import datetime as datetime
import os

# define way of numbering pins
GPIO.setmode( GPIO.BCM )

# place pins 
sound_pin = 4
in1 = 17
in2 = 18
in3 = 27
in4 = 22

# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move
step_sleep = 0.002

step_count = 96 # * 7 # 5.625*(1/64) per step, 4096 steps is 360°
 
close = False # Turning clockwise is closing, counter-clockwise is opening

# defining stepper motor sequence (found in documentation http://www.4tronix.co.uk/arduino/Stepper-Motors.php)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# Define every pin as IN or OUT
GPIO.setup( sound_pin, GPIO.IN )
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
 
# initializing
GPIO.output( in1, GPIO.LOW )
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )

motor_pins = [in1,in2,in3,in4]
motor_step_counter = 0 ;

claps = list()

def cleanup():
    GPIO.output( in1, GPIO.LOW )
    GPIO.output( in2, GPIO.LOW )
    GPIO.output( in3, GPIO.LOW )
    GPIO.output( in4, GPIO.LOW )
    GPIO.cleanup()

def turn_stepper(move):

    global motor_step_counter
    global close
    
    # switch direction for every double clap
    if move == 'both':
        close = not close

    elif move == 'open':
        close = False
        
    elif move == 'close':
        close = True
     
    i = 0
    
    # for every step in a 360 round
    for i in range(step_count):
        
        print(i)
        
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
        print('DOUBLE time delta: ', deltastep)
        print('Today\'s Wake-up time: ', str(nowtime))
        turn_stepper('both')
        
    return nowtime

print("Sound sensor test, CTR + C to quit")

time.sleep(0.5)
      
print("Are you ready?")

try:
    
    # If the sound pin is triggered by rising value, run detected function
    GPIO.add_event_detect(sound_pin, GPIO.RISING, callback=detected)
    
    while 1:
    
        time.sleep(1)

      
except KeyboardInterrupt:
    print("Quit")
    cleanup()
    
