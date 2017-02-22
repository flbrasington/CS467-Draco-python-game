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

WHITE = constants.WHITE
BLUE = constants.BLUE
BLACK = constants.BLACK
NAVY = constants.NAVY

# set height and width of window
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT

#sets the button's width and height
width = constants.BUTTON_WIDTH
height = constants.BUTTON_HEIGHT

#for the font
myFont = constants.MENU_FONT


#this object diplays the rect and text for a button
    #Text is for the desired text to be displayed
    #x and y are for the x & cooridnates
    #Screen is for the display of the game
    #Mouse is for the mouse cursor's current location
    #Click is for deteching a left mouse click
    #action is for the action to be taken in menu_action
    #music is for if music is being passed thru
def text_objects(text, font, x, y, screen, mouse, click, action, music=None):
    pygame.draw.rect(screen, NAVY, (x, y, width,height))

    #this changes the color of the button if the mouse is over the button
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(screen, BLUE, (x,y,width,height))
        if click[0] == 1:
            menu_action(action,music)

    label = font.render(text, 1, WHITE)
    screen.blit(label, (x+5,y+height/3))
                     
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
    screen_size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(screen_size)

    gamemusic.pause = True

    #this loop is used to display the options of what to do for the player.
    while gamemusic.pause == True:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        screen.fill(constants.ORANGE)

        #this displays the quit game button
        text_objects("Quit Game", myFont, 150, 450, screen, mouse, click, 'q')

        #This displays the next song button
        text_objects("Next Song", myFont, 150, 550, screen, mouse, click, 'n_s', gamemusic)

        #displays the prev song button
        text_objects("Prev Song", myFont, 150, 650, screen, mouse, click, 'p_s', gamemusic)

        #this is for returning to the game
        text_objects("Return to Game", myFont, 450, 450, screen, mouse, click, 'r', gamemusic)

        #this sets the music volume up
        text_objects("Music Volume++", myFont, 450, 550, screen, mouse, click, 'MV_U', gamemusic)

        #this sets the music volume down
        text_objects("Music Volume--", myFont, 450, 650, screen, mouse, click, 'MV_D', gamemusic)


        
        #this allows the player to exit the paused menu via the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pause= False



        pygame.display.update()
