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
def menu_button(x, y, screen, mouse, click, action, image1, image2, music=None):
    if x+190 > mouse[0] > x and y+50 > mouse[1] > y:
        screen.blit(image2, (x, y))
        if click[0] == 1:
            menu_action(action,music)
    else:
        screen.blit(image1, (x, y))
                     
#this function stores all the actions that a player can take on the menu screen
    #q   : Quit program
    #n_s : Next Song
    #p_s : previous Song
    #r   : return to game
    #MV_D: music volume down
    #MV_U: music volume up
def menu_action(action, music=None):
    #list of possible actions
    if action == 'q':
        pygame.quit()
        quit()
    if action == 'n_s':
        time.sleep(.25)
        music.next_song()
    if action == 'p_s':
        time.sleep(.25)
        music.prev_song()
    if action == 'r':
        music.pause = False
    if action == 'MV_D':
        music.music_volume_down()
    if action == 'MV_U':
        music.music_volume_up()
        

def game_menu(gamemusic):
    pygame.init()
    #The pause variable is used to keep the pause loop going.
    pause = True
    # this sets up the screen size for the user using the sizes defined in constants
    screen_size = [constants.SCREEN_WIDTH + constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT + constants.SCREEN_HEIGHT//2]
    screen = pygame.display.set_mode(screen_size)

    gamemusic.pause = True

    #sets all the images up for the menu
    #quit game buttons
    quit1 = graphics.quit_button1
    quit2 = graphics.quit_button2

    #next song
    next1 = graphics.next_song1
    next2 = graphics.next_song2

    #previous song
    prev1 = graphics.prev_song1
    prev2 = graphics.prev_song2

    #music volume
    music_up1 = graphics.music_up1
    music_up2 = graphics.music_up2
    music_down1 = graphics.music_down1
    music_down2 = graphics.music_down2

    #return to game
    return1 = graphics.return1
    return2 = graphics.return2

    #background button
    button_back = graphics.button_back
    background_image = graphics.background_menu

    #this loop is used to display the options of what to do for the player.
    while gamemusic.pause == True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.fill(BACKGOUND_COLOR)

        #adds the background image
        screen.blit(background_image, (0,0))

        #adds teh background button
        screen.blit(button_back, (50, 50))

        #quit button
        menu_button(100, 100, screen, mouse, click, 'q',quit1, quit2)
        #next song
        menu_button(100, 175, screen, mouse, click, 'n_s', next1, next2, gamemusic)
        #Music volume up
        menu_button(100, 250, screen, mouse, click, 'MV_U', music_up1, music_up2, gamemusic)
        #prev song
        menu_button(300, 100, screen, mouse, click, 'p_s', prev1, prev2, gamemusic)
        #return to game
        menu_button(300, 175, screen, mouse, click, 'r', return1, return2, gamemusic)
        #Music volume down
        menu_button(300, 250, screen, mouse, click, 'MV_D', music_down1, music_down2, gamemusic)


        
        #this allows the player to exit the paused menu via the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pause= False



        pygame.display.update()
