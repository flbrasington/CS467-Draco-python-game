'''
image credits

backgrounds and blocks: http://opengameart.org/content/platformer-art-deluxe
spelunky guy, snakes, and yeti: https://www.spriters-resource.com/pc_computer/spelunky/
ghost https://www.spriters-resource.com/snes/smarioworld/
'''

import pygame
import constants

def addImages(numImg, folder, prefix):
	array = []
	for i in range(1, numImg + 1):
		filename = "Graphics/" + folder + "/" + prefix + str(i) + ".png"
		array.append(filename)

	return array

# to add images, list the number of images to add, the name of the folder, and
# the start of the filename for the images
greenSnakeAttack = addImages(10, 'GreenSnake', 'Snake_attack_')

greenSnakeWalk = addImages(11, 'GreenSnake', 'Snake_walk_')
 
# ghostWalk = addImages(4, 'ghost', 'ghost_walk')
ghostWalk = addImages(5, 'ghost', 'marioGhost')

snowmanStand = []
for i in range(0, 10):
	snowmanStand.append("Graphics/snowman/snowman1.png")

snowmanAttack = addImages(7, 'snowman', 'snowman')

blueSnakeAttack = addImages(8, 'BlueSnake', 'BlueSnakeAttack')

blueSnakeWalk = addImages(8, 'BlueSnake', 'BlueSnakeWalk')

spelunkyGuyWalk = addImages(9, 'SpelunkyGuy', 'spelunkyGuyWalk')

spelunkyGuyClimb = addImages(10, 'SpelunkyGuy', 'spelunkyGuyClimb')

spelunkyGuyAttack = addImages(6, 'SpelunkyGuy', 'spelunkyGuyAttack')

spelunkyGuyWallClimbLeft = addImages(8, 'SpelunkyGuy', 'spelunkyGuyWall')

spelunkyGuyWallClimbRight = addImages(8, 'SpelunkyGuy', 'spelunkyGuyWall_right')

spelunkyGuyDamage = pygame.image.load("Graphics/SpelunkyGuy/guy_damage.png")

spelunkyGuyGhost = pygame.image.load("Graphics/SpelunkyGuy/guy_ghost.png")

yetiWalk = addImages(7, 'Yeti', 'yetiWalk')

selection_box = pygame.image.load("Graphics/Inventory/selection_box.png")

whip_large = pygame.image.load("Graphics/Inventory/whip_large.png")

whip = addImages(3, 'Whip', 'whip')

ropePile = pygame.image.load("Graphics/Rope/rope_pile2.png")

knifeIcon = pygame.image.load("Graphics/Inventory/knife_large.png")

TILEDICT = {'ice block': pygame.image.load('Graphics/tiles/iceBlock.png'),
			'ice block wall': pygame.image.load('Graphics/tiles/landscape.png'),
			'ice block alt': pygame.image.load('Graphics/tiles/iceBlockAlt.png'),
			'tundra': pygame.image.load('Graphics/tiles/tundra.png'),
			'snow mid top': pygame.image.load('Graphics/tiles/snow_mid_top.png'),
			'snow center': pygame.image.load('Graphics/tiles/snow_center.png'),
			'dirt block wall': pygame.image.load('Graphics/tiles/landscape.png'),
			'dirt center': pygame.image.load('Graphics/tiles/dirt_center.png'),
			'dirt mid top': pygame.image.load('Graphics/tiles/dirt_mid_top.png'),
			'plat right': pygame.image.load('Graphics/tiles/dirt_plat_right.png'),
			'dirt dart': pygame.image.load('Graphics/tiles/dirtMid.png'),
			'castle wall': pygame.image.load('Graphics/tiles/landscape.png'),
			'castle center': pygame.image.load('Graphics/tiles/castle_center.png'),
			'castle mid top': pygame.image.load('Graphics/tiles/castle_mid_top.png'),
			'spikes': pygame.image.load('Graphics/tiles/spikes.png'),
			'castle dart': pygame.image.load('Graphics/tiles/castle_mid_top.png')}

#buttons for the menu
quit_button1 = pygame.image.load("Graphics/menu/quitgame1.png")
quit_button2 = pygame.image.load("Graphics/menu/quitgame2.png")
next_song1 = pygame.image.load("Graphics/menu/next_song1.png")
next_song2 = pygame.image.load("Graphics/menu/next_song2.png")
prev_song1 = pygame.image.load("Graphics/menu/prev_song1.png")
prev_song2 = pygame.image.load("Graphics/menu/prev_song2.png")
music_up1 = pygame.image.load("Graphics/menu/music_up1.png")
music_up2 = pygame.image.load("Graphics/menu/muisc_up2.png")
music_down1 = pygame.image.load("Graphics/menu/music_down1.png")
music_down2 = pygame.image.load("Graphics/menu/music_down2.png")
return1 = pygame.image.load("Graphics/menu/return1.png")
return2 = pygame.image.load("Graphics/menu/return2.png")
button_back = pygame.image.load("Graphics/menu/button_background.png")
background_menu = pygame.image.load("Graphics/menu/background_menu.png")
game_menu1 = pygame.image.load("Graphics/menu/game_menu1.png")
game_menu2 = pygame.image.load("Graphics/menu/game_menu2.png")
new_game1 = pygame.image.load("Graphics/menu/new_game1.png")
new_game2 = pygame.image.load("Graphics/menu/new_game2.png")
bar_button = pygame.image.load("Graphics/menu/bar_button.png")
game_display = pygame.image.load("Graphics/menu/game_display.png")

#game over images
game_over = pygame.image.load("Graphics/GameOver/GameOver.png")
background = pygame.image.load("Graphics/GameOver/moutains.png")
press_a = pygame.image.load("Graphics/GameOver/press_a.png")

#game credits
congrat = pygame.image.load("Graphics/menu/congrats.png")
game_credits = pygame.image.load("Graphics/menu/CREDITS.png")

