"""
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file is for displaying the GameOver Screen

"""

import pygame
import constants
import graphics
import main

WHITE = constants.WHITE
BLUE = constants.BLUE
BLACK = constants.BLACK
NAVY = constants.NAVY
BACKGOUND_COLOR = constants.DARK_YELLOW

# set height and width of window
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT

#sets the button's width and height
width = constants.BUTTON_WIDTH
height = constants.BUTTON_HEIGHT

        

def Game_Over_Screen():
    pygame.init()
    #The pause variable is used to keep the pause loop going.
    pause = True
    # this sets up the screen size for the user using the sizes defined in constants
    screen_size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(screen_size)

    pause = True

    #this loop is used to display the options of what to do for the player.
    while pause == True:

        #loads the background Image
        screen.blit(graphics.background, (0,0))

        #loads the green background button
        screen.blit(graphics.button_back, (750,150))

        #press a to quit button
        screen.blit(graphics.press_a, (770, 170))
        
        #adds the background image
        screen.blit(graphics.game_over, (200,200))

        screen.blit(graphics.spelunkyGuyGhost, (900, 400))
        
        #this allows the player to exit the paused menu via the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pause= False



        pygame.display.update()

    #when the player presses a return to the main game
    main.main()
