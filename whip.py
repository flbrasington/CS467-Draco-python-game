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

        for img in graphics.whip:
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

        #sets the direction of the whip
        self.direction = 'r'

        
    #this plays the whip's animation
    #AAA1
    def whip_animation(self):
        #test = 16
        if self.direction == 'r':
            if self.whip_being_used == 'y':
                self.frame = (self.frame + 1) % len(self.whip_frames_right)
                self.image = self.whip_frames_right[self.frame]
                #self.image = self.whip_frames_right[test]

                if self.frame == 5:
                    self.whip_being_used = 'n'
                    self.frame = 0
        else:
            if self.whip_being_used == 'y':
                self.whip_correction()
                self.frame = (self.frame + 1) % len(self.whip_frames_left)
                self.image = self.whip_frames_left[self.frame]
                #self.image = self.whip_frames_left[test]

                if self.frame == 5:
                    self.whip_being_used = 'n'
                    self.frame = 0

        
        print("frame = ", self.frame)
            

    #this updates the whip as needed
    #AAA2
    def whip_update(self, player_x, player_y):
        if self.whip_being_used == 'n':
            self.rect.x = -50
            self.rect.y = -50
        else:
            self.rect.centerx = player_x
            self.rect.centery = player_y
            self.whip_correction()
            self.whip_animation()
            #time.sleep(1)

    #this corrects the animation of the whip to look better
    #AAA3
    def whip_correction(self):
        if self.frame >= 0 and self.frame <= 2:
            self.rect.y -= 5
            if self.direction == 'r':
                self.rect.x += 38
            else:
                self.rect.x -= 18
        if self.frame >= 3 and self.frame <= 6:
            self.rect.y -= 0
            if self.direction == 'r':
                self.rect.x += 38
            else:
                self.rect.x -= 18
        if self.frame >= 7 and self.frame <= 9:
            self.rect.y -= 0
            if self.direction == 'r':
                self.rect.x += 38
            else:
                self.rect.x -= 18
            
        
            
            
        
