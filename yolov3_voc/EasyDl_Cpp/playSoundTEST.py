import pygame
import sys
from pygame.locals import *
pygame.init()
pygame.mixer.init()
music = pygame.mixer.music.load("/home/ubuntu/python_pro/A_polyp/垃圾分类宣传2.wav")
while True:
    if pygame.mixer.music.get_busy() == False:
        pygame.mixer.music.play()
