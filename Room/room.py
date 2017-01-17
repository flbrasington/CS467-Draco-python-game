'''
Course: CS 467 - Capstone
Program: Python platformer game
Dev Team: Frank Brasington
          Barry Hall
          Edwin Grove

File Description:
This file is used to generate a the random cells in a room.

'''

import pygame
import constants
import random

random.seed()

class Room:
	def __init__(self, height, width, screenWidth, screenHeight, roomType):
		# roomHeight is the number of rows of cells
		self.roomHeight = height
		# toomWidth is the number of columns of cells
		self.roomWidth = width
		'''
		the sizes of the cells as defined below allow them all to be displayed on the screen
		the player should not be able to view all cells of a room, so this will need to be changed
		'''
		# width of one cell
		self.cellWidth = screenWidth/width
		# height of one cell
		self.cellHeight = screenHeight/height

		# this will need to be worked on with the room types from the path file
		# entrances on the right can exit to the top or left
		# entrances on the left can exit to the top or right
		# entrances on the bottom, can exit left, right, or top
		if roomType == 1:
			self.entrance = 'Right'
			self.exit = 'Left'
		elif roomType == 2:
			self.entrance = 'Right'
			self.exit = 'Top'
		elif roomType == 3:
			self.entrance = 'Left'
			self.exit = 'Right'
		elif roomType == 4:
			self.entrance = 'Left'
			self.exit = 'Top'
		elif roomType == 5:
			self.entrance = 'Bottom'
			self.exit = 'Right'
		elif roomType == 6:
			self.entrance = 'Bottom'
			self.exit = 'Left'
		else:
			self.entrance = 'Bottom'
			self.exit = 'Top'

	def generate(self):
		self.cells = []
		# create array of arrays with one array per row
		for i in range(0, self.roomHeight):
			self.cells.append([])

		# assign black color to all cells on first row (bottom edge)
		for i in range(0, self.roomWidth):
			self.cells[0].append(constants.BLACK)

		# if the entrance is on the right, place it in the right column
		# of a row that is in the bottom half of the cell
		if self.entrance == 'Right':
			entranceRow = random.randrange(1, int(self.roomHeight/2))
			self.entranceCoord = {'x': self.roomWidth-2, 'y': entranceRow}
		# if the entrance is on the left, place it in the left column
		# of a row in the bottom half of the cell
		elif self.entrance == 'Left':
			entranceRow = random.randrange(1, int(self.roomHeight/2))
			self.entranceCoord = {'x': 1, 'y': entranceRow}
		# the entrance is on the bottom, so put it in the bottom row
		# in a column that is neither on the left nor right edge
		else:
			entranceCol = random.randrange(2, int(self.roomWidth-2))
			self.entranceCoord = {'x': entranceCol, 'y': 1}

		# print("entrance " + self.entrance + " " + str(self.entranceCoord))

		# if the exit is on the right, place it on the right column
		# in a row that is in the top half of the cell
		if self.exit == 'Right':
			exitRow = random.randrange(int(self.roomHeight/2), self.roomHeight-1)
			self.exitCoord = {'x': self.roomWidth-2, 'y': exitRow}
		# if the exit is on the left, place it on the left column
		# in a row that is in the top half of the cell
		elif self.exit == 'Left':
			exitRow = random.randrange(int(self.roomHeight/2), self.roomHeight-1)
			self.exitCoord = {'x': 1, 'y': exitRow}
		# the exit is on the top, so put it in the top row
		# in a column that is neither on the left nor right edge
		else:
			exitCol = random.randrange(2, self.roomWidth-2)
			self.exitCoord = {'x': exitCol, 'y': self.roomHeight-1}

		# print("exit " + self.exit + " " + str(self.exitCoord))

		# for the rows between bottom edge and top edge
		for row in range(1, self.roomHeight-1):
			# make first cell of the row black (left edge)
			self.cells[row].append(constants.BLACK)
			# for the columns between the left edge and right edge
			for col in range(1, self.roomWidth-1):
				# if cell is entrance, make it lime green
				if row == self.entranceCoord['y'] and col == self.entranceCoord['x']:
					self.cells[row].append(constants.LIME_GREEN)
					continue
				# # if cell is exit, make it red
				if row == self.exitCoord['y'] and col == self.exitCoord['x']:
					self.cells[row].append(constants.RED)
					continue
				# choose a random type of cell
				n = random.randrange(0, 4)
				# cell type 0 will be open space in working model
				# we probably need to work on a way to get more cells of this type
				if n == 0:
					self.cells[row].append(constants.WHITE)
				# cell type 1
				elif n == 1:
					self.cells[row].append(constants.GREEN)
				# cell type 2
				elif n == 2:
					self.cells[row].append(constants.BLUE)
				# cell type 3
				else:
					self.cells[row].append(constants.GRAY)
			# make last cell in row black (right edge)
			self.cells[row].append(constants.BLACK)

		# make cells in last row black (top edge)
		for i in range(0, self.roomWidth):
			self.cells[self.roomHeight-1].append(constants.BLACK)

		# reverse array because it is built from the bottom up but it is printed from the top down
		self.cells.reverse()
		# print(self.cells)

	def draw_screen(self, screen):
        # Print path to screen
        # NOTE:  You must pass in the output destination

        # background
		screen.fill(constants.GOLD)

		# modified from path.py
		for row in range(self.roomHeight):
			for col in range(self.roomWidth):
				pygame.draw.rect(screen, self.cells[row][col], [col*self.cellWidth, row*self.cellHeight, self.cellWidth-10, self.cellHeight-10], 0)

def main():
    #Call this function so the pygame library can initialize itself
    pygame.init()

    screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])

    #Set the title of the window
    pygame.display.set_caption("Room Algorithm")

    #Loop until the user clicks the close button
    done = False
    clock = pygame.time.Clock()
    level = [1]

    # Room(height, width, SW, SH, Room Type)
    room = Room(11, 11, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, 1)

    #-----MAIN PROGRAM LOOP-----#
    # a room will need to be generated for every room in the path for a level
    for r in level:

        #ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        #ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

        room.generate()

        #ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        #ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        #clear the screen and set the screen background

        if not done:
            room.draw_screen(screen)


        #ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        #update the screen with what has been drawn
        pygame.display.flip()

        #limits the loop to 60 times per second
        clock.tick(4)

    #**********
    #this code is only here so the user can look over the program.

    #used for displaying the exit game text
    myfont = pygame.font.SysFont("None", 60)
    done = False
    while not done:
        label = myfont.render("press esc key to quit", 0, constants.BLACK)
        screen.blit(label, (100, 100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True



        

    pygame.quit()


if __name__ == "__main__":
	main()