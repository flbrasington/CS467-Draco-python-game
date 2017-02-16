"""
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file contains all the code needed for the enemies in the game.
"""

import pygame
import constants
import sound_effects
import math
import time

#$$$$$$$$$$$$$$$$$$$$$$$
#$$$ MONSTER LIST    $$$
#$$$ ctrl-f to find  $$$
#$$$ GHOST - AAA1    $$$
#$$$ Snowman -BBB1   $$$
#$$$ SnowBall -CCC1  $$$
#$$$ Greensnake-DDD1 $$$
#$$$ Bluesnake-EEE1  $$$
#$$$$$$$$$$$$$$$$$$$$$$$

#this is for the ghost class of bad guy
#AA1
class ghost(pygame.sprite.Sprite):

    def __init__(self):
        #calls the parent's constructor
        super().__init__()

        #self.ghost_color = constants.RED
        #self.image = pygame.Surface([width, height])
        #self.image.fill(self.ghost_color)

        #this is the distance that the 'ghost will detect the player
        #when the player gets with in this distance the ghost will attack
        self.detection_distance = constants.DETECTION_DISTANCE

        #this is the speed the ghost will move towards the player
        self.speed_x = 3
        self.speed_y = 3

        #this sets the direction of the ghost
        self.direction = 'r'

        #this is for loading the ghost's images
        self.moving_frames_right = []
        self.moving_frames_left = []

        self.frame = 0

        #List all the sprites incase the enemy bumps into it
        self.level = None

        image = pygame.image.load("Graphics/ghost/ghost_walk1.png")
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)
        
        image = pygame.image.load("Graphics/ghost/ghost_walk2.png")
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)

        image = pygame.image.load("Graphics/ghost/ghost_walk3.png")
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)

        image = pygame.image.load("Graphics/ghost/ghost_walk4.png")
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)

        image = pygame.image.load("Graphics/ghost/ghost_walk3.png")
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)

        image = pygame.image.load("Graphics/ghost/ghost_walk2.png")
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        self.moving_frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)
        self.moving_frames_left.append(image)

        self.image = self.moving_frames_right[0]

        #this gets the ghost's rect
        self.rect = self.image.get_rect()


    #this function updates the ghost's actions
    def update(self, player=None):
        #if the player is within the detection distance then move the ghost
        #towards the player else the ghost sleeps
        if self.detect_player(player) == True:
            self.looking_at_ghost(player)

    #this checks to see if the ghost is within the ghost's dectection range
    def detect_player(self, player=None):
        #calculates the distance to the player
        distance = abs((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)
        distance = math.sqrt(distance)
        #if the player is within the detection distance return true
        if distance < self.detection_distance:
            return True
        else:
            return False

    #this checks to see if the player is looking at the ghost
    def looking_at_ghost(self, player=None):
        #if the player is to the right of the ghost
        if player.rect.x > self.rect.x:
            if player.direction == 'r':
                self.frame = (self.frame + 1) % len(self.moving_frames_right)
                if self.frame > len(self.moving_frames_right):
                    self.frame = 0
                self.image = self.moving_frames_right[self.frame]
                self.move_towards_player(player)
        else:
            if player.direction == 'l':
                self.frame = (self.frame + 1) % len(self.moving_frames_left)
                if self.frame > len(self.moving_frames_right):
                    self.frame = 0
                self.image = self.moving_frames_left[self.frame]
                self.move_towards_player(player)

    #this function moves the ghost towards the player
    def move_towards_player(self, player=None):
        #checks the player's x position in relationship to the ghost's
        if player.rect.x > self.rect.x:
            self.rect.x += self.speed_x
        else:
            self.rect.x -= self.speed_x

        #checks the player's y position in relationship to the ghost's
        if player.rect.y > self.rect.y:
            self.rect.y += self.speed_y
        else:
            self.rect.y -= self.speed_y



#This is for the snowman bad guy
#BB1
class SnowMan(pygame.sprite.Sprite):

    def __init__(self):
        #calls the parent's constructor
        super().__init__()

        #this is the distance that the snow man will detect the play and start throwing
        #snow balls
        self.detection_distance = constants.DETECTION_DISTANCE

        #this sets the direction of the ghost
        self.direction = 'r'

        #this is for loading the ghost's images
        self.frames_right = []
        self.frames_left = []

        image = pygame.image.load("Graphics/snowman/snowman1.png")
        self.frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_left.append(image)
        
        image = pygame.image.load("Graphics/snowman/snowman2.png")
        self.frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_left.append(image)

        image = pygame.image.load("Graphics/snowman/snowman3.png")
        self.frames_right.append(image)
        image = pygame.transform.flip(image, True, False)
        self.frames_left.append(image)
        
        self.frame = 0

        self.image = self.frames_right[0]

        #this get's the rect for the snowman image
        self.rect = self.image.get_rect()

        #this sets the direction of the snowman
        self.direction = 'r'

        #this is for the change of movement vertical
        self.change_y = 0

        #these are timers for the throwing animation
        self.timer_start = 0
        self.timer = 0
        self.timer_limit = 2

        #this variable is used to move the snowman down if needed
        self.move_snowman_down = 'y'

        #the throw variable is used to see if the snowman is able to throw a snowball
        self.throw = 'y' #y is for yes the snowman can throw

        #this is a list that will store all the snow ball objects
        self.snowball_list = []

    #this is the update function for the snowman
        #this function updates the ghost's actions
    def update(self, player=None):
        #if the player is within the detection distance
        #then start the snowball throwing animation
        if self.detect_player(player) == True:
            self.throw_snowball(player)

            #this checks if the snowman needs to be shifted down
            if self.move_snowman_down == 'y':
                
                #moves the snowman down if needed
                self.rect.y += self.change_y

                #this moves the snowman down in the event there is nothing under the snowman
                block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                for block in block_hit_list:
                    #resets the position of the snowman based on the top/bottom of the object
                    self.move_snowman_down = 'n'
                    if self.change_y > 0:
                        self.rect.bottom = block.rect.top
                    elif self.change_y < 0:
                        self.rect.top = block.rect.bottom

                #this calculates the gravity if needed
                self.calc_grav()

        #this bit of code handles all the snowballs being thrown by the snowman
        for ball in self.snowball_list:
            if ball.upgrade == 'd':
                self.snowball_list.remove(ball)
                
                


    #this checks to see if the player is within the snowman's dectection range
    def detect_player(self, player=None):
        #calculates the distance to the player
        distance = abs((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)
        distance = math.sqrt(distance)
        #if the player is within the detection distance return true
        if distance < self.detection_distance + 300:
            return True
        else:
            return False

    #calcualtes the effect of the gravity
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

    #this begins the snowman animation for throwing snowballs
    def throw_snowball(self, player=None):
        self.set_direction(player)
        self.throw_animation(self)

    #this cycles thru the snowman's throwing animations
    def throw_animation(self, player=None):
        if self.timer == 0:
            self.timer_start = time.clock()
            self.timer = 1
        else:
            if self.animation_timer() > self.timer_limit:
                self.timer = 0
                self.timer_start = 0
                if self.frame >= 2:
                    self.frame = 0
                    self.throw = 'y' #resets the conditions that allow the snowman to throw a snowball
                else:
                    self.frame += 1
            else:
                self.timer = time.clock()

    #this function will create a snowball if the conditions apply
        #Conditions to throw
        #snowman is able to throw and is on the proper frame
    def make_snow_ball(self, player=None):
        #checks for the conditions
        if self.frame == 2 and self.throw == 'y':
            sb = enemies.SnowBall()
            sb.set_starting_location(self.rect.x+2, self.rect.y+2)
            sb.set_up_platforms(self.level)
            #if the snowman is facing to the right
            if self.direction == 'r':
                sb.set_speed(5,0)
            else:
                sb.set_speed(-5,0)

            #adds the snowball to the list of snowball objects
            self.snowball_list.add(sb)
            self.throw = 'n'

    #this function is used for the delay between animations
    def animation_timer(self):
        self.timer = time.clock()
        return self.timer - self.timer_start

    #this sets the direction for the snowman
    def set_direction(self, player=None):
        if self.rect.x > player.rect.x:
            self.direction = 'l'
            self.image = self.frames_left[self.frame]
        else:
            self.direction = 'r'
            self.image = self.frames_right[self.frame]


#this is for the snowball which can be thrown by a snowman or possiblely other objects
#CCC1
class SnowBall(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        # this sets up the screen size for the user using the sizes defined in constants
        screen_size = [constants.SCREEN_WIDTH + constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT + constants.SCREEN_HEIGHT//2]
        screen = pygame.display.set_mode(screen_size)

        #this sets the speed for the snowball
        self.speed_x = 0
        self.speed_y = 0

        #this sets up the image to be used for the snowball
        image = pygame.image.load("Graphics/snowman/snowball.png")

        #this gets the snowball's image
        self.rect = self.image.get_rect()

        self.level = None

        self.delete = 'n'

    #this is the update for the snowball
    def update(self):
        print("print")
        #this moves the snowball
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        #this draws the snowball
        self.image.draw(screen)

        #this checks to see if the snowball has hit any of the objects in the game
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            #if the snowball hits a platfrom then the update is to return delete so that the
            #snowball object will be removed
            # set our right side to the left side of the item we hit
            if self.speed_x > 0:
                self.rect.right = block.rect.left
            elif self.speed_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

    #this sets up the speed for the snowball
    def set_speed(self, speedx, speedy):
        self.speed_x = speedx
        self.speed_y = speedy

    #this sets up the starting location for the snowball
    def set_starting_location(self, start_x, start_y):
        self.rect.x = start_x
        self.rect.y = start_y

    #this adds all the platforms to the snowball object
    def set_up_platfroms(self, objects):
        self.level = objects

        
#this is the code for the smiple green snake. The green snake moves left and right
#and will attack the player if the player gets too close
#EEE1
class green_snake(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        #this loads all the images for the snake
        #arrays for the left/right walk &
        #left/right attack
        self.walking_frames_left = []
        self.walking_frames_right = []
        self.attacking_frames_left = []
        self.attacking_frames_right = []

        #loads the walking frames
        for i in range(1,12):
            filename = 'Graphics/Snake/Snake_walk_' + str(i) + '.png'
            image = pygame.image.load(filename)
            for j in range(1,5):
                self.walking_frames_right.append(image)
            image = pygame.transform.flip(image, True, False)
            for k in range(1,5):
                self.walking_frames_left.append(image)

        #loads the attack frames
        for i in range(1,9):
            filename = 'Graphics/Snake/Snake_attack_' + str(i) + '.png'
            image = pygame.image.load(filename)
            for j in range(1,5):
                self.attacking_frames_right.append(image)
            image = pygame.transform.flip(image, True, False)
            for k in range(1,5):
                self.attacking_frames_left.append(image)

        #this loads the distance that the snake will detect the player
        #and begin to move around
        self.detection_distance = constants.DETECTION_DISTANCE

        #this varaible is used to have the snake attack the player.
        #if the player is closer than this distance the snake will attack
        self.attack_distance = 100

        #this sets the snake's speed
        self.speed_x = 2
        self.change_x = 0
        self.change_y = 0

        #this sets the direction of the snake
        self.direction = 'r'

        #this sets the current frame for the animations
        self.frame = 0

        #this loads all the sprites that the snake can bump into
        self.level = None

        #this sets the snake's image
        self.image = self.walking_frames_right[self.frame]

        #this get's the snakes' rect
        self.rect = self.image.get_rect()

        #this stores if the snake is attacking or 'walking'
            #w: walking
            #a: attacking
        self.action = 'w'

        #this is used to see if the snake needs to fall.
        #the snake shouldn't fall. The snake should move left/right
        #if there is no platform under te snake the snake should turn around
        #this variable is used in the move function
            #y: TURN AROUND
            #n: DON'T TURN AROUND
        self.turn_around = 'y'

        #this sets the snake to fall if needed
        self.fall = 'y'

    #this function updates the snakes' action
    def update(self, player=None):
        #if the player is within the detection distance then the snake will move around
        if self.detect_player(player) == True:
            if self.attack_range(player) == True:
                self.attack()
            else:
                self.move()

        self.rect.x += self.change_x
        if self.fall == 'y':
            self.rect.y += self.change_y

    #this checks if the player is within the snake's detection range
    def detect_player(self, player=None):
        #calculates the distance to the player
        distance = abs((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)
        distance = math.sqrt(distance)
        #if the player is within the detection distance return true
        if distance < self.detection_distance:
            return True
        else:
            return False

    #this checks if the player is within the snake's attack range
    def attack_range(self, player=None):
        #calculates the distance to the player
        distance = abs((player.rect.x - self.rect.x)**2 + (player.rect.y - self.rect.y)**2)
        distance = math.sqrt(distance)
        #if the player is within the detection distance return true
        if distance < self.attack_distance:
            if player.rect.x < self.rect.x:
                self.direction = 'l'
            else:
                self.direction = 'r'
            return True
        else:
            return False

    #this makes the snake attack
    def attack(self):
        print("attack")

    #this moves the snake around
    def move(self):
        #this switches the attacking to the moving
        if self.action != 'w':
            self.frame = 0
            self.action = 'w'
        #moves the snake in the direction the snake is moving
        if self.direction == 'l':
            self.change_x = -self.speed_x
            self.frame = (self.frame + 1) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[self.frame]
            if self.frame > len(self.walking_frames_left):
                self.frame = 0
        else:
            self.change_x = self.speed_x
            self.frame = (self.frame + 1) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[self.frame]
            if self.frame > len(self.walking_frames_right):
                self.frame = 0

        #this checks to see if the snake has hit anything left/right
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            #if the snake is moving to the right
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.direction = 'l'
                self.rect.x -= 3
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.direction = 'r'
                self.rect.x += 3

        """
        #this checks to see if the snake needs to turn around because of the platform
        self.turn_around = 'y'
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            self.turn_around = 'n'
            #resets the position based on the top/bottom of the object
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.fall = 'n'
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            #stops the vertical movement
            self.change_y = 0
        
        #turns the snake around is needed
        if self.turn_around == 'y':
            if self.direction == 'l':
                self.direction = 'r'
                self.change_x = self.speed_x
            else:
                self.direction = 'l'
                self.change_x = -self.speed_x

            self.rect.x += self.change_x
        
        #shifts the snake down if needed
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        """ 
        

        

        
        
        
        
        
            
    

        
    

        

        
























        
        
