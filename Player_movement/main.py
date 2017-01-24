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
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)

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
        level = [[constants.SCREEN_WIDTH-10, 100, 0, constants.SCREEN_HEIGHT - 10],
                 [100, 100, 100, constants.SCREEN_HEIGHT - 100],
                 [100, 100, 500, constants.SCREEN_HEIGHT - 300],
                 [constants.SCREEN_WIDTH, 100, 0, constants.SCREEN_HEIGHT]
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

    #this bit create's the level for the program5
    level_list = []
    level_list.append( Level_01(player))

    #set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]


    # List to hold all the sprites
    all_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 10
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height - 20
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(player)
    #active_sprite_list.add(player.rope_object)


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

        
        #this is for controlling the Frames per Second
        clock.tick(FPS)



main()
