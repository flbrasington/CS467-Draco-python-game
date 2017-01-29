"""
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file is used to generate a the game's music.

"""


import pygame



class Game_Music:

    def __init__(self):
        #this sets up all the music
        self.Song1 = "Swamp_Stomp.mp3"
        self.Song2 = "Eagle_Rock.mp3"
        self.Song3 = "Guts_and_Bourbon.mp3"
        self.Song4 = "Dirt_Road_Traveler.mp3"
        self.Song5 = "Uptown.mp3"

        #this is a list that stores all the songs for the game
        self.SongList = [self.Song1, self.Song2, self.Song3, self.Song4, self.Song5]

        #this variable stores which song is being used in the game
        #the variable stores the current location in the list
        self.current_song = 0

        #for pausing and unpausing
        self.pause = True

    def play_music(self):
        pygame.mixer.music.play(self.current_song)

    def next_song(self):
        pygame.mixer.music.stop()
        if self.current_song < 3:
            self.current_song += 1
        else:
            self.current_song = 0
        pygame.mixer.music.load(self.SongList[self.current_song])
        self.play_music()

    def prev_song(self):
        pygame.mixer.music.stop()
        if self.current_song > 0:
            self.current_song -= 1
        else:
            self.current_song = 3
        pygame.mixer.music.load(self.SongList[self.current_song])
        self.play_music()

    def load_music(self):
        pygame.mixer.music.load(self.SongList[self.current_song])

    #This function controlles the music for the game based on input from the keyboard
    def up_date_music(self):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.next_song()        #if the Y key is pressed then it plays the next song
                if event.key == pygame.K_t:
                    self.prev_song()        #if the T key is pressed then it loads the previous song

    def pause_music(self):
        pygame.mixer.music.pause()

    def unpause_music(self):
        pygame.mixer.music.unpause()
