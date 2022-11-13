
import pygame
import random

pygame.mixer.init()

morninglist = ['Good Morning.wav', 'GM_sun.wav', 'Good Morning Turdbrain.wav','goodmorning_vietnam.wav',
               'John Wayne Dont tell its a fine morning.wav', 'Wanna Beer.wav']

morningsound = random.choice(morninglist)

morning = pygame.mixer.Sound(f'/home/pi/Music/GM_wav/Wanna Beer.wav')

pygame.mixer.Sound.play(morning)
