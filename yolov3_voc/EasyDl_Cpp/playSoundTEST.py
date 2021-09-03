import pygame
import sys
from pygame.locals import *
from func_timeout import func_set_timeout
pygame.init()
pygame.mixer.init()
music = pygame.mixer.music.load("/home/ubuntu/python_pro/A_polyp/垃圾分类宣传2.wav")
@func_set_timeout(3)
def test():
    while True:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.play()
            
try:
    test()
except:
    print("end!!")
