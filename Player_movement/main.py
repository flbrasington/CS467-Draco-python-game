'''
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file stores the main program of the game. Here is where the function will run
and the program will begin.

'''

import pygame
import constants
from player import Player

#defines the frames persecond
FPS = constants.fps

#this is a list of items for the sandbox level.. This will have objects for the player to jump
#on hit and move around for testing.

#this class stores the level
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    world_shift_x = 0
    world_shift_y = 0
    level_limit = -1000

 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(constants.WHITE)
        #screen.blit(self.background,(self.world_shift // 3,0))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

    def shift_world_x(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift_x += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

    def shift_world_y(self, shift_y):
        #keep track of the shift amount
        self.world_shift_y += shift_y

        #go through all the aprite lists ans shift
        for platform in self.platform_list:
            platform.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.y += shift_y

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(constants.GREEN)
 
        self.rect = self.image.get_rect()
        
#this creates the testing level for game play testing
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
 
        # Array with width, height, x, and y of platform
        level = [[constants.SCREEN_WIDTH-10, 11, 0, constants.SCREEN_HEIGHT - 10],
                 [210, 70, 200, 500],
                 [210, 70, 600, 400],
                 [constants.SCREEN_WIDTH, 1, 0, constants.SCREEN_HEIGHT]
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


            

#Function Main
def main():
    #this initizates pygame
    pygame.init()

    #this sets up the screen size for the user using the sizes defined in constants
    screen_size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode (screen_size)

    #this is the caption for the window
    pygame.display.set_caption("Climbing Game")

    #this time function is used to manage the frames per second
    clock = pygame.time.Clock()

    #this bit of code sets up the players for the game
    player = Player()

    #this bit create's the level for the program
    level_list = []
    level_list.append( Level_01(player))

    #set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]


    # List to hold all the sprites
    all_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 300
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 20
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)


    #this is the heart of the main program.
    #currently the program runs on a loop until the python sheet is closed.
    done = False
    while not done:
        #this updates the the display
        screen.fill(constants.WHITE)
        current_level.draw(screen)
        active_sprite_list.update()
        active_sprite_list.draw(screen)
        #player.update()
        #pygame.draw.rect(screen, constants.BLACK, [player.lead_x, player.lead_y, 10,10])

        pygame.display.update()

        #this shifts the camera for the world
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world_x(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 100:
            diff = 120 - player.rect.x
            player.rect.x = 100
            current_level.shift_world_x(diff)

        #if the player gets near the top of the screen
        if player.rect.y <= constants.SCREEN_HEIGHT/4:
            diff = player.rect.y - constants.SCREEN_HEIGHT/4
            player.rect.y = constants.SCREEN_HEIGHT/4
            current_level.shift_world_y(-diff)

        #if the player gets near the bottom of the screen
        if player.rect.y >= constants.SCREEN_HEIGHT*3/4:
            diff = constants.SCREEN_HEIGHT*3/4 - player.rect.y
            player.rect.y = constants.SCREEN_HEIGHT*3/4
            current_level.shift_world_y(diff)

        
        #this is for controlling the Frames per Second
        clock.tick(FPS)



main()
