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


def menu_button(x, y, screen, mouse, click, action, image1, image2):
    if x+190 > mouse[0] > x and y+50 > mouse[1] > y:
        screen.blit(image2, (x, y))
        if click[0] == 1:
            menu_action(action)
    else:
        screen.blit(image1, (x, y))
                     
#this function stores all the actions that a player can take on the menu screen
    #q   : Quit program
    #n_s : Next Song
    #p_s : previous Song
    #r   : return to game
    #MV_D: music volume down
    #MV_U: music volume up
def menu_action(action):
    #list of possible actions
    if action == 'q':
        pygame.quit()
        quit()
    if action == 'n_g':
        main.main()       

def End_Game_Screen():
    pygame.init()
    #The pause variable is used to keep the pause loop going.
    pause = True
    # this sets up the screen size for the user using the sizes defined in constants
    screen_size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(screen_size)

    pause = True

    #sets all the images up for the menu
    #quit game buttons
    quit1 = graphics.quit_button1
    quit2 = graphics.quit_button2

    #New game buttons
    new_game1 = graphics.new_game1
    new_game2 = graphics.new_game2

    #this loop is used to display the options of what to do for the player.
    while pause == True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.fill(BACKGOUND_COLOR)

        #loads the background Image
        screen.blit(graphics.background, (0,0))

        #loads the green background button
        screen.blit(graphics.congrat, (50,100))

        #press a to quit button
        screen.blit(graphics.game_credits, (650, 100))
        
        #adds the background image
        screen.blit(graphics.bar_button, (400,650))

        menu_button(410, 660, screen, mouse, click, 'n_g', new_game1, new_game2)

        menu_button(610, 660, screen, mouse, click, 'q', quit1, quit2)
        
        #this allows the player to exit the paused menu via the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pause= False



        pygame.display.update()

    #when the player presses a return to the main game
    main.main()
