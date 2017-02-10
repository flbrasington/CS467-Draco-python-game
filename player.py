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
from rope import Rope
import time
import sound_effects

CELL_HEIGHT = constants.SCREEN_HEIGHT / (constants.ROOM_HEIGHT * constants.ROOMS_ON_SCREEN)
CELL_WIDTH = constants.SCREEN_WIDTH / (constants.ROOM_WIDTH * constants.ROOMS_ON_SCREEN)


#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ --Quick Find - Ctrl + F-- $$$
#$$$ playermovement - AAA1     $$$
#$$$ player update - AAA2      $$$
#$$$ Check Max Speed - AAA3    $$$
#$$$ collision - AAA4          $$$
#$$$ Exit level - AAA5         $$$
#$$$ Gravity - AA6             $$$
#$$$ Double Jump - AA7         $$$
#$$$ Double Jump Timer - AAA8  $$$
#$$$ start/end/cooldown - AAA9 $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()

        
        #this loads all the sound effects & sound effect functions for the game
        self.soundEffects = sound_effects.Player_Sound_Effects()

        self.frame = 0

        #check if player has reached the exit
        self.exit_level = 'n'
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        #this sets the speed for walking and running
        self.walk_speed = 0.1  * CELL_WIDTH
        self.run_speed =  1.5 * self.walk_speed
        self.climb_speed = self.walk_speed

        #the below two variables are for the jump heights
        self.walk_jump = 7
        self.run_jump = 10
 
        # List of sprites we can bump against
        self.level = None

        #This is used to determine if the player is walking or running
        #w is for walk, r is for run
        self.walk_status = "w"

        #this variable is for stopping a player's jump in mid jump
        self.stop_jump = 'y'

        #this sets the player's direction to the right at the start of the game
        self.direction = 'r'

        #This variable is used to see if the player is walking
        #y: yes player is walking
        #n: no the player isn't walking
        self.walk_animation = 'y'
        
        #arrays that will hold images of sprite used for movement
        #l = left-facing and r = right-facing
        self.walking_frames_left = []
        self.walking_frames_right = []
        self.climbing_frames_up = []
        self.climbing_frames_down = []

        for i in range(1,10):
            filename = 'Graphics/spelunkyGuyWalk' + str(i) + '.png'
            image = pygame.image.load(filename)
            self.walking_frames_right.append(image)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_left.append(image)

        for i in range(1,11):
            filename = 'Graphics/spelunkyGuyClimb' + str(i) + '.png'
            image = pygame.image.load(filename)
            self.climbing_frames_up.append(image)
            self.climbing_frames_down.append(image)

        self.climbing_frames_down.reverse()

        self.image = self.walking_frames_right[0]

        self.rect = self.image.get_rect()
        self.jump_start_time = 0
        self.jump_end_time = 0
        self.can_double_jump = 'y'
        #this is for the double jump
        self.double_jump_count = 2

        #this is all for drawing lines for ropes
        #will be changed once coding is done
        self.rope_list = []
        self.current_rope = 0

        #this creates 10 rope objects
        self.num_of_ropes = 0
        for i in range(0,10):
            rope_object = Rope()
            rope_object.level = self.level
            self.rope_list.append(rope_object)
            self.num_of_ropes += 1
                    
        #this code is used for the cool down time for the ropes
        self.start_time = 0
        self.end_time = 0
        self.cool_down_time = 1
        self.can_shoot = True

        #this stores the player's current action
        #c: climbing
        #w: walking/running
        #j: jumping
        #f: falling
        self.action = 'w'


        
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ ----------------AAA1-------------------------$$$
#$$$ this function is for the player movements    $$$
#$$$ Summary of player movement                   $$$
#$$$ up/down/left right - wasd keys or arrow keys $$$
#$$$ jump/double jump - space bar                 $$$
#$$$ shoot rope - H key   (subject to change)     $$$
#$$$ walk/run - left/right shift key              $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def player_controls(self):
        pressed = pygame.key.get_pressed()

        #if the player clicks the left mouse button
        #a rope will travel in the direction of the mouse click
        #a cool down time will also begin, else the player will shoot too many ropes
        if pygame.mouse.get_pressed()[0]:
            if self.can_shoot == True:
                self.rope_list[self.current_rope].shoot_rope(self.rect.centerx, self.rect.centery,
                                                             pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                self.start_timer()
                self.current_rope += 1
                self.can_shoot = False
                if self.current_rope > self.num_of_ropes - 1:
                    self.current_rope = 0
            else:
                self.can_shoot = self.check_cool_down()

        #CHEAT FOR DEBUGGING ONLY
        if pressed[pygame.K_u]:
            self.double_jump()
            self.jump_start_time = 0
            self.jump_end_time = 0
            self.can_double_jump = 'y'
            self.double_jump_count = 2         
            
        if pressed[pygame.K_SPACE]:
            self.action = 'j'
            self.double_jump()


        if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
            self.walk_status = 'r'
        else:
            self.walk_status = 'w'

        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            if self.walk_status == 'r':
                self.change_x = -self.run_speed
            if self.walk_status == 'w':
                self.change_x = -self.walk_speed

            self.direction = 'l'
            
            if  self.walk_animation == 'y':
                self.frame = (self.frame + 1) % len(self.walking_frames_left)
                self.image = self.walking_frames_left[self.frame]
                if self.frame > len(self.walking_frames_right):
                    self.frame = 0
                #this plays the sound effect for walking
                if self.walk_status == 'w':
                    self.soundEffects.player_walking_sound()
                else:
                    #plays the player's running sound effect
                    self.soundEffects.player_running_sound()
            else:
                self.image = self.walking_frames_left[0]

        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            if self.walk_status == 'r':
                self.change_x = self.run_speed
            if self.walk_status == 'w':
                self.change_x = self.walk_speed

            self.direction = 'r'

            if self.walk_animation == 'y':
                self.frame = (self.frame + 1) % len(self.walking_frames_right)
                self.image = self.walking_frames_right[self.frame]
                if self.frame > len(self.walking_frames_right):
                    self.frame = 0
                #this plays the sound effect for walking
                if self.walk_status == 'w':
                    self.soundEffects.player_walking_sound()
                else:
                    #plays the player's running sound effect
                    self.soundEffects.player_running_sound()
            else:
                self.image = self.walking_frames_right[0]

        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            block_hit_list = pygame.sprite.spritecollide(self, self.level.exit_sprite, False)
            for block in block_hit_list:
                if pressed[pygame.K_UP]:
                    self.exit_level = 'y'

            #if the player wants to climb the rope
            self.action = 'w'
            for rope in self.rope_list:
                rope_hit_list = pygame.sprite.spritecollide(self, rope.rope_segments, False)
                for seg in rope_hit_list:
                    self.action = 'c'
                    self.change_y = -self.climb_speed
                    self.can_double_jump = 'y'
                    #this is for the double jump
                    self.double_jump_count = 2

        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            if self.action == 'c':
                #if the player wants to climb the rope
                self.action = 'w'
                for rope in self.rope_list:
                    rope_hit_list = pygame.sprite.spritecollide(self, rope.rope_segments, False)
                    for seg in rope_hit_list:
                        self.action = 'c'
                        self.change_y = self.climb_speed
                        self.can_double_jump = 'y'
                        #this is for the double jump
                        self.double_jump_count = 2
            
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.soundEffects.player_sounds_stop()#stops the player's walk/run sound effect
                    self.change_x = 0
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.soundEffects.player_sounds_stop()#stops the player's walk/run sound effect
                    self.change_x = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.change_y = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.change_y = 0 
        
        
#AAA2
#the update function includes all the effects happening to the player
#as well as updating the rope objects,
#the effects of gravity
    def update(self, player=None):

        #this updates all the ropes as needed
        for rope in self.rope_list:
            rope.update_rope()
        
        #this section recieves input from the user.
        #for user commands see player.py
        #checks if the shift key is being pushed which will allow the player to run
        self.player_controls()
        
        # Gravity
        self.calc_grav()
 
        # Move left/right
        #this makes sure that change_x doesn't get too great else the player can fly around the screen
        if self.action != 'c':
            self.change_x = self.max_speed(self.change_x)
            self.rect.x += self.change_x

        #this checks for any collisons with blocks
        self.collision_blocks_x()
 
        # Move up/down
        #also checks that the player doesn't fall or fly too quickly
        self.change_y = self.max_speed(self.change_y)
        self.rect.y += self.change_y

        #this checks for any collisons with blocks up/down
        self.collision_blocks_y()

#AAA3
#this limits the maximun speed of the player
#if the speed (or change_x/change_y) is greater than 10 then limit that number to 10
    def max_speed(self, speed=None):
        if abs(speed) > 10:
            if speed < 0:
                speed = -10
            else:
                speed = 10
        return speed

#AAA4
    def collision_blocks_x(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

#AAA5
    def collision_blocks_y(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.double_jump_count = 2
                self.walk_animation = 'y'
                self.stop_jump = 'y'
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
#AAA6
    def calc_grav(self):
        #if the player is not climbing the rope
        if self.action != 'c':
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35
                    
         
            # See if we are on the ground.
            if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
                self.change_y = 0
                self.rect.y = constants.SCREEN_HEIGHT - self.rect.height


#AAA7
    def double_jump(self):
        """ Called when user hits 'double jump' button. """
        if self.double_jump_count > 0:
            if self.can_double_jump == 'y':
                self.jump_start_time = time.clock()
                self.can_double_jump = 'n'
                self.double_jump_count -= 1
            
                # move down a bit and see if there is a platform below us.
                # Move down 2 pixels because it doesn't work well if we only move down
                # 1 when working with a platform moving down.
                self.rect.y += 2
                platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                self.rect.y -= 2

                self.change_y -= self.walk_jump

            elif self.can_double_jump == 'n':
                if self.double_jump_timer() > .33:
                    self.can_double_jump = 'y'
                
#AAA8
    #this function is used to delayed te double jump for the player
    def double_jump_timer(self):
        self.end_time = time.clock()
        return self.end_time - self.jump_start_time


#AAA9
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


            
