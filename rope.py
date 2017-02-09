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
#$$$ Timer functions - AAA5                $$$
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
        self.draw_line = 'n'

        #this is used for calculating the speed of which the rope is shot out and the direction
        self.speed = 10
        self.speed_x = 0
        self.speed_y = 0
        
        self.start_time = 0
        self.end_time = 0
        self.cool_down_time = 1


#$$$ AAA3
    def update_rope(self):
        if self.draw_line == 'y':
            self.end_point_x += self.speed_x
            self.end_point_y += self.speed_y
            pygame.draw.lines(constants.DISPLAYSURF, constants.ROPE, False, [(self.start_point_x,self.start_point_y),
                                                                             (self.end_point_x,self.end_point_y)], 8)
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

        self.end_point_x = self.start_point_x
        self.end_point_y = self.start_point_y

        
        self.draw_line = 'y'

#$$$ AAA5
    def start_timer(self):
        self.start_time = time.clock()

    def end_timer(self):
        self.end_time = time.clock()

    def check_cool_down(self):
        self.end_time = time.clock()
        if self.end_time - self.start_time > self.cool_down_time:
            return True
        else:
            return False

#$$$ AAA1
    def find_Opposite(self, start_y, end_y):
        return end_y - start_y
    
    def find_Adjacent(self, start_x, end_x):
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
        
