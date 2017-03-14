"""
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file controls the game menu when the player presses the escape key

"""

import pygame
import music
import constants
import time
import graphics
import main
import Menu

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


#this object diplays the rect and text for a button
    #x and y are for the x & cooridnates
    #Screen is for the display of the game
    #Mouse is for the mouse cursor's current location
    #Click is for deteching a left mouse click
    #action is for the action to be taken in menu_action
    #music is for if music is being passed thru
def menu_button(x, y, screen, mouse, click, action, image1, image2):
    if x+190 > mouse[0] > x and y+50 > mouse[1] > y:
        screen.blit(image2, (x, y))
        if click[0] == 1:
            menu_action(action)
    else:
        screen.blit(image1, (x, y))
        return True
                     
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
        return True

    
def game_menu():
    pygame.init()
    #The pause variable is used to keep the pause loop going.
    pause = True
    # this sets up the screen size for the user using the sizes defined in constants
    screen_size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(screen_size)


    loop = True

    #sets all the images up for the menu
    #quit game buttons
    quit1 = graphics.quit_button1
    quit2 = graphics.quit_button2

    #New game buttons
    new_game1 = graphics.new_game1
    new_game2 = graphics.new_game2

    #Game_menu game button
    game_menu1 = graphics.game_menu1
    game_menu2 = graphics.game_menu2

    #background button
    bar_button = graphics.bar_button
    background_image = graphics.background_menu

    #game title
    title = graphics.game_display

    #this loop is used to display the options of what to do for the player.
    while loop == True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.fill(BACKGOUND_COLOR)

        #adds the background image
        screen.blit(background_image, (0,0))

        #Adds the title
        screen.blit(title, (175,25))

        #adds teh background button
        screen.blit(bar_button, (390, 550))

        #quit button
        print("mouse_y = ", mouse[1])
        if 400+190 > mouse[0] > 400 and 560 < mouse[1] < 560+50:
            screen.blit(new_game2, (400, 560))
            if click[0] == 1:
                loop = False
        else:
            screen.blit(new_game1, (400,560))
                
        if 610+190 > mouse[0] > 610 and 560 < mouse[1] < 560+50:
            screen.blit(quit2, (610, 560))
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            screen.blit(quit1, (610,560))

        
        #this allows the player to exit the paused menu via the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    loop = False



        pygame.display.update()
