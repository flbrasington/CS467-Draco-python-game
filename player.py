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
from spritesheet import SpriteSheet
import time

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


        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 60

        self.frame = 0
        # self.image = pygame.Surface([width, height])
        # self.image.fill(constants.RED)

        self.width = width
        self.height = height
        
        # Set a referance to the image rect.
        # self.rect = self.image.get_rect()
 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0

        #this sets the speed for walking and running
        # self.walk_speed = 4
        # self.run_speed = 8

        self.walk_speed = 0.1  * CELL_WIDTH
        self.run_speed =  1.5 * self.walk_speed

        #the below two variables are for the jump heights
        self.walk_jump = 7
        self.run_jump = 10
 
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

        #adds the rope object to the player
        self.rope_object = Rope()

        #the following code is used for when the rope's anchor is attached to a platform
        self.swing_speed = .35
        #this variable is for slowing the swing speed down, other wise the player will swing back and forth forever
        self.swing_speed_slowdown = .70

        #this sets the player's direction to the right at the start of the game
        self.direction = 'r'

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
        
        
    def update(self):
        #this updates the location of the anchor for the rope
        if self.rope_object.ex == 'a':
            self.double_jump_count = 2
        self.rope_object.update_rope()
        
        #this section recieves input from the user.
        #for user commands see player.py
        #checks if the shift key is being pushed which will allow the player to run

        pressed = pygame.key.get_pressed()
            

        if pressed[pygame.K_f]:
            self.double_jump()
            #this detaches the anchors when the player jumps
            if self.rope_object.ex == 'a':
            #this starts the timer for the rope.
                #the player will be able to use the rope again afer the cool_down time has expired
                self.rope_object.start_timer()
                    
                #this allows the player to jump while attached to a rope
                self.double_jump()
                #this stops the player from sliding to the left or right after swinging on the rope
                self.change_x = 0
                #this returns the anchor to the space space
                self.rope_object.change_extention_status()


        if pressed[pygame.K_LSHIFT]:
            self.walk_status = 'r'
        else:
            self.walk_status = 'w'

        if pressed[pygame.K_LEFT]:
            #if the player isn't hanging on to a rope
            if self.rope_object.ex != 'a':
                if self.walk_status == 'r':
                    self.change_x = -self.run_speed
                if self.walk_status == 'w':
                    self.change_x = -self.walk_speed
            self.direction = 'l'

            #if the player is hanging on to the rope
            """
            if self.rope_object.ex == 'a':
                distance = self.rope_distance()
                print (distance)
                if distance < (self.rope_object.rope_length - 100):
                    self.change_x -= self.walk_speed
                    self.calc_grav()
            """

            if  self.can_jump == 'y':
                self.frame = (self.frame + 1) % len(self.walking_frames_left)
                self.image = self.walking_frames_left[self.frame]
            else:
                self.image = self.walking_frames_left[0]

        if pressed[pygame.K_RIGHT]:
            #if the player isn't hanging on to a rope
            if self.rope_object.ex != 'a':
                if self.walk_status == 'r':
                    self.change_x = self.run_speed
                if self.walk_status == 'w':
                    self.change_x = self.walk_speed

            """
            #if the player is hanging on to the rope
            if self.rope_object.ex == 'a':
                distance = self.rope_distance()
                print (distance)
                if distance < (self.rope_object.rope_length - 100):
                    self.change_x += self.walk_speed
                    self.calc_grav()
            """

            self.direction = 'r'

            if self.can_jump == 'y':
                self.frame = (self.frame + 1) % len(self.walking_frames_right)
                self.image = self.walking_frames_right[self.frame]
            else:
                self.image = self.walking_frames_right[0]

        #the UP arrow keys does the following:
            #if the player is holding on to the rope the player can climb up the rope to the rope's anchor
        if pressed[pygame.K_UP]:
            #if the player is holding on the to the rope
            if self.rope_object.ex == 'a':
                #the player can't climb higher than the rope's anchor
                if self.rope_object.rect.y < self.rect.y:
                    self.change_y = -self.walk_speed
                else:
                    self.change_y = 0
                self.frame = (self.frame + 1) % len(self.climbing_frames_up)
                self.image = self.climbing_frames_up[self.frame]

        #the DOWN arrow Key does the following:
            #if the player is holding on to the rope the player can climb down the rope
        if pressed[pygame.K_DOWN]:
            #if the player is holding on the to the rope
            if self.rope_object.ex == 'a':
                #the player can't climb lower than the rope's length
                if (self.rect.y - self.rope_object.rect.y) < self.rope_object.rope_length/3:
                    print((self.rect.y - self.rope_object.rect.y))
                    self.change_y = self.walk_speed
                else:
                    self.change_y = 0 
        

        if pressed[pygame.K_z]:
                if self.can_jump == 'y':
                    self.jump()
                #this detaches the anchors when the player jumps
                if self.rope_object.ex == 'a':
                    #this starts the timer for the rope.
                        #the player will be able to use the rope again afer the cool_down time has expired
                    self.rope_object.start_timer()
                    
                    #this allows the player to jump while attached to a rope
                    self.jump()
                    #this stops the player from sliding to the left or right after swinging on the rope
                    self.change_x = 0
                    #this returns the anchor to the space space
                    self.rope_object.change_extention_status()

        #the x button is used for the following
            #when the player is touching the ground
                #shoots the rope if the rope timer is is valid
            #when hanging from the rope
                #no effect
        if pressed[pygame.K_x]:
            can_shoot_rope = self.rope_object.check_cool_down()
            if can_shoot_rope == True:
                self.rope_object.shoot_rope(self.rect.x, self.rect.y, self.width, self.height, self.direction)
        else:
            if self.rope_object.ex != 'n':
                self.rope_object.recall_rope(self.rect.x, self.rect.y, self.width, self.height)
            
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.change_x = 0
                if event.key == pygame.K_RIGHT:
                    self.change_x = 0
                if event.key == pygame.K_UP:
                    if self.rope_object.ex == 'a':
                        self.change_y = 0
                if event.key == pygame.K_z:
                    if self.stop_jump == 'y':
                        self.change_y = 0
                        self.stop_jump = 'n'

        #this swings the player if the player is attached to a rope
        if self.rope_object.ex == 'a':
            self.attached_rope()
            
                    
        """ Move the player. """
        # Gravity
        #this moves the player down if the player isn't attached to a rope
        self.calc_grav()
 
        # Move left/right
        #this makes sure that change_x doesn't get too great else the player can fly around the screen
        if abs(self.change_x) > 10:
            if self.change_x < 0:
                self.change_x = -10
            elif self.change_x > 0:
                self.change_x = 10
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
            #this stops the player from swinging wildly when attached to the rope
            if self.rope_object.ex == 'a':
                self.change_x = 0
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.double_jump_count = 2
                self.can_jump = 'y'
                self.stop_jump = 'y'
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.rope_object.ex == 'n':
            if self.change_y == 0:
                self.change_y = 1
            else:
                self.change_y += .35
                #self.change_y += 1.8
        elif self.rope_object.ex == 'a':
            distance = self.rope_distance()
            if distance < self.rope_object.rope_length - 100:
                if self.change_y == 0:
                    self.change_y = 1
                else:
                    self.change_y += .35
            else:
                #This stops the player from falling down too far
                if self.change_y > 0:
                    self.change_y = 0
                
     
        # See if we are on the ground.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height


    #this function calculates the distance between the player and the rope
    def rope_distance(self):
        return math.sqrt((self.rect.y - self.rope_object.rect.y)**2 + (self.rect.x - self.rope_object.rect.x)**2)
        
 
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
            #if the player is attached to a rope this allows the player to up:
            if self.rope_object.ex == 'a':
                    #this sets self.change_y to 0 otherwise the player can launch themselves into space
                self.change_y = 0
                if self.walk_status == 'w':
                    self.change_y -= self.walk_jump
                #if the player is running
                if self.walk_status == 'r':
                    self.change_y -= self.run_jump
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



    #this function is for when the anchor is attached to a block.
    #this function currently will cause the player to swing back and forth
        #disables the left and right arrow keys from moving the player left & right
        #also allows the player to climb up and down the rope.
    def attached_rope(self):
        #this swings the player back and forth
        if self.rect.x < self.rope_object.rect.x:
            self.change_x += self.swing_speed
        else:
            self.change_x -= self.swing_speed
        self.swing_slow_down()


    #this function checks if the player passes the anchor
    #if the anchor is passed then the player will be slowed down
    def swing_slow_down(self):
        #if the player is swinging from the left to the right.
        if self.rect.x < self.rope_object.rect.x:
            if self.rect.x + self.change_x > self.rope_object.rect.x:
                self.change_x -= self.swing_speed_slowdown
        else:
            if self.rect.x + self.change_x < self.rope_object.rect.x:
                self.change_x += self.swing_speed_slowdown


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
                

    #this function is used to delayed te double jump for the player
    def double_jump_timer(self):
        self.end_time = time.clock()
        return self.end_time - self.jump_start_time


            
