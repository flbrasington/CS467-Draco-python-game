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

class Rope(pygame.sprite.Sprite):
    #this class is for the rope that a player can shoot out to swing on objects

    #this is the constructor for the rope class
    def __init__(self):
         #call the parent's constructor
        super().__init__()

        #this creates the image for the block
        width = 10
        height = 10
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.PURPLE)

        self.width = width
        self.height = height
        
        #this sets up the image's rectanagle
        self.rect = self.image.get_rect()

        #this sets the location of the rope for shooting and swinging
        #rope_start_ is the location of the player. The rope will follow the player till the rope is
        #anchored int a wall
        self.rope_start_point_x = 0
        self.rope_start_point_y = 0
        #rope_end is the location of where the rope is shooting off to. 
        self.rope_end_x = 0
        self.rope_end_y = 0
        #rope_speed is the speed at which the rope travels
        self.rope_speed_x = 8
        self.rope_speed_y = 8
        #the rope length is the maximun length that the rope can travel.
        self.rope_length = 300
        #rope_change is the change in direction for the rope
        self.rope_change_x = 0
        self.rope_change_y = 0
        #rope_ex is for extending and retracting the rope.
            #e is for extend
            #r is for retract
            #a is for attached
            #n is for not being used
        self.ex = 'n'

        #this variable stores all the platfroms that the user can anchor a rope to
        self.level = None

    #this function allows the user to shoot a rope to be used for swinging & climbing
    def shoot_rope(self, player_x, player_y, player_width, player_height, direction):
        if self.ex == 'n':
            self.rect.x = player_x
            self.rect.y = player_y + player_height/2
            self.ex = 'e'
            self.rope_end_x = player_x + player_width/2
            self.rope_end_y = player_y + player_height/2

        if self.ex == 'e':
            if math.sqrt( (self.rope_end_x - (player_x + player_width/2) )**2 + (self.rope_end_y - (player_y + player_height/2))**2 ) <= self.rope_length:
                if direction == 'r':
                    self.rope_end_x += self.rope_speed_x
                else:
                    self.rope_end_x -= self.rope_speed_x
                self.rope_end_y -= self.rope_speed_y
                pygame.draw.aaline(constants.DISPLAYSURF, constants.PURPLE, ((player_x+ player_width/2), (player_y+ player_height/2)),(self.rope_end_x, self.rope_end_y))
            else:
                self.recall_rope(player_x, player_y, player_width, player_height)
        else:
            self.recall_rope(player_x, player_y, player_width, player_height)


    #this is the code for retracting the rope
    def recall_rope(self, player_x, player_y, player_width, player_height):
        if self.ex != 'a':
            if math.sqrt( (self.rope_end_x - (player_x + player_width/2) )**2 + (self.rope_end_y - (player_y + player_height/2))**2 ) >= 11:
                self.ex = 'r'
                if self.rope_end_x != (player_x + player_width/2):
                    if self.rope_end_x > (player_x + player_width/2):
                        self.rope_end_x -= self.rope_speed_x
                    else:
                        self.rope_end_x += self.rope_speed_x
                if self.rope_end_y != (player_y + player_height/2):
                    if self.rope_end_y > (player_y + player_height/2):
                        self.rope_end_y -= self.rope_speed_y
                    else:
                        self.rope_end_y += self.rope_speed_y
                pygame.draw.line(constants.DISPLAYSURF, constants.PURPLE, ((player_x + player_width/2), (player_y + player_height/2)),(self.rope_end_x,self.rope_end_y))
            else:
                self.ex = 'n'
        else:
            #this bit of code draws a line to show the rope between the player and the anchor
            pygame.draw.line(constants.DISPLAYSURF, constants.PURPLE, ((player_x + player_width/2), (player_y + player_height/2)),(self.rope_end_x,self.rope_end_y))

    #this updates the rope object to follow the player's movements
    def update_rope(self):
        if self.ex == 'n':
            self.rect.x = 0
            self.rect.y = 0

        elif self.ex == 'e' or self.ex == 'r':
            self.rect.x = self.rope_end_x
            self.rect.y = self.rope_end_y
            #this checks for the case when the rope's anchor hits an object.
            #if the anchor hits that object the extend variable (self.ex) will change to attach (a)
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            for block in block_hit_list:
                self.ex = 'a'


    #this updates the rope's extention status
    def change_extention_status(self):
        self.ex = 'n'
        


        
