'''
image credits

backgrounds and blocks: http://opengameart.org/content/platformer-art-deluxe
spelunky guy, snakes, and yeti: https://www.spriters-resource.com/pc_computer/spelunky/
'''

import pygame

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
 
ghostWalk = addImages(4, 'ghost', 'ghost_walk')

snowmanAttack = addImages(3, 'snowman', 'snowman')

blueSnakeAttack = addImages(8, 'BlueSnake', 'BlueSnakeAttack')

blueSnakeWalk = addImages(8, 'BlueSnake', 'BlueSnakeWalk')

spelunkyGuyWalk = addImages(9, 'SpelunkyGuy', 'spelunkyGuyWalk')

spelunkyGuyClimb = addImages(10, 'SpelunkyGuy', 'spelunkyGuyClimb')

yetiWalk = addImages(7, 'Yeti', 'yetiWalk')

ropeCounter = []
for i in range(0, 11):
	ropeCounter.append("Graphics/Rope/RopeCount" + str(i) + ".png")

knifeCounter = []
for i in range(0,11):
        knifeCounter.append("Graphics/Inventory/KnifeCount" + str(i) + ".png")

selection_box = pygame.image.load("Graphics/Inventory/selection_box.png")

whip_large = pygame.image.load("Graphics/Inventory/whip_large.png")

whip_animation = []
for i in range(1, 10):
        whip_animation.append("Graphics/Whip/whip" + str(i) +".png")

TILEDICT = {'ice block': pygame.image.load('Graphics/tiles/iceBlock.png'),
			'ice block wall': pygame.image.load('Graphics/tiles/iceBlockWall.png'),
			'ice block alt': pygame.image.load('Graphics/tiles/iceBlockAlt.png'),
			'tundra': pygame.image.load('Graphics/tiles/tundra.png'),
			'tundra center': pygame.image.load('Graphics/tiles/tundraCenter.png'),
			'dirt block wall': pygame.image.load('Graphics/tiles/dirtBlockWall.png'),
			'dirt center': pygame.image.load('Graphics/tiles/dirtCenter.png'),
			'castle wall': pygame.image.load('Graphics/tiles/castleWall.png'),
			'castle center': pygame.image.load('Graphics/tiles/castleCenter.png'),
			'spikes': pygame.image.load('Graphics/tiles/spikes.png')}
