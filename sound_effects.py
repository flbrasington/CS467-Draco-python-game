"""
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file contains all the code and infomation required
for the game's sound effects.

"""

import pygame

class Player_Sound_Effects:

    def __init__(self):
        pygame.init()
        #this sets up the sound effects for the game
        self.p_running = "SoundEffects/Jog_On_Grit.wav"
        self.p_walking = pygame.mixer.Sound("SoundEffects/Walking_on_Grit.wav")

        #The following is for setting up the channels for the sound effects
        #Default is 8 so I put in an 8. Subject to change
            #Channel 0 is empty
            #Channel 1 is for player's movement sounds
            #Channel 2 is for enemies
            #Channel 3 is for enviromental sounds
            #Channel 4 is for the player's equipment/tools
        numChannels = pygame.mixer.set_num_channels(8)


    #Plays the walking sound for the game
    def player_walking_sound(self):
        walking = pygame.mixer.Sound(self.p_walking)
        walking.set_volume(0.5)
        walking.play(loops = -1, maxtime = 300)

    #sets up the player's run sound
    def player_running_sound(self):
        running = pygame.mixer.Sound(self.p_running)
        running.set_volume(0.5)
        running.play(loops = -1, maxtime = 300)


    #this stops the player's sound effects
    def player_sounds_stop(self):
        #set's the sound to the player's sound effect
        #self.channel = pygame.mixer.Channel(1)
        #stops the sound Effect
        pygame.mixer.Channel(1).stop()
        
        

    
        
