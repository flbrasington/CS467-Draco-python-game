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
import graphics
from projectiles import SnowBall

#$$$$$$$$$$$$$$$$$$$$$$$
#$$$ MONSTER LIST    $$$
#$$$ ctrl-f to find  $$$
#$$$ GHOST - AAA1    $$$
#$$$ Snowman -BBB1   $$$
#$$$ SnowBall -CCC1  $$$
#$$$ Greensnake-DDD1 $$$
#$$$ Bluesnake-EEE1  $$$
#$$$ Yeti - FFF1     $$$
#$$$$$$$$$$$$$$$$$$$$$$$


class Enemy(pygame.sprite.Sprite):
    def __init__(self, walkingImages, attackingImages, attackDist, speedX, speedY, hp):
        super().__init__()

        self.attackingImages = attackingImages

        #this loads all the images for the snake
        #arrays for the left/right walk &
        #left/right attack
        self.walking_frames_left = []
        self.walking_frames_right = []
        self.attacking_frames_left = []
        self.attacking_frames_right = []

        if walkingImages != None:
            for img in walkingImages:
                image = pygame.image.load(img)
                self.walking_frames_right.append(image)
                image = pygame.transform.flip(image, True, False)
                self.walking_frames_left.append(image)

        if attackingImages != None:
            for img in attackingImages:
                image = pygame.image.load(img)
                self.attacking_frames_right.append(image)
                image = pygame.transform.flip(image, True, False)
                self.attacking_frames_left.append(image)


        #this loads the distance that the snake will detect the player
        #and begin to move around
        self.detection_distance = constants.DETECTION_DISTANCE

        #this varaible is used to have the snake attack the player.
        #if the player is closer than this distance the snake will attack
        self.attack_distance = attackDist

        #this sets the snake's speed
        self.speed_x = speedX
        self.speed_y = speedY
        self.change_x = 0
        self.change_y = 0

        #this sets the direction of the snake
        self.direction = 'r'

        #this sets the current frame for the animations
        self.frame = 0
        # number of steps that an enemy takes
        self.frameCount = 0

        #this loads all the sprites that the snake can bump into
        self.level = None

        #this sets the snake's image
        if walkingImages != None:
            self.image = self.walking_frames_right[self.frame]
        elif attackingImages != None:
            self.image = self.attacking_frames_right[self.frame]

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

        self.hp = hp

        self.total_snowballs = 0

    #this function updates the snakes' action
    def update(self, player=None):
        #if the player is within the detection distance then the snake will move around
        if self.hp <= 0:
            self.kill()
        if self.fall == 'y':
            self.calc_grav()
        if self.detect_player(player):
            if self.attack_range(player) and self.facingPlayer(player):
                self.attack()
            else:
                self.walk()

            self.rect.y += self.change_y
            self.fall = 'y'
            self.collision_blocks_y()
            self.rect.x += self.change_x

    def facingPlayer(self, player=None):
        # enemy is facing left
        if self.direction == 'l':
            # player is to the left of the enemy
            if player.rect.x <= self.rect.x:
                return True
            # player is to the right of the enemy
            else:
                return False
        # enemy is facing right
        else:
            # player is to the right of the enemy
            if player.rect.x >= self.rect.x:
                return True
            # player is to the left of the enemy
            else:
                return False


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
            # if player.rect.x < self.rect.x:
            #     self.direction = 'l'
            # else:
            #     self.direction = 'r'
            return True
        else:
            return False

    #this makes the snake attack
    def attack(self):
        # print("attack")
        # if not in attack mode, switch to attack mode
        if self.action != 'a':
            self.frame = 0
            self.action = 'a'

        self.move(self.attacking_frames_left, self.attacking_frames_right)

    def walk(self):
        #this switches the attacking to the moving
        if self.action != 'w':
            self.frame = 0
            self.action = 'w'

        self.move(self.walking_frames_left, self.walking_frames_right)

    #this moves the snake around
    def move(self, leftFrames, rightFrames):
        
        #moves the snake in the direction the snake is moving
        if self.direction == 'l':
            self.change_x = -self.speed_x
            self.frame = (self.frame + 1) % len(leftFrames)
            self.image = leftFrames[self.frame]
            if self.frame > len(leftFrames):
                self.frame = 0
        else:
            self.change_x = self.speed_x
            self.frame = (self.frame + 1) % len(rightFrames)
            self.image = rightFrames[self.frame]
            if self.frame > len(rightFrames):
                self.frame = 0
        # enemy has taken another step
        self.frameCount += 1

        #this checks to see if the snake has hit anything left/right
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            #if the snake is moving to the right
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.direction = 'l'
                self.rect.x -= 3
                # direction changed so reset frame counter
                self.frameCount = 0
            elif self.change_x < 0:
                self.rect.left = block.rect.right
                self.direction = 'r'
                self.rect.x += 3
                # direction changed so reset frame counter
                self.frameCount = 0

        # after 100 frames (steps) the enemy will change direction
        if self.frameCount >= 100:
            if self.direction == 'l':
                self.direction = 'r'
            else:
                self.direction = 'l'
            self.frameCount = 0
        '''
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
        '''

    def calc_grav(self):
        #if the player is not climbing the rope
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 0.35
            
    def collision_blocks_y(self):
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                # Stop our vertical movement
                self.change_y = 0
                self.fall = 'n'
                
    # this method is intended to deal one damage to an enemy if the player jumps on it
    # however, it only works for a small range of speeds for the player, so falling at
    # full speed does not kill the enemy, but switching from going up to going down,
    # does kill it
    # def detectCollision(self, player=None):
    #     if player.falling:
    #         if self.rect.top == player.rect.bottom:
    #             if self.rect.left <= player.rect.right and self.rect.right >= player.rect.left:
    #                 self.hp -= 1
    #     if self.hp > 0:
    #         return True
    #     else:
    #         return False

#this is for the ghost class of bad guy
#AA1
class ghost(Enemy):

    def __init__(self):
        Enemy.__init__(self, graphics.ghostWalk, None, 0, 3, 3, 10)


    #this function updates the ghost's actions
    def update(self, player=None):
        #if the player is within the detection distance then move the ghost
        #towards the player else the ghost sleeps
        if self.hp <= 0:
            self.kill()
        if self.detect_player(player) == True:
            self.looking_at_ghost(player)

    #this checks to see if the player is looking at the ghost
    def looking_at_ghost(self, player=None):
        #if the player is to the right of the ghost
        if player.rect.x > self.rect.x:
            if player.direction == 'r':
                self.frame = (self.frame + 1) % len(self.walking_frames_right)
                if self.frame > len(self.walking_frames_right):
                    self.frame = 0
                self.image = self.walking_frames_right[self.frame]
                self.move(player)
        else:
            if player.direction == 'l':
                self.frame = (self.frame + 1) % len(self.walking_frames_left)
                if self.frame > len(self.walking_frames_right):
                    self.frame = 0
                self.image = self.walking_frames_left[self.frame]
                self.move(player)

    #this function moves the ghost towards the player
    def move(self, player=None):
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
class SnowMan(Enemy):

    def __init__(self):
        #calls the parent's constructor
        Enemy.__init__(self, graphics.snowmanStand, graphics.snowmanAttack, 500, 0, 0, 10)

        self.time = time.clock()

        #these are timers for the throwing animation
        self.start_time = 0
        self.end_time = 0
        self.cool_down_time = 1
        self.timer = 0
        self.timer_limit = 2
        self.can_shoot = True

        #this variable is used to move the snowman down if needed
        self.move_snowman_down = 'y'

        #the throw variable is used to see if the snowman is able to throw a snowball
        self.can_shoot = 'y' #y is for yes the snowman can throw

        #this is a list that will store all the snow ball objects
        self.snowball_list = []
        self.current_snowball = 0
        self.num_of_snowballs = 0
        self.total_snowballs = 0

        self.snowballGroup = pygame.sprite.Group()

        for i in range(0,10):
            snowball_object = SnowBall()
            snowball_object.level = self.level
            self.snowballGroup.add(snowball_object)
            self.snowball_list.append(snowball_object)
            self.num_of_snowballs += 1
            self.total_snowballs += 1

    def walk(self):
        #this switches the attacking to the moving
        if self.action != 'w':
            self.frame = 0
            self.action = 'w'
        # if time.clock() >= self.time + 2:
        #     self.time = time.clock()
        #     if self.direction == '1':
        #         self.direction = 'r'
        #     else:
        #         self.direction = 'l'

        #moves the snake in the direction the snake is moving
        if self.direction == 'l':
            self.frame = (self.frame + 1) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[self.frame]
            # if self.frame > len(self.walking_frames_left):
            #     self.frame = 0
            # print("frame number ", self.frame)
            if self.frame == len(self.walking_frames_left) - 1:
                self.direction = 'r'
                self.frame = 0
                # print("switch l to r")
        else:
            self.frame = (self.frame + 1) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[self.frame]
            # if self.frame > len(self.walking_frames_right):
            #     self.frame = 0
            # print("frame number ", self.frame)
            if self.frame == len(self.walking_frames_left) - 1:
                self.direction = 'l'
                self.frame = 0
                # print("switch r to l")

    def attack(self):
        # print("attack")
        # if not in attack mode, switch to attack mode
        if self.action != 'a':
            self.frame = 0
            self.action = 'a'

        if self.direction == 'l':
            self.frame = (self.frame + 1) % len(self.attacking_frames_left)
            self.image = self.attacking_frames_left[self.frame]
            if self.frame > len(self.attacking_frames_left):
                self.frame = 0
            if self.frame == 3:
                self.throw_snowball(self)
        else:
            self.frame = (self.frame + 1) % len(self.attacking_frames_right)
            self.image = self.attacking_frames_right[self.frame]
            if self.frame > len(self.attacking_frames_right):
                self.frame = 0
            if self.frame == 3:
                self.throw_snowball(self)


    #this begins the snowman animation for throwing snowballs
    def throw_snowball(self, player=None):
        if self.can_shoot and self.num_of_snowballs > 0:
            if self.direction == 'r':
                self.snowball_list[self.current_snowball].throw_snowball(self.rect.centerx, self.rect.centery,
                                                                        int(self.rect.centerx)+self.attack_distance,
                                                                        self.rect.centery, self.playerGroup)
            elif self.direction == 'l':
                self.snowball_list[self.current_snowball].throw_snowball(self.rect.centerx, self.rect.centery,
                                                                        int(self.rect.centerx)-self.attack_distance,
                                                                        self.rect.centery, self.playerGroup)
            self.start_time = time.clock()
            self.current_snowball += 1
            self.num_of_snowballs -= 1
            self.can_shoot = False

            if self.current_snowball > self.total_snowballs - 1:
                self.current_snowball = 0
                self.num_of_snowballs -= 1
        else:
            self.can_shoot = self.check_cool_down()

    def check_cool_down(self):
        self.end_time = time.clock()
        if self.end_time - self.start_time > self.cool_down_time:
            return True
        else:
            return False

'''
This class is the yeti.
FFF1
'''
class Yeti(Enemy):
    def __init__(self):
        # for now the walking images and attacking images are the same
        Enemy.__init__(self, graphics.yetiWalk, graphics.yetiWalk, 100, 2, 0, 50)

#this is the code for the smiple green snake. The green snake moves left and right
#and will attack the player if the player gets too close
#DDD1
class green_snake(Enemy):

    def __init__(self):
        Enemy.__init__(self, graphics.greenSnakeWalk, graphics.greenSnakeAttack, 100, 2, 0, 1)

#this is the code for the smiple blue snake. The blue snake moves left and right
#and will attack the player if the player gets too close
#EEE1
class BlueSnake(Enemy):

    def __init__(self):
        Enemy.__init__(self, graphics.blueSnakeWalk, graphics.blueSnakeAttack, 100, 3, 0, 1)

class Trap(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        # spikes are always in attack mode
        self.action = 'a'
        
        self.image = image
        self.rect = self.image.get_rect()

        self.hp = 1000

        self.total_snowballs = 0


class Spikes(Trap):
    def __init__(self):
        Trap.__init__(self, graphics.TILEDICT['spikes'])

class Darts(Trap):
    def __init__(self, theme):
        if theme is 'dirt':
            image = graphics.TILEDICT['dirt dart']
        elif theme is 'castle':
            image = graphics.TILEDICT['castle dart']
        else:
            image = graphics.TILEDICT['ice block alt']
        Trap.__init__(self, image)

