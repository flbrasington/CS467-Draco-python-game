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
from projectiles import Knife
#from whip import Whip
import time
import sound_effects
import graphics
from health import Health
import GameOver

import Level

CELL_HEIGHT = constants.SCREEN_HEIGHT / constants.ROOM_HEIGHT
CELL_WIDTH = constants.SCREEN_WIDTH / constants.ROOM_WIDTH


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
#$$$ Take Damage - AAA10       $$$
#$$$ Hit enemies - AAA11       $$$
#$$$ throw rope - AAA12        $$$
#$$$ Throw knife - AAA13       $$$
#$$$ Player Animation - AAA14  $$$
#$$$ Damage animation - AAA15  $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$



#$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$ Ctrl-f && for testing $$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self):
        """ Constructor function """

 
        # Call the parent's constructor
        super().__init__()


        #sets the block for climbing
        self.block = None

        #this loads all the sound effects & sound effect functions for the game
        self.soundEffects = sound_effects.Player_Sound_Effects()

        self.frame = 0

        #check if player has reached the exit
        self.exit_level = 'n'
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        #this sets the speed for walking and running
        self.walk_speed = 0.04  * CELL_WIDTH * 1.1
        self.run_speed =  1.3 * self.walk_speed * 1.1
        self.climb_speed = self.walk_speed

        #the below two variables are for the jump heights
        self.walk_jump = 11
        self.run_jump = 14
 
        # List of sprites we can bump against
        self.level = None

        #added the enemies to the list
        self.enemies = None

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
        self.attacking_frames_left = []
        self.attacking_frames_right = []
        self.wall_climbing_left = []
        self.wall_climbing_right = []

        for img in graphics.spelunkyGuyWalk:
            image = pygame.image.load(img)
            self.walking_frames_right.append(image)
            image = pygame.transform.flip(image, True, False)
            self.walking_frames_left.append(image)

        for img in graphics.spelunkyGuyClimb:
            image = pygame.image.load(img)
            self.climbing_frames_up.append(image)
            self.climbing_frames_down.append(image)

        for img in graphics.spelunkyGuyAttack:
            image = pygame.image.load(img)
            self.attacking_frames_right.append(image)
            self.attacking_frames_right.append(image)
            self.attacking_frames_right.append(image)
            image = pygame.transform.flip(image, True, False)
            self.attacking_frames_left.append(image)
            self.attacking_frames_left.append(image)
            self.attacking_frames_left.append(image)

        for img in graphics.spelunkyGuyWallClimbLeft:
            image = pygame.image.load(img)
            image = pygame.transform.flip(image, True, False)
            self.wall_climbing_left.append(image)
            self.wall_climbing_left.append(image)

        for img in graphics.spelunkyGuyWallClimbRight:
            image = pygame.image.load(img)
            self.wall_climbing_right.append(image)
            self.wall_climbing_right.append(image)

        #sets up the taking damage images    
        self.take_damage_img = []
        image = graphics.spelunkyGuyDamage
        self.take_damage_img.append(image)
        image = pygame.transform.flip(image, True, False)
        self.take_damage_img.append(image)

        self.climbing_frames_down.reverse()

        self.image = self.walking_frames_right[0]

        self.rect = self.image.get_rect()
        self.jump_start_time = 0
        self.jump_end_time = 0
        self.can_double_jump = 'y'
        #this is for the double jump
        #self.double_jump_count = 2
        #&&
        self.double_jump_count = 1



        #this is all for drawing lines for ropes
        #will be changed once coding is done
        self.rope_list = []
        self.current_rope = 0

        #this creates 10 rope objects
        self.num_of_ropes = 0
        self.total_ropes = 0
        for i in range(0, 10):
            rope_object = Rope()
            rope_object.level = self.level
            self.rope_list.append(rope_object)
            self.num_of_ropes += 1
            self.total_ropes += 1

        #the following code is for the player's knives
        self.knife_list = []
        self.current_knife = 0
        self.num_of_knives = 0
        self.total_knives = 0
        for i in range(0, 10):
            knife_object = Knife()
            knife_object.level = self.level
            self.knife_list.append(knife_object)
            self.num_of_knives += 1
            self.total_knives += 1


        #loads in the whip objects
        #self.whip = Whip()
        
                    
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
        #wc: wall climbing
        self.action = 'w'

        #this adds the health object to the player
        self.health = Health()

        #this loads the empty image for the taking damage
        self.empty = pygame.image.load('Graphics/SpelunkyGuy/empty.png')

        #this is to set the amount of time that the player is invicable after taking damage
        self.damage_timer = 1 #currently set to 1 sec of invicablily
        self.damage_start_time = 0
        self.damage_end_time = 0

        #this sets the timer and image if the player is taking damage
        #n: not taking damage
        #y: player is or has taken damage
        self.damage = 'n'

        #This variable is for selecting which item is currently selected by the player
        #r: rope selected
        #k: knife selected
        #w: whip selected
        self.inv = 0
        self.item = ['r','k']
        #this is a small timer added so that the player has time to select what item they want
        self.inv_start_time = 0
        self.inv_end_time = 0
        self.inv_timer = 0.1

        #used for animations
        self.player_status = 'walk'

        self.knifePickup = False
        self.ropePickup = False


        
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#$$$ ----------------AAA1-------------------------$$$
#$$$ this function is for the player movements    $$$
#$$$ Summary of player movement                   $$$
#$$$ up/down/left right - wasd keys or arrow keys $$$
#$$$ jump/double jump - space bar                 $$$
#$$$ shoot rope - H key   (subject to change)     $$$
#$$$ walk/run - left/right shift key              $$$
#$$$ switch item - Right Click                    $$$
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    def player_controls(self):
        pressed = pygame.key.get_pressed()

        #if the player isn't taking damage
        if self.action != 'td' and self.player_status != 'take_damage':

            #if the player clicks the left mouse button
            #a rope will travel in the direction of the mouse click
            #a cool down time will also begin, else the player will shoot too many ropes
            if pygame.mouse.get_pressed()[0]:
                if self.player_status != 'attack':
                        self.player_status = 'attack'
                        self.frame = 0
                        if pygame.mouse.get_pos()[0] > self.rect.x:
                            self.direction = 'r'
                        else:
                            self.direction = 'l'

                if self.inv == 0:
                    self.throw_rope()
                elif self.inv == 1:
                    self.throw_knife()
                #else:
                #    self.whip.direction = self.direction
                #    self.whip.whip_being_used = 'y'

                

            #this is for changing the player's inventory
            if pygame.mouse.get_pressed()[2]:
                if self.inv_start_time == 0:
                    self.start_timer('i')
                    if self.inv >= 1:
                        self.inv = 0
                    else:
                        self.inv += 1
                else:
                    #checks that the cool down is finished
                    self.end_timer('i')
                    inv_time = self.inv_end_time - self.inv_start_time
                    if inv_time > self.inv_timer:
                        self.inv_start_time = 0

            #CHEAT FOR DEBUGGING ONLY
            if pressed[pygame.K_u]:
                self.double_jump()
                self.jump_start_time = 0
                self.jump_end_time = 0
                self.can_double_jump = 'y'
                #&& self.double_jump_count = 2   
                self.double_jump_count = 1         
                
            if pressed[pygame.K_SPACE]:
                self.action = 'j'
                self.double_jump()


            if pressed[pygame.K_LSHIFT] or pressed[pygame.K_RSHIFT]:
                self.walk_status = 'r'
            else:
                self.walk_status = 'w'

            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                if self.action != 'wc':
                    if self.action != 'c':
                        self.direction = 'l'
                        if self.walk_status == 'r':
                            self.change_x = -self.run_speed
                        if self.walk_status == 'w':
                            self.change_x = -self.walk_speed


                        self.player_status = 'walk'
                        self.player_animation()

            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                if self.action !='wc':
                    if self.action != 'c':
                        if self.walk_status == 'r':
                            self.change_x = self.run_speed
                        if self.walk_status == 'w':
                            self.change_x = self.walk_speed

                        if self.action != 'wc':
                            self.direction = 'r'

                        self.player_status = 'walk'
                        self.player_animation()
                        
                        

            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                block_hit_list = pygame.sprite.spritecollide(self, self.level.exit_sprite, False)
                for block in block_hit_list:
                    if pressed[pygame.K_UP]:
                        self.exit_level = 'y'

                bagHitList = pygame.sprite.spritecollide(self, self.level.bagGroup, True)
                for bag in bagHitList:
                    if bag.type == 'knife':
                        self.knifePickup = True
                    elif bag.type == 'rope':
                        self.ropePickup = True

                #if the player wants to climb the rope
                #self.action = 'w'
                if self.action != 'wc':
                    temp = 'f'
                    for rope in self.rope_list:
                        rope_hit_list = pygame.sprite.spritecollide(self, rope.rope_segments, False)
                        for seg in rope_hit_list:
                            temp = 'c'
                            self.change_y = -self.climb_speed
                            self.can_double_jump = 'y'
                            #this is for the double jump
                            #&& self.double_jump_count = 2
                            self.double_jump_count = 1
                            
                            self.player_status = 'climb'
                            self.player_animation()

                    self.action = temp

                elif self.action == 'wc':
                    self.change_y = -self.climb_speed
                    self.player_status = 'wall_climb'
                    self.player_animation()
                    self.can_double_jump = 'y'
                    #&& self.double_jump_count = 2
                    self.double_jump_count = 1
                        
            if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
                if self.action == 'wc':
                    self.change_y = self.climb_speed
                    self.can_double_jump = 'y'
                    #this is for the double jump
                    #&& self.double_jump_count = 2
                    self.double_jump_count = 1
                    self.player_animation()

                    
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
                            #&& self.double_jump_count = 2
                            self.double_jump_count = 1

                            self.player_status = 'climb'
                            self.player_animation()
                
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.action != 'wc':
                            self.soundEffects.player_sounds_stop()#stops the player's walk/run sound effect
                            self.change_x = 0
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.action != 'wc':
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

        #this updates the knives as needed
        # for knife in self.knife_list:
            # knife.update_projectile()

        #this updates the whip as needed
        #self.whip.whip_update(self.rect.centerx, self.rect.centery)

        #adds attack animation
        if self.player_status == 'attack':
            self.player_animation()

        
        #this section recieves input from the user.
        #for user commands see player.py
        #checks if the shift key is being pushed which will allow the player to run
        self.player_controls()
        
        # Gravity
        self.calc_grav()
        self.move_left_right()
 
        # Move left/right
        #this makes sure that change_x doesn't get too great else the player can fly around the screen
        if self.action != 'c':
            if self.action != 'wc':
                self.change_x = self.max_speed_x(self.change_x)
        self.rect.x += self.change_x

        #this checks for any collisons with blocks
        self.collision_blocks_x()
 
        # Move up/down
        #also checks that the player doesn't fall or fly too quickly
        self.change_y = self.max_speed_y(self.change_y)
        self.rect.y += self.change_y

        #this checks for any collisons with blocks up/down
        self.collision_blocks_y()

        #this checks for collision with enemies
        # self.collision_enemies()

        #this checks the damage for the player
        self.take_damage()

#AAA3
#this limits the maximun speed of the player
#if the speed (or change_x/change_y) is greater than 10 then limit that number to 10
    def max_speed_x(self, speed=None):
        if abs(speed) > 9:
            if speed < 0:
                speed = -9
            else:
                speed = 9
        return speed
        
    def max_speed_y(self, speed=None):
        if abs(speed) > 18:
            if speed < 18:
                speed = -18
            else:
                speed = 18
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

            #sets up for climbing walls
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP] or pressed[pygame.K_w]:
                fall = False
                if self.action != 'wc':
                    self.block = block
                    self.wall_x = self.block.rect.x
                            
                    print("wall_x = ", self.wall_x)
                    if self.direction == 'r':
                        self.rect.right = block.rect.left
                    self.change_y = 0
                    self.action = 'wc'
                    self.player_status = 'wall_climb'


#AAA5
    def collision_blocks_y(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                #&& self.double_jump_count = 2
                self.double_jump_count = 1
                self.walk_animation = 'y'
                self.stop_jump = 'y'
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0


#AAA11
    # def collision_enemies(self):
    #     enemy_hit_list = pygame.sprite.spritecollide(self, self.enemies, False)
    #     for bad_guy in enemy_hit_list:
    #         if bad_guy.action == 'a':
    #             if self.damage == 'n':
    #                 self.damage = 'y'
    #                 self.damage_start_time = 0

        
#AAA6
    def calc_grav(self):
        #if the player is not climbing the rope

        if self.action != 'c' and self.action != 'wc':
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .6
         
            # See if we are on the ground.
            if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
                self.change_y = 0
                self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

            if self.change_y > 0:
                self.falling = True


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
    def start_timer(self, action = 'n'):
        if action == 'n':
            self.start_time = time.clock()
        elif action == 'i': #i for inventory
            self.inv_start_time = time.clock()
        else:
            self.damage_start_time = time.clock()

    def end_timer(self, action = 'n'):
        if action == 'n':
            self.end_time = time.clock()
        elif action == 'i':
            self.inv_end_time = time.clock()
        else:
            self.damage_end_time = time.clock()

    def check_cool_down(self):
        self.end_time = time.clock()
        if self.end_time - self.start_time > self.cool_down_time:
            return True
        else:
            return False

#AAA10
    #this function allows the player to take damage and then starts a countdown
    def take_damage(self):
        if self.damage == 'y':
            if self.damage_start_time == 0:
                self.action = 'td'
                self.player_status = 'take_damage'
                self.start_timer('y')
                self.health.update_health()
                if self.direction == 'r':
                    self.image = self.take_damage_img[0]
                    self.change_x = 10
                else:
                    self.image = self.take_damage_img[1]
                    self.change_x = -10
            else:
                self.end_timer('y')
                if self.direction == 'r':
                    self.change_x -= .15
                else:
                    self.change_x += .15
                time = self.damage_end_time - self.damage_start_time
                if time > self.damage_timer:
                    self.damage = 'n'
                    self.change_x = 0
                    self.action = 'f'
                    self.player_status = 'fall'
                    if self.health.life == 0:
                        GameOver.Game_Over_Screen()

#AAA12
    def throw_rope(self):
        if self.can_shoot and self.num_of_ropes > 0:
            # print("current rope = ", self.current_rope)
            # print("num_of_ropes = ", self.num_of_ropes)
            self.rope_list[self.current_rope].shoot_rope(self.rect.centerx, self.rect.centery,
                                                         pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            self.start_timer()
            self.current_rope += 1
            self.num_of_ropes -= 1
            self.can_shoot = False
            if self.current_rope > self.total_ropes - 1:
                self.current_rope = 0
                if self.num_of_ropes > 0:
                    self.num_of_ropes -= 1
        else:
            self.can_shoot = self.check_cool_down()

#AAA13
    def throw_knife(self):
        if self.can_shoot and self.num_of_knives > 0:
            self.knife_list[self.current_knife].shoot(self.rect.centerx, self.rect.centery,
                                                            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], self.level.enemy_list)
            self.start_timer()

            self.current_knife += 1
            self.num_of_knives -= 1
            self.can_shoot = False

            if self.current_knife > self.total_knives - 1:
                self.current_knife = 0
                # self.num_of_knives-= 1
            print("knives", self.num_of_knives)
        else:
            self.can_shoot = self.check_cool_down()

#AAA14
    def player_animation(self):
        if self.player_status == 'walk':
            self.player_walk_animation()
        if self.player_status == 'climb':
            self.player_climb_animation()
        if self.player_status == 'attack':
            self.player_attack_animation()
        if self.player_status == 'wall_climb':
            self.player_wall_climb_animation()
        if self.player_status == 'fall':
            self.frame = 0
            self.image = self.walking_frames_left[self.frame]

#AAA15
    def player_walk_animation(self):
        if self.direction == 'l':
            if self.walk_animation == 'y':
                if self.frame > len(self.walking_frames_right):
                    self.frame = 0
                    
                self.frame = (self.frame + 1) % len(self.walking_frames_left)
                self.image = self.walking_frames_left[self.frame]
                
                #this plays the sound effect for walking
                if self.walk_status == 'w':
                    self.soundEffects.player_walking_sound()
                else:
                    #plays the player's running sound effect
                    self.soundEffects.player_running_sound()
            else:
                self.image = self.walking_frames_left[0]
        else:
            if self.walk_animation == 'y':

                if self.frame > len(self.walking_frames_right):
                    self.frame = 0
                    
                self.frame = (self.frame + 1) % len(self.walking_frames_right)
                self.image = self.walking_frames_right[self.frame]
                
                #this plays the sound effect for walking
                if self.walk_status == 'w':
                    self.soundEffects.player_walking_sound()
                else:
                    #plays the player's running sound effect
                    self.soundEffects.player_running_sound()
            else:
                self.image = self.walking_frames_right[0]
#AAA16
    def player_climb_animation(self):
        self.frame = (self.frame + 1) % len(self.climbing_frames_up)
        self.image = self.climbing_frames_up[self.frame]
        if self.frame > len(self.climbing_frames_up):
            self.frame = 0

#AAA17
    def player_attack_animation(self):
        if self.frame >= 12:
            self.frame = 0
            self.player_status = 'walk'
            if self.direction == 'r':
                self.image = self.walking_frames_right[self.frame]
            else:
                self.image = self.walking_frames_left[self.frame]

        if self.direction == 'r':

                self.frame = (self.frame + 1) % len(self.attacking_frames_right)
                self.image = self.attacking_frames_right[self.frame]
        else:
                if self.frame > len(self.attacking_frames_left):
                    self.frame = 0

                self.frame = (self.frame + 1) % len(self.attacking_frames_left)
                self.image = self.attacking_frames_left[self.frame]

#AAA18
    def player_wall_climb_animation(self):
        if self.frame >= 15:
            self.frame = 0
            self.player_status = 'wall_climb'

        self.frame = (self.frame + 1) % len(self.wall_climbing_left)

        if self.direction == 'l':
            self.image = self.wall_climbing_left[self.frame]
        else:
            self.image = self.wall_climbing_right[self.frame]


    def move_left_right(self):
        if self.action == 'wc':
            if self.direction == 'l':
                if self.rect.x -self.block.rect.width != self.block.rect.x:
                     self.action = 'f'
                     self.player_status = 'fall'
                     self.change_x = 0
                     self.player_animation()
                else:
                    if self.direction == 'l':
                        self.change_x = -2
                    else:
                        self.change_x = 2
            else:
                if self.rect.x + self.rect.width != self.block.rect.x:
                     self.action = 'f'
                     self.player_status = 'fall'
                     self.change_x = 0
                     self.player_animation()
                else:
                    if self.direction == 'l':
                        self.change_x = -2
                    else:
                        self.change_x = 2

