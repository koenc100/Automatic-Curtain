import RPi.GPIO as GPIO
import time
import datetime as datetime
import os

# define way of numbering pins
GPIO.setmode( GPIO.BCM )

sound_pin = 4

# Define every pin as OUTPUT
GPIO.setup( sound_pin, GPIO.IN )

count = 0

claps = list()

def detected(sound_pin):
    
    global count
    global claps
    
    nowtime = datetime.datetime.now()
    print(nowtime)
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
        
    return nowtime

print("Sound sensor test, CTR + C to quit")

time.sleep(0.5)
      
print("Are you ready?")

run = True

try:
    
    # If the sound pin is triggered by rising value, run detected function
    GPIO.add_event_detect(sound_pin, GPIO.RISING, callback=detected)
    
    # have it run 100 seconds ?
    while 1:
        time.sleep(100)     
      
# cleanup 
except KeyboardInterrupt:
    print("Quit")
    GPIO.cleanup()

