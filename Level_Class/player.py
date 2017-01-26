'''
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file stores all the functions and objects related to the player.
Here is where you will find things such as the player's sprite's sheet,
movement and actions.

'''
import pygame
import constants
import math
import rope

CELL_HEIGHT = constants.SCREEN_HEIGHT / (constants.ROOM_HEIGHT * constants.ROOMS_ON_SCREEN)
CELL_WIDTH = constants.SCREEN_WIDTH / (constants.ROOM_WIDTH * constants.ROOMS_ON_SCREEN)


class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 

        #adds the rope object to the player
        #self.rope_object = rope.Rope()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.RED)

        self.width = width
        self.height = height
        
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        #this sets the speed for walking and running
        # self.walk_speed = 4
        # self.run_speed = 8

        self.walk_speed = 0.1  * CELL_WIDTH
        self.run_speed =  1.5 * self.walk_speed

        #the below two variables are for the jump heights
        self.walk_jump = 6
        self.run_jump = 12
        #self.walk_jump = CELL_HEIGHT
        #self.run_jump = CELL_HEIGHT
 
        # List of sprites we can bump against
        self.level = None

        #This is used to determine if the player is walking or running
        #w is for walk, r is for run
        self.walk_status = "w"

        #this variable checks if the bottom of the spirte is touching something else our player will
        #be able to jump in mid air
        #y for yes the player can jump
        #and no for the player can not jump
        self.can_jump = 'y'
        #this variable is for stopping a player's jump in mid jump
        self.stop_jump = 'y'


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
        #e is for extend and r is for retract
        self.ex = 'e'

        #This sets up which direction the player is facing
        #r is for right, l for left
        self.direction = 'r'
        


    #this function allows the user to shoot a rope to be used for swinging & climbing
    def shoot_rope(self):
        if self.ex == 'e':
            if math.sqrt( (self.rope_end_x - (self.rect.x +self.width/2) )**2 + (self.rope_end_y - (self.rect.y +self.height/2))**2 ) <= self.rope_length:
                if self.direction == 'r':
                    self.rope_end_x += self.rope_speed_x
                else:
                    self.rope_end_x -= self.rope_speed_x
                self.rope_end_y -= self.rope_speed_y
                pygame.draw.aaline(constants.DISPLAYSURF, constants.PURPLE, ((self.rect.x+ self.width/2), (self.rect.y+ self.height/2)),(self.rope_end_x,self.rope_end_y))
            else:
                self.recall_rope()
        else:
            self.recall_rope()


    #this is the code for retracting the rope
    def recall_rope(self):
        if math.sqrt( (self.rope_end_x - (self.rect.x +self.width/2) )**2 + (self.rope_end_y - (self.rect.y +self.height/2))**2 ) >= 11:
            self.ex = 'r'
            if self.rope_end_x != (self.rect.x + self.width/2):
                if self.rope_end_x > (self.rect.x + self.width/2):
                    self.rope_end_x -= self.rope_speed_x
                else:
                    self.rope_end_x += self.rope_speed_x
            if self.rope_end_y != (self.rect.y + self.height/2):
                if self.rope_end_y > (self.rect.y + self.height/2):
                    self.rope_end_y -= self.rope_speed_y
                else:
                    self.rope_end_y += self.rope_speed_y
            pygame.draw.aaline(constants.DISPLAYSURF, constants.PURPLE, ((self.rect.x+ self.width/2), (self.rect.y+ self.height/2)),(self.rope_end_x,self.rope_end_y))
        else:
            self.ex = 'e'



    def update(self):
        #this updates the location of the anchor for the rope
        #self.rope_object.update_rope(self.rect.x, self.rect.y, self.width, self.height)
        
        #this section recieves input from the user.
        #for user commands see player.py
        #checks if the shift key is being pushed which will allow the player to run

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LSHIFT]:
            self.walk_status = 'r'
        else:
            self.walk_status = 'w'

        if pressed[pygame.K_LEFT]:
            if self.walk_status == 'r':
                self.change_x = -self.run_speed
            if self.walk_status == 'w':
                self.change_x = -self.walk_speed
            self.direction = 'l'

        if pressed[pygame.K_RIGHT]:
            if self.walk_status == 'r':
                self.change_x = self.run_speed
            if self.walk_status == 'w':
                self.change_x = self.walk_speed
            self.direction = 'r'

        if pressed[pygame.K_z]:
                if self.can_jump == 'y':
                    self.jump()

        if pressed[pygame.K_x]:
            self.shoot_rope()
        else:
            self.recall_rope()
            
                       

        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.change_x = 0
                if event.key == pygame.K_RIGHT:
                    self.change_x = 0
                if event.key == pygame.K_z:
                    if self.stop_jump == 'y':
                        self.change_y = 0
                        self.stop_jump = 'n'
                    
                    
                    
        """ Move the player. """
        # Gravity
        self.calc_grav()
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.can_jump = 'y'
                self.stop_jump = 'y'
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
            #self.change_y += 1.8
 
        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """

        #sets the user's ability to jump back to not jump
        self.can_jump = 'n'
        
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            # If it is ok to jump, set our speed upwards
            if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
                #if the player is walking/standing
                if self.walk_status == 'w':
                    self.change_y -= self.walk_jump
                #if the player is running
                if self.walk_status == 'r':
                    self.change_y -= self.run_jump
        else:
            self.change_y = 0
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0