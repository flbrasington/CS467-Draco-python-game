"""
Course: CS 462 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file is used to generate a level's path.
A level's path is a path that any player regardless of items should be able to complete if objects don't
kill or stop the player first.

"""

import pygame
import random
import constants
import player
import music
import sound_effects
import Menu
import Level
import enemies
import graphics
from projectiles import Knife, SnowBall
from rope import Rope

FPS = constants.fps

random.seed()

WHITE = constants.WHITE
BLUE = constants.BLUE
BLACK = constants.BLACK

# set height and width of window
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT


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

def game_menu():

    # The pause variable is used to keep the pause loop going.
    pause = True

    # this loop is used to display the options of what to do for the player.
    while pause == True:
        screen_size = [constants.SCREEN_WIDTH + constants.SCREEN_WIDTH // 2,
                       constants.SCREEN_HEIGHT + constants.SCREEN_HEIGHT // 2]
        screen = pygame.display.set_mode(screen_size)
        screen.fill(constants.BLUE)

        # this allows the player to exit the paused menu via the keyboard
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    pause = False

def generateEnemies(levelNum):
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #$$$ This is for testing for enemies $$$
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #$$$ This sets up all the enemies in a list $$$
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    enemy_sprite_list = pygame.sprite.Group()

    #$$$$$$$$$$$$$$$$$$$$$
    #$$$ GHOST TESTING $$$
    #$$$$$$$$$$$$$$$$$$$$$
    
    # ghosts can be in any level at the moment
    g1 = enemies.ghost()
    g2 = enemies.ghost()
    # g1.rect.x = 300
    g1.rect.x = random.randint(0, constants.SCREEN_WIDTH * 2)
    # g1.rect.y = 300
    g1.rect.y = random.randint(0, constants.SCREEN_HEIGHT * 2)
    # g2.rect.x = 500
    g2.rect.x = random.randint(0, constants.SCREEN_WIDTH * 2)
    # g2.rect.y = 500
    g2.rect.y = random.randint(0, constants.SCREEN_HEIGHT * 2)
    # print('g1 ' + str(g1.rect.x) + ' ' + str(g1.rect.y))
    # print('g2 ' + str(g2.rect.x) + ' ' + str(g2.rect.y))

    enemy_sprite_list.add(g1)
    enemy_sprite_list.add(g2)
    
    #$$$$$$$$$$$$$$$$$$$$$$$$
    #$$$ Snow Man Testing $$$
    #$$$$$$$$$$$$$$$$$$$$$$$$

    # snowman can only be in ice level
    # sm1 = enemies.SnowMan()
    # sm1.rect.x = 400
    # sm1.rect.y = 100
    # sm1.rect.x = random.randint(0, constants.SCREEN_WIDTH * 2)
    # sm1.rect.y = random.randint(0, constants.SCREEN_HEIGHT * 2)
    # print('sm1 ' + str(sm1.rect.x) + ' ' + str(sm1.rect.y))
    # enemy_sprite_list.add(sm1)


    #$$$$$$$$$$$$$$$$$$$$$$$$
    #$$$ Yeti Testing $$$
    #$$$$$$$$$$$$$$$$$$$$$$$$

    # yeti can only be in ice level
    if levelNum == 2:
        y1 = enemies.Yeti()
        y1.rect.x = random.randint(0, constants.SCREEN_WIDTH * 2)
        y1.rect.y = random.randint(0, constants.SCREEN_HEIGHT * 2)
        # print('y1 ' + str(y1.rect.x) + ' ' + str(y1.rect.y))
        enemy_sprite_list.add(y1)


    #$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #$$$ Green Snake Testing $$$
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # green snake can only be in dirt level
    if levelNum == 1:
        s1 = enemies.green_snake()
        # s1.rect.x = p.rect.x
        # s1.rect.y = p.rect.y
        s1.rect.x = random.randint(0, constants.SCREEN_WIDTH * 2)
        s1.rect.y = random.randint(0, constants.SCREEN_HEIGHT * 2)
        # print('s1 ' + str(s1.rect.x) + ' ' + str(s1.rect.y))
        enemy_sprite_list.add(s1)

    #$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #$$$ Blue Snake Testing $$$
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # blue snake can only be in ice level
    if levelNum == 2:
        bs1 = enemies.BlueSnake()
        # s1.rect.x = p.rect.x
        # s1.rect.y = p.rect.y
        bs1.rect.x = random.randint(0, constants.SCREEN_WIDTH * 2)
        bs1.rect.y = random.randint(0, constants.SCREEN_HEIGHT * 2)
        # print('bs1 ' + str(bs1.rect.x) + ' ' + str(bs1.rect.y))
        enemy_sprite_list.add(bs1)

    #adds the platforms to the enemies
    # for i in enemy_sprite_list:
    #     i.level = current_level
    return enemy_sprite_list
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    #$$$ This is for testing for enemies $$$
    #$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

def detectCollision(player, enemy):
    enemy.detectCollision(player)
    # bottomLeft = rect.collidepoint()

# Function Main
def main():
    # this initializes pygame
    pygame.init()

    # this sets up the screen size for the user using the sizes defined in constants
    screen_width = constants.SCREEN_WIDTH
    screen_height = constants.SCREEN_HEIGHT
    screen_size = [screen_width, screen_height]
    screen = pygame.display.set_mode(screen_size)

    # this is the caption for the window
    pygame.display.set_caption("Climbing Game")

    # this time function is used to manage the frames per second
    clock = pygame.time.Clock()

    # this bit of code sets up the players for the game
    p = player.Player() 
    playerGroup = pygame.sprite.Group()
    playerGroup.add(p)   

    #this loads all the music & music function for the game
    gamemusic = music.Game_Music()


    # this bit create's the level for the program
    level_list = []
    # level_list.append(Level.Level(5, 5, constants.SCREEN_WIDTH * 5, constants.SCREEN_HEIGHT * 5, p))
    # level_list.append(Level.Level(5, 5, constants.SCREEN_WIDTH * 5, constants.SCREEN_HEIGHT * 5, p))
    maxLevels = 9

    # set the current level
    # current_level_no = 0
    current_level_no = 6
    # current_level = level_list[current_level_no]
    current_level = Level.snow_level(5, 5, constants.SCREEN_WIDTH * 5, constants.SCREEN_HEIGHT * 5, p, 1)

    # List to hold all the sprites
    p.level = current_level
    p.rect.x = current_level.entrance_coords['x']
    p.rect.y = current_level.entrance_coords['y']

    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(p)
    for rope in p.rope_list:
        active_sprite_list.add(rope)
        for segment in rope.rope_segments:
            active_sprite_list.add(segment)

    for knife in p.knife_list:
        active_sprite_list.add(knife)

    #adds the whip
        active_sprite_list.add(p.whip)

    #adds the player's health bar
    active_sprite_list.add(p.health)


    # enemy_sprite_list = generateEnemies(current_level_no)
    enemy_sprite_list = current_level.enemy_list
    enemy_sprite_list.add(generateEnemies(current_level_no))
    active_sprite_list.add(enemy_sprite_list)
    for enemy in enemy_sprite_list:
        enemy.playerGroup = playerGroup
        if enemy.total_snowballs > 0:
            active_sprite_list.add(enemy.snowballGroup)

    #adds the enemies to the player list
    p.enemies = enemy_sprite_list

    for sprite in active_sprite_list:
        sprite.level = current_level

    # this is the heart of the main program.
    # currently the program runs on a loop until the python sheet is closed.
    done = False

    #this plays the music for the game
    gamemusic.load_music()
    #this sets the music for the game
    gamemusic.music_volume_up()
    #this plays the music
    gamemusic.play_music()
    # print('sprites')
    # for s in active_sprite_list:
    #     print(s)


    #adds the images for the number of ropes the player has
    ropeCounter = []
    for img in graphics.ropeCounter:
        # print(img)
        image = pygame.image.load(img)
        ropeCounter.append(image)

    #adds the images for the number of knives the player has
    knifeCounter = []
    for img in graphics.knifeCounter:
        # print(img)
        image = pygame.image.load(img)
        knifeCounter.append(image)


    #adds the selection box image
    selection_box = graphics.selection_box

    #adds the whip image for the item selection
    whip_item = graphics.whip_large

    while not done:


        #this updates the music based on player's input
        #gamemusic.up_date_music()

        #this controls everything for the user's input for menus and quiting
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            Menu.game_menu(gamemusic)
        
        # for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        done = True
        # this updates the the display
        screen.fill(constants.WHITE)
        current_level.draw(screen)
        active_sprite_list.update(p)

        # If the player gets near the right side, shift the world left (-x)

        if p.rect.right >= 800 and p.level.edge_sprites[1].rect.right > screen_width:
            diff = p.rect.right - 800
            p.rect.right = 800
            current_level.shift_world_x(-diff)

            #this shifts all the rope objects as needed
            for rope in p.rope_list:
                rope.rect.x -= diff
                for segment in rope.rope_segments:
                    segment.rect.x -= diff

            #updates all the knife objects as needed
            for knife in p.knife_list:
                knife.rect.x -= diff

            #The enemies are being spawned in the level class so the shifting is done in that class as well
            #for enemy in enemy_sprite_list:
            #    enemy.rect.x -= diff

        # If the player gets near the left side, shift the world right (+x)
        if p.rect.left <= 400 and p.level.edge_sprites[0].rect.left < 0:
            diff = 400 - p.rect.left
            p.rect.left = 400
            current_level.shift_world_x(diff)

            #this shifts all the rope objects as needed
            for rope in p.rope_list:
                rope.rect.x += diff
                for segment in rope.rope_segments:
                    segment.rect.x += diff
                    
            #updates all the knife objects as needed
            for knife in p.knife_list:
                knife.rect.x += diff
                
            #for enemy in enemy_sprite_list:
            #    enemy.rect.x += diff

        # If the player gets near the bottom, shift the world up (-x)
        if p.rect.bottom >= 600 and p.level.edge_sprites[3].rect.bottom >= screen_height:
            diff = p.rect.bottom - 600
            p.rect.bottom = 600
            current_level.shift_world_y(-diff)

            #this shifts all the rope objects as needed
            for rope in p.rope_list:
                rope.rect.y -= diff
                for segment in rope.rope_segments:
                    segment.rect.y -= diff
                    
            #updates all the knife objects as needed
            for knife in p.knife_list:
                knife.rect.y -= diff
                
            #for enemy in enemy_sprite_list:
            #    enemy.rect.y -= diff

        # If the player gets near the top, shift the world down (+x)
        if p.rect.top <= 200 and p.level.edge_sprites[2].rect.top < 0:
            diff = 200 - p.rect.top
            p.rect.top = 200
            current_level.shift_world_y(diff)
            
            #updates all the knife objects as needed
            for knife in p.knife_list:
                knife.rect.y += diff
                
            #this shifts all the rope objects as needed
            for rope in p.rope_list:
                rope.rect.y += diff
                for segment in rope.rope_segments:
                    segment.rect.y += diff


        if p.num_of_ropes >= 10:
            ropeDisplay = ropeCounter[10]
        elif p.num_of_ropes <= 0:
            ropeDisplay = ropeCounter[0]
        else:
            ropeDisplay = ropeCounter[p.num_of_ropes]

        screen.blit(ropeDisplay, (200,5))

        if p.num_of_knives >= 10:
            knifeDisplay = knifeCounter[10]
        elif p.num_of_knives <= 0:
            knifeDisplay = knifeCounter[0]
        else:
            knifeDisplay = knifeCounter[p.num_of_knives]

        screen.blit(knifeDisplay, (350,5))

        screen.blit(whip_item, (500, 5))

        if p.inv == 0:
            screen.blit(selection_box, (190,0))
        elif p.inv == 1:
            screen.blit(selection_box, (340,0))
        else:
            screen.blit(selection_box, (490,0))
                    
            #for enemy in enemy_sprite_list:
            #    enemy.rect.y += diff

        if p.exit_level == 'y':
            if current_level_no <= maxLevels:
                current_level_no += 1
                # current_level = level_list[current_level_no]

                # current level is generated from a call to Level.  Calling it when it is needed instead
                # of at the beginning of the game will allow for easier expansion in the number of levels
                if current_level_no <= 3:
                    current_level = Level.dirt_level(5,5, constants.SCREEN_WIDTH * 5, constants.SCREEN_HEIGHT *5, p, current_level_no)
                    p.level = current_level
                    p.rect.x = current_level.entrance_coords['x']
                    p.rect.y = current_level.entrance_coords['y']
                elif current_level_no > 3 and current_level_no <= 6:
                    current_level = Level.castle_level(5, 5, constants.SCREEN_WIDTH * 5, constants.SCREEN_HEIGHT * 5, p, current_level_no)
                    p.level = current_level
                    p.rect.x = current_level.entrance_coords['x']
                    p.rect.y = current_level.entrance_coords['y']
                elif current_level_no > 6:
                    current_level = Level.snow_level(5, 5, constants.SCREEN_WIDTH * 5, constants.SCREEN_HEIGHT * 5, p, current_level_no)
                    p.level = current_level
                    p.rect.x = current_level.entrance_coords['x']
                    p.rect.y = current_level.entrance_coords['y']
                # p.level = current_level
                # p.rope_object.level = current_level
                p.exit_level = 'n'

                # remove all enemy sprites from active list
                for sprite in enemy_sprite_list:
                    if sprite.total_snowballs > 0:
                        active_sprite_list.remove(sprite.snowballGroup)
                    if sprite in active_sprite_list:
                        active_sprite_list.remove(sprite)

                # generate new set of enemies for new level
                # enemy_sprite_list = generateEnemies(current_level_no)
                enemy_sprite_list = current_level.enemy_list

                # add newly generated list of enemies to active list
                active_sprite_list.add(enemy_sprite_list)

                for enemy in enemy_sprite_list:
                    enemy.playerGroup = playerGroup
                    if enemy.total_snowballs > 0:
                        for snowball in enemy.snowballGroup:
                            active_sprite_list.add(snowball)

                # update level for all sprites (enemy, player, and rope)
                for sprite in active_sprite_list:
                    sprite.level = current_level

                p.level = current_level
                p.enemies = enemy_sprite_list
            else:
                pygame.quit()
                quit()

        if p.knifePickup:
            for i in range(0, 5):
                knife_object = Knife()
                knife_object.level = current_level
                p.knife_list.append(knife_object)
                p.num_of_knives += 1
                p.total_knives += 1
                active_sprite_list.add(knife_object)
            p.knifePickup = False
        if p.ropePickup:
            for i in range(0, 5):
                rope_object = Rope()
                rope_object.level = current_level
                p.rope_list.append(rope_object)
                p.num_of_ropes += 1
                p.total_ropes += 1
                active_sprite_list.add(rope_object)
            p.ropePickup = False
        
            


        active_sprite_list.draw(screen)

        # for enemy in enemy_sprite_list:
        #     enemy.detectCollision(p)

        # p.update()
        # pygame.draw.rect(screen, constants.BLACK, [p.lead_x, p.lead_y, 10,10])

        # if an enemy collides with the player, add it to enemies Hit
        enemiesHit = pygame.sprite.spritecollide(p, enemy_sprite_list, True)

        # for all enemies in enemiesHit, kill the enemy
        # once a health system is implemented, we will need to change the detection
        # for how we want the enemies to die otherwise, they will harm the player
        for enemy in enemiesHit:
            enemy.kill()

        pygame.display.update()

        # this is for controlling the Frames per Second
        clock.tick(FPS)


# Call the main function, start up the game
if __name__ == "__main__":
    main()
