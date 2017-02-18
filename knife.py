'''
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file stores all the functions and objects related to the knife object

'''
import pygame
import constants
import math
import time

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ -------------- Ctrl + F ------------- $$$
#$$$ ----------   Knife Class  ----------- $$$
#$$$ Update Knife - AAA1                   $$$
#$$$ Collision Detection - AAA2            $$$
#$$$ throw knife- AAA3                     $$$
#$$$ trinalge calculations AAA4            $$$
#$$$  Calculate speed - AAA5               $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class Knife(pygame.sprite.Sprite):
    #this class is for the knife that a player can throw

    #this is the constructor for the knife class
    def __init__(self):
         #call the parent's constructor
        super().__init__()
        
        #this is the end_point
        self.end_point_x = 0
        self.end_point_y = 0
    
        #this is the starting_point
        self.start_point_x = 0
        self.start_point_y = 0
        
        #this sets the speed for the knife object
        self.speed = 20
        self.speed_x = 0
        self.speed_y = 0

        #sets up the image for the knife
        self.image = pygame.image.load('Graphics/Inventory/knife_small.png')

        self.rect = self.image.get_rect()

        #this stores all the platfroms that could be hit by the knife
        self.level = None

        #This is for if the knife has been thrown or not thrown
        #y: knife has been or is being thrown
        #n: knife hasn't been thrown yet
        #s: knife is stock in the wall
        self.thrown = 'n'
        
        #this is a set of locations for the rope_anchor positions
        self.rect = self.image.get_rect()
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery

        self.angle = 0

        self.enemies = None
        
#$$$ AAA1
    def update_knife(self):
        if self.thrown == 'n':
            self.rect.x = -50
            self.rect.y = -50
        elif self.thrown == 'y':
            self.end_point_x += self.speed_x
            self.end_point_y += self.speed_y
            self.rect.centerx = self.end_point_x
            self.rect.centery = self.end_point_y

            self.knife_Collision()

        
#$$$ AAA2
    # this detects collisions between the knife and other items
    def knife_Collision(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.thrown = 's'

        # for every update of the knife, a list of enemies which collide with it
        # will be returned
        enemiesHit = pygame.sprite.spritecollide(self, self.enemies, False)
        
        # if an enemy is hit (enemiesHit will be an empty list for open space)
        if len(enemiesHit) >= 1:
            # deal damage to the first enemy hit
            enemiesHit[0].hp -= 5
            # remove knife from game
            self.kill()

#$$$ AAA3
    def throw_knife(self, start_x, start_y, end_x, end_y, enemies):
        self.end_point_x = end_x
        self.end_point_y = end_y
        self.start_point_x = start_x
        self.start_point_y = start_y

        O = self.find_Opposite(start_y, end_y)
        A = self.find_Adjacent(start_x, end_x)
        H = self.find_Hypotenuse(start_x, start_y, end_x, end_y)
        
        self. calc_speed(O,A,H)
        self.angle = self.find_angle(O, A)
        self.angle = self.update_angle(self.angle, start_x, start_y, end_x, end_y)
        self.image = self.rot_center(self.image, self.angle)

        self.end_point_x = self.start_point_x
        self.end_point_y = self.start_point_y

        self.thrown = 'y'

        self.enemies = enemies

#$$$ AAA4
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

#$$$ AAA5
#$$$ Calculate speed
    def calc_speed(self, opposite, adjacent, hypotenuse):
        self.speed_x = adjacent/hypotenuse * self.speed
        self.speed_y = opposite/hypotenuse * self.speed

#$$$ AAA6
#Rotates an image around the image's center
    def rot_center(self, image, angle):
        loc = image.get_rect().center  #rot_image is not defined 
        rot_sprite = pygame.transform.rotate(image, angle)
        rot_sprite.get_rect().center = loc
        return rot_sprite

#$$$ AAA7
#this find the angle for the rope
    def find_angle(self, Opposite, Adjacent):
        angle_rads = Opposite/Adjacent
        angle_rads = math.atan(angle_rads)
        #now to convert from radians to degree
        angle_degrees = angle_rads * 180 / math.pi

        return angle_degrees

#$$$ AAA8
#this updates the angle based on which cooridantes the mouse is shot out at
    def update_angle(self, angle, player_x, player_y, mouse_x, mouse_y):
        if player_x > mouse_x:
            return -angle + 180
        else:
            return -angle