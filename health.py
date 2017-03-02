'''
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file stores all the functions and objects related to the player's health

'''

import pygame
import constants
import time
import math

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ --Quick Find - Ctrl + F-- $$$
#$$$ update health - AAA1      $$$
#$$$ set health - AAA2         $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


class Health(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        #this loads all the images needed for a rope
        self.hearts = []
        self.hearts.append(pygame.image.load('Graphics/Health/hearts_1.png'))
        self.hearts.append(pygame.image.load('Graphics/Health/hearts_2.png'))
        self.hearts.append(pygame.image.load('Graphics/Health/hearts_3.png'))

        #This set's up the player's life bar
        self.life = 3
        
        self.image = self.hearts[self.life-1]

        #this is a set of locations for the player's life bar
        self.rect = self.image.get_rect()
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery



    #AAA1
    #This function updates the player's bar
    def update_health(self):
        #checks that the life isn't below zero
        if self.life >= 0:
            self.life -= 1
            self.image = self.hearts[self.life-1]

    #AAA2
    #this sets the health to a value
    def set_life(self, life=2):
        self.life = life
