'''
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file stores all the functions and objects related to the whip

'''
import pygame
import constants
import math
import time
import graphics


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ -------------- Ctrl + F ------------- $$$
#$$$ --------- Whip Class - AAA ---------- $$$
#$$$ - Whip Animation - AAA1               $$$
#$$$ - Updates the whip - AAA2             $$$
#$$$ - Animation Corections - AAA3         $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class Whip(pygame.sprite.Sprite):
    #this class is for the rope that a player can shoot out to swing on objects

    #this is the constructor for the rope class
    def __init__(self):
         #call the parent's constructor
        super().__init__()

        #these arrays will store the images for the whip both left and right
        self.whip_frames_left = []
        self.whip_frames_right = []

        for img in graphics.whip_animation:
            image = pygame.image.load(img)
            self.whip_frames_right.append(image)
            self.whip_frames_right.append(image)
            image = pygame.transform.flip(image, True, False)
            self.whip_frames_left.append(image)
            self.whip_frames_left.append(image)

        #stores which frame is being used currently
        self.frame = 0

        #used to determine if the whip should be whipping!
        #n: not whipping
        #y: whip it, whip it real good
        self.whip_being_used = 'n'

        #sets the image
        self.image = self.whip_frames_right[0]
        self.rect = self.image.get_rect()

        
    #this plays the whip's animation
    #AAA1
    def whip_animation(self):
        if self.whip_being_used == 'y':
            self.whip_correction()
            self.frame = (self.frame + 1) % len(self.whip_frames_right)
            self.image = self.whip_frames_right[self.frame]

            if self.frame == 17:
                self.whip_being_used = 'n'
                self.frame = 0

    #this updates the whip as needed
    #AAA2
    def whip_update(self, player_x, player_y):
        if self.whip_being_used == 'n':
            self.rect.x = -50
            self.rect.y = -50
        else:
            self.rect.x = player_x
            self.rect.y = player_y
            self.whip_animation()

    #this corrects the animation of the whip to look better
    #AAA3
    def whip_correction(self):
        #correct this
        #if the player is facing to the right
        if self.frame == 0 or self.frame == 1:
            self.rect.x -= 25
            self.rect.y -= 25
        if self.frame == 2 or self.frame == 3:
            self.rect.x -= 25
            self.rect.y -= 25 
        if self.frame == 4 or self.frame == 5:
            self.rect.x -= 35
            self.rect.y -= 25  
        if self.frame == 6 or self.frame == 7:
            self.rect.x -= 35
            self.rect.y -= 35  
        if self.frame == 8 or self.frame == 9:
            self.rect.x -= 15
            self.rect.y -= 35  
        if self.frame == 10 or self.frame == 11:
            self.rect.x += 10
            self.rect.y -= 25   
        if self.frame == 12 or self.frame == 13:
            self.rect.x += 10
            self.rect.y += 10   
        if self.frame == 14 or self.frame == 15:
            self.rect.x += 10
            self.rect.y += 10   
        if self.frame == 16 or self.frame == 17:
            self.rect.x += 10
            self.rect.y += 10        
            
        
