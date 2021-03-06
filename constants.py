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

pygame.init()

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
TRANSPARENT = (1,2,3)
ROPE = (155, 73, 35)
DARK_GREY = (42, 42, 42)
DARK_YELLOW = (204,204,0)

#Screen Dimensions
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

#Room Dimensions
ROOM_HEIGHT = 8
ROOM_WIDTH = 10

#Rooms on screen at once
ROOMS_ON_SCREEN = 1

#Level Dimensions
NUM_ROOMS_X = 5
NUM_ROOMS_Y = 5

#Sets the display surface for the game
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Frames Per Second
fps = 60

#Font information
BUTTON_WIDTH = 125
BUTTON_HEIGHT = 100

#Detection distance for enemies
DETECTION_DISTANCE = 1200

# font for inventory count
INV_FONT = pygame.font.SysFont("comicsansms", 38)