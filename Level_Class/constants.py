'''
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file is to store all the global varaibles that will be used thruout the program
For example here is where all the colors will be defined.

'''

import pygame
#This page is for Global Constants

#Colors
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
NAVY  = (  0,  0,128)
GRAY  = (190,190,190)
LIME_GREEN = (50,205,50)
GREEN = (34,139,34)
YELLOW = (255,255,0)
GOLD = (255,215,0)
RED = (255,0,0)
ORANGE = (255,165,0)
PURPLE = (160,32,240)

#Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Sets the display surface for the game
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Frames Per Second
fps = 60