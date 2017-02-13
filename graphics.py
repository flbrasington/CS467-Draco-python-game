def addImages(numImg, folder, prefix):
	array = []
	for i in range(1, numImg + 1):
		filename = "Graphics/" + folder + "/" + prefix + str(i) + ".png"
		array.append(filename)

	return array

greenSnakeAttack = addImages(8, 'Snake', 'Snake_attack_')

# for i in range(1, 9):
# 	filename = "Graphics/Snake/Snake_attack_" + str(i) + ".png"
# 	greenSnakeAttack.append(filename)

greenSnakeWalk = addImages(11, 'Snake', 'Snake_walk_')
 
# for i in range(1, 12):
# 	filename = "Graphics/Snake/Snake_walk_" + str(i) + ".png"
# 	greenSnakeWalk.append(filename)

ghostWalk = addImages(4, 'ghost', 'ghost_walk')

# for i in range(1, 5):
# 	filename = "Graphics/ghost/ghost_walk" + str(i) + ".png"
# 	ghostWalk.append(filename)

snowmanAttack = addImages(3, 'snowman', 'snowman')

# for i in range(1, 4):
# 	filename = "Graphics/snowman/snowman" + str(i) + ".png"