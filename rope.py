'''
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file stores all the functions and objects related to the player.
Here is where you will find things such as the player's spirit's sheet,
movement and actions.

'''
import pygame
import constants
import math
import time

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ -------------- Ctrl + F ------------- $$$
#$$$ Opposite, Adjacent, Hypotenuse - AAA1 $$$
#$$$ Calculate rope's speed - AAA2         $$$
#$$$ Update Rope - AAA3                    $$$
#$$$ Shoot the rope - AAA4                 $$$
#$$$                                       $$$
#$$$ Collision detections - AAA6           $$$
#$$$ Rotate Image- AAA7                    $$$
#$$$ Calculates Angle - AAA8               $$$
#$$$ update_angle - AAA9                   $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


class Rope(pygame.sprite.Sprite):
    #this class is for the rope that a player can shoot out to swing on objects

    #this is the constructor for the rope class
    def __init__(self):
         #call the parent's constructor
        super().__init__()

        #this is the end_point
        self.end_point_x = 0
        self.end_point_y = 0
    
        #this is the starting_point
        self.start_point_x = 0
        self.start_point_y = 0

        #if the rope has been shot then draw the line
        #else don't
        #n: do not draw
        #y: yes draw the line
        #a: rope is attached
        self.draw_line = 'n'

        #this is used for calculating the speed of which the rope is shot out and the direction
        self.speed = 10
        self.speed_x = 0
        self.speed_y = 0

        #this loads all the images needed for a rope
        rope_anchor = pygame.image.load('Graphics/Rope/rope_anchor.png')
        self.image = rope_anchor

        #this is a set of locations for the rope_anchor positions
        self.rect = self.image.get_rect()
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery

        #this stores all the platfroms that could be hit by the rope's anchor
        self.level = None

        


#$$$ AAA3
    def update_rope(self):
        #sets the image offscreen if not being used
        if self.draw_line == 'n':
            self.center_x = -30
            self.center_y = -30
            
        if self.draw_line == 'y':
            self.end_point_x += self.speed_x
            self.end_point_y += self.speed_y
            pygame.draw.lines(constants.DISPLAYSURF, constants.ROPE, False, [(self.start_point_x,self.start_point_y),
                                                                             (self.end_point_x,self.end_point_y)], 8)
            self.rect.centerx = self.end_point_x
            self.rect.centery = self.end_point_y

            self.rope_Collision()

        if self.draw_line == 'a':
            pygame.draw.lines(constants.DISPLAYSURF, constants.ROPE, False, [(self.start_point_x,self.start_point_y),
                                                                             (self.end_point_x,self.end_point_y)], 8)
            

        
#AAA6
#This function checks for the event that the rope's anchor hits an object
    def rope_Collision(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.draw_line = 'a'

            
#$$$ AAA4
    def shoot_rope(self, start_x, start_y, end_x, end_y):
        self.end_point_x = end_x
        self.end_point_y = end_y
        self.start_point_x = start_x
        self.start_point_y = start_y

        O = self.find_Opposite(start_y, end_y)
        A = self.find_Adjacent(start_x, end_x)
        H = self.find_Hypotenuse(start_x, start_y, end_x, end_y)
        
        self. calc_speed(O,A,H)
        angle = self.find_angle(O, A)
        angle = self.update_angle(angle, start_x, start_y, end_x, end_y)
        self.image = self.rot_center(self.image, angle)

        self.end_point_x = self.start_point_x
        self.end_point_y = self.start_point_y

        self.draw_line = 'y'

#$$$ AAA1
    def find_Opposite(self, start_y, end_y):
        if end_y - start_y == 0:
            return 1
        return end_y - start_y
    
    def find_Adjacent(self, start_x, end_x):
        if end_x - start_x == 0:
            return 1
        return end_x - start_x
    
    def find_Hypotenuse(self, start_x, start_y, end_x, end_y):
        A = start_x - end_x
        B = start_y - end_y
        return math.sqrt(A*A + B*B)

#$$$ AAA2
#$$$ Calculate speed
    def calc_speed(self, opposite, adjacent, hypotenuse):
        self.speed_x = adjacent/hypotenuse * self.speed
        self.speed_y = opposite/hypotenuse * self.speed

#$$$ AAA7
#Rotates an image around the image's center
    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

#$$$ AAA8
#this find the angle for the rope
    def find_angle(self, Opposite, Adjacent):
        angle_rads = Opposite/Adjacent
        angle_rads = math.atan(angle_rads)
        #now to convert from radians to degree
        angle_degrees = angle_rads * 180 / math.pi

        return angle_degrees

#$$$ AAA9
#this updates the angle based on which cooridantes the mouse is shot out at
    def update_angle(self, angle, player_x, player_y, mouse_x, mouse_y):
        if player_x > mouse_x:
            return -angle + 90
        else:
            return -angle - 90
        
        
        

        
