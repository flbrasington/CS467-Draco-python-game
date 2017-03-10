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
import os
import constants
import enemies
import collections
from sys import exit
import graphics

FPS = constants.fps

random.seed()

WHITE = constants.WHITE
BLUE = constants.BLUE
BLACK = constants.BLACK

# set height and width of window
SCREEN_WIDTH = constants.SCREEN_WIDTH
SCREEN_HEIGHT = constants.SCREEN_HEIGHT


class Level:
    """This class will create procedurally generated levels including
    a path of cells from entrance to exit and random cells"""

    def __init__(self, numRow, numCol, level_width, level_height, player, levelNum, theme):
        # constructor for level class

        # http://tinysubversions.com/spelunkyGen/
        # 0 = a room that is not part of the solution path
        # 1 = room with exits left and right
        # 2 = room with exits left right and bottom with open top with blocks, or some way to jump up to room above
        # 3 = room with exits left right and top
        # 4 = start and end room
        # NOTE: room 2 and three ALWAYS have completely open tops with no walls.  This is because cells rely on the
        # opening of the cell, or the floor of the cell,  above it to filter the player to the next cell

        # save height and width of level
        self.level_height = level_height
        self.level_width = level_width

        self.screen_width = constants.SCREEN_WIDTH
        self.screen_height = constants.SCREEN_HEIGHT

        self.levelNum = levelNum

        self.theme = theme

        # save number of rows and columns (cell grid) of level
        self.num_rows = numRow
        self.num_cols = numCol
        # the cell_side_length is how big each room in the level is going to be
        self.room_side_length_x = self.level_width / numCol
        self.room_side_length_y = self.level_height / numRow

        # ------RANDOMLY GENERATE ENTRANCE CELL AT BOTTOM OF LEVEL------#
        # create 2-d array and fill with 0's
        self.room_type = [[0] * numCol for _ in range(numRow)]
        # variables to keep track of start and end rooms
        self.start_room = {'row': None, 'column': None}
        self.entrance_coords = {'x': None, 'y': None}
        self.current_room_x = 0
        self.current_room_y = random.randrange(0, self.num_cols)
        self.room_type[self.current_room_x][self.current_room_y] = 4

        # save end room location
        self.end_room = {'row': self.current_room_x, 'column': self.current_room_y}
        self.exit_coords = {'x': None, 'y': None}

        # boolean variable to see if we moved up to the next row due to hitting the edge of level
        # initially starts as true so that we don't immediately down up if we start on an edge
        self.edge_row_jump = True
        self.number_of_rooms = 0
        done = False
        while not done:
            done = self.path()

        # for rows in self.room_type:
        #    print(rows)
        # --------------------------------------------------------------#

        # -----CONSTRUCTOR VARIABLES FOR SPRITES AND ROOM GENERATION----#
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.exit_sprite = pygame.sprite.Group()
        self.bagGroup = pygame.sprite.Group()
        self.blocks_per_room_x = constants.ROOM_WIDTH
        self.blocks_per_room_y = constants.ROOM_HEIGHT
        self.block_width = self.room_side_length_x / self.blocks_per_room_x
        self.block_height = self.room_side_length_y / self.blocks_per_room_y
        print(self.block_width, self.block_height)
        self.player = player
        self.edges = None
        self.edge_sprites = []

        self.level_edge()
        self.create_room()
        # --------------------------------------------------------------#
        # -----SHIFT WORLD SO THAT STARTING VIEW IS ON PLAYER------------#
        self.world_shift_x = self.block_width + self.start_room['column'] * self.room_side_length_x
        # world has been shifted so starting point is based on new zero position
        self.entrance_coords['x'] -= self.world_shift_x
        self.world_shift_y = self.level_height - self.room_side_length_y + self.block_height
        self.entrance_coords['y'] -= self.world_shift_y

        # shift world to the left
        self.shift_world_x(-self.world_shift_x)
        # shift world up
        self.shift_world_y(-self.world_shift_y)

        #if we start on the left side of screen, shift world so that the view is not over the edge of the map
        if (self.player.rect.left - self.edge_sprites[0].rect.left) < 300:
            self.entrance_coords['x'] += self.edge_sprites[0].rect.left - self.player.rect.left
            self.shift_world_x(self.edge_sprites[0].rect.left - self.player.rect.left)
        #if we start on the right side of screen, shift world so that the view is not over the edge of the map
        elif self.edge_sprites[1].rect.right < self.screen_width:
            self.entrance_coords['x'] += (self.screen_width - self.edge_sprites[1].rect.right)
            self.shift_world_x(self.screen_width - self.edge_sprites[1].rect.right)

        if self.edge_sprites[3].rect.bottom < self.screen_height:
            self.entrance_coords['y'] += self.screen_height - self.edge_sprites[3].rect.top
            self.shift_world_y(self.screen_height - self.edge_sprites[3].rect.bottom)

    def level_edge(self):

        # setting parameters for level edge
        # edges[0] = left edge
        # edges[1] = right edge
        # edges[2] = top edge
        # edges[3] = bottom edge
        #[width, height, x coord, y coord]
        self.edges = [[self.block_width, self.level_height + self.block_height * 2, 0, 0],
                      [self.block_width, self.level_height + self.block_height * 2, self.level_width + self.block_width,
                       0],
                      [self.level_width, self.block_height, self.block_width, 0],
                      [self.level_width, self.block_height, self.block_width, self.level_height + self.block_height]]

        for edge in self.edges:
            block = Platform(edge[0], edge[1], 'edge', self.theme)
            block.rect.x = edge[2]
            block.rect.y = edge[3]
            self.platform_list.add(block)
            self.edge_sprites.append(block)

    def path(self):
        """Create a path through level"""

        path_direction = random.randrange(1, 6)
        # print(path_direction)

        # if current room is on the edge of the level (column 0 or column 4 and we did not drop to that room
        # because of hitting an edge in the previous assignment, assign the current room to be of type 2 and the
        # new room above it to be of type 3 so that the rooms connect
        if self.current_room_y in (0, 4) and self.edge_row_jump is False:
            self.room_type[self.current_room_x][self.current_room_y] = 3
            self.current_room_x += 1
            # if we are at the bottom of level and attempt to go down again, we will have found our start room.  In this
            # we save the parameter and exit the loop
            if self.current_room_x > 4:
                self.room_type[self.current_room_x - 1][self.current_room_y] = 4
                self.start_room['row'] = self.current_room_x - 1
                self.start_room['column'] = self.current_room_y
                return True
            self.room_type[self.current_room_x][self.current_room_y] = 2
            # this is set to true so that we don't continue jumping up the side of the level
            self.edge_row_jump = True
            self.number_of_rooms += 1

        # if random number is 1 or 2 we move the path left and give that new room left/right exits
        elif path_direction in (1, 2):

            # if we are on the left edge of level then we shouldn't move left any further
            # if cell we are moving to has already been assigned then we should not move there either
            if self.current_room_y > 0 and self.room_type[self.current_room_x][self.current_room_y - 1] is 0:
                # we now have a new direction without jumping rows because of hitting an edge
                self.edge_row_jump = False
                # move current room to the left
                self.current_room_y -= 1
                # assign that room with a left/right exit
                self.room_type[self.current_room_x][self.current_room_y] = 1
                self.number_of_rooms += 1

        # if random number is 3 or 4 we move right and give that new room left/right exits
        elif path_direction in (3, 4):
            # check if the room we are moving to has already been assigned or is off the screen
            if self.current_room_y < 4 and self.room_type[self.current_room_x][self.current_room_y + 1] == 0:
                # we now have a new direction without jumping rows because of hitting an edge
                self.edge_row_jump = False
                # move current room to the right
                self.current_room_y += 1
                # assign that room with a left/right exit
                self.room_type[self.current_room_x][self.current_room_y] = 1
                self.number_of_rooms += 1

        # if random number is 5 then we are moving down
        elif self.number_of_rooms != 0 and path_direction is 5:
            self.edge_row_jump = False
            self.room_type[self.current_room_x][self.current_room_y] = 3
            # print cell to screen
            self.current_room_x += 1
            # if we are at bottom of level and attempt to go down again, we will have found our start room.  In this
            # we save the parameter and exit the loop
            if self.current_room_x > 4:
                self.room_type[self.current_room_x - 1][self.current_room_y] = 4
                self.start_room['row'] = self.current_room_x - 1
                self.start_room['column'] = self.current_room_y
                return True
            self.room_type[self.current_room_x][self.current_room_y] = 2
            self.number_of_rooms += 1

        # print array to see if movements are correct
        # for row in self.room_type:
        #    print(row)
        return False

    def create_room(self):
        """
        fill in each room based on templates

        """
        # iterate through array of room types
        rooms = []
        prob_block_5_list = []
        prob_block_6_list = []

        for row in self.room_type:
            for col in row:
                rooms.append(self.import_template(col))
        # iterate through rooms to fill screen
        # this number will be part of how we find location of top left corner of room
        # based on 5x5 grid of rooms
        for pos in range(25):
            # this will iterate through the number of columns in array
            # the number y will be part of how we find where to place the block on the y axis (according to pygame.draw)
            for y in range(self.blocks_per_room_y):
                # this will iterate through the number of rows in array
                # the number x will be part of how we find where to place the block on the x axis (according to pygame.draw)
                for x in range(self.blocks_per_room_x):
                    # if cell is a 1 add a platform sprite
                    if rooms[pos][y][x] is 1:
                        #check if platform has another above it for graphics
                        if rooms[pos][y - 1][x] in (0, 3, 4, 7) and y - 1 >= 0:
                            # the cases checked in each of these conditionals are the basic case that check surrounding blocks
                            # to see what platform we should be using, the edge cases, such as if a block is at the edge of
                            # the room, in which case we need to check the neighboring room (array in this case)

                            #check conditions to see if we are using the sprite with with rounded edges on the bottom right and top right
                            if ((y + 1) < self.blocks_per_room_y and (x - 1) >= 0 and (x + 1) < self.blocks_per_room_x
                                  and rooms[pos][y + 1][x] is 0 and rooms[pos][y][x + 1] is 0 and rooms[pos][y][x - 1] is 1)\
                                    or (x is self.blocks_per_room_x - 1 and y < self.blocks_per_room_y - 1 and pos < 24 and rooms[pos][y + 1][x] is 0 and rooms[pos + 1][y][0] is 0)\
                                    or (y is self.blocks_per_room_y - 1 and x < self.blocks_per_room_x - 1 and pos < 20 and rooms[pos][y][x + 1] is 0):
                                block = Platform(self.block_width, self.block_height, 'right', self.theme)
                            #check conditionals to see if we are using the sprite with rounded edges on the bottom left and top left
                            elif ((y + 1) < self.blocks_per_room_y and (x - 1) >= 0 and (x + 1) < self.blocks_per_room_x
                                  and rooms[pos][y + 1][x] is 0 and rooms[pos][y][x - 1] is 0 and rooms[pos][y][x + 1] is 1)\
                                    or (x is 0 and y < self.blocks_per_room_y - 1 and pos > 0 and rooms[pos][y + 1][x] is 0 and rooms[pos - 1][y][self.blocks_per_room_x - 1] is 0) \
                                    or (y is self.blocks_per_room_y - 1 and x > 0 and pos < 20 and rooms[pos][y][x - 1] is 0):
                                block = Platform(self.block_width, self.block_height, 'left', self.theme)
                            #check conditionals to see if we are using the sprite with the rounded corners on top left and top right
                            elif ((x + 1) < self.blocks_per_room_x and (x - 1) >= 0 and rooms[pos][y][x + 1] in (0, 3, 4) and rooms[pos][y][x - 1] in (0, 3, 4))\
                                    or (x is 0 and pos > 0 and rooms[pos - 1][y][self.blocks_per_room_x - 1] in (0, 3, 4) and rooms[pos][y][x + 1] in (0, 3, 4))\
                                    or (x is self.blocks_per_room_x - 1 and pos < 24 and rooms[pos + 1][y][0] in (0, 3, 4) and rooms[pos][y][x - 1] in (0, 3, 4)):
                                block = Platform(self.block_width, self.block_height, 'round top', self.theme)
                            elif ((y + 1) < self.blocks_per_room_y and (x - 1) >= 0 and (x + 1) < self.blocks_per_room_x
                                  and rooms[pos][y + 1][x] is 1 and rooms[pos][y][x - 1] is 0 and rooms[pos][y][x + 1] is 1) \
                                    or (x is 0 and y < self.blocks_per_room_y - 1 and pos > 0 and rooms[pos][y + 1][x] is 1 and rooms[pos - 1][y][self.blocks_per_room_x - 1] is 0) \
                                    or (y is self.blocks_per_room_y - 1 and x > 0 and pos < 20 and rooms[pos][y][x - 1] is 0):
                                block = Platform(self.block_width, self.block_height, 'top left', self.theme)
                            elif ((y + 1) < self.blocks_per_room_y and (x - 1) >= 0 and (x + 1) < self.blocks_per_room_x
                                  and rooms[pos][y + 1][x] is 1 and rooms[pos][y][x + 1] is 0 and rooms[pos][y][x - 1] is 1)\
                                    or (x is self.blocks_per_room_x - 1 and y < self.blocks_per_room_y - 1 and pos < 24 and rooms[pos][y + 1][x] is 0 and rooms[pos + 1][y][0] is 0)\
                                    or (y is self.blocks_per_room_y - 1 and x < self.blocks_per_room_x - 1 and pos < 20 and rooms[pos][y][x + 1] is 0):
                                block = Platform(self.block_width, self.block_height, 'top right', self.theme)
                            else:
                                block = Platform(self.block_width, self.block_height, 'top', self.theme)
                        else:
                            block = Platform(self.block_width, self.block_height, 'middle', self.theme)
                        coord_x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                        block.rect.x = coord_x
                        block.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                        block.player = self.player
                        self.platform_list.add(block)
                        #if the space above this block is empty see if we spawn an enemy on the spot above current block
                        if rooms[pos][y-1][x] is 0 and y - 1 >= 0:
                            self.enemy_generation(coord_x, self.block_height + (pos // 5) * self.room_side_length_y + (y - 1) * self.block_height)
                    # if the cell is a 3 then it will be an item pickup
                    elif rooms[pos][y][x] is 3:
                        rand = random.randrange(0, 4)
                        if rand == 0:
                            #calculate coordinates of the bag
                            bag = pickupSprite('rope')
                            # print('width = ' + str(self.block_width) + ' height = ' + str(self.block_height))
                            bag.rect.x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                            bag.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                            bag.player = self.player
                            self.bagGroup.add(bag)
                        elif rand == 1:
                            #calculate coordinates of the bag
                            bag = pickupSprite('knife')
                            # print('width = ' + str(self.block_width) + ' height = ' + str(self.block_height))
                            bag.rect.x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                            bag.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                            bag.player = self.player
                            self.bagGroup.add(bag)
                        elif rand == 2:
                            bag = pickupSprite('health')
                            bag.rect.x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                            bag.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                            bag.player = self.player
                            self.bagGroup.add(bag)


                    # if the cell is a 4 then it will be either a spike, if the space is on the bottom of the room,
                    # otherwise it is a randomized block or nothing
                    elif rooms[pos][y][x] is 4:
                        # if the cell is at the bottom of the level, randomly choose whether to place a spike or not
                        rand = random.randrange(0, 3)
                        rand2 = random.randrange(0, 2)
                        if y is 6 and rand is 1:
                            spike = enemies.Spikes()
                            spike.rect.x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                            spike.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                            spike.player = self.player
                            self.enemy_list.add(spike)
                        # elif y is 6 and rand is 2:
                        #     dart = enemies.Darts(self.theme, 'up')
                        #     dart.rect.x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                        #     dart.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                        #     dart.player = self.player
                        #     self.enemy_list.add(dart)
                        elif y != 6 and rand2 is 0:
                            if rooms[pos][y - 1][x] is 0:
                                block = Platform(self.block_width, self.block_height, 'top', self.theme)
                            else:
                                block = Platform(self.block_width, self.block_height, 'middle', self.theme)
                            block.rect.x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                            block.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                            block.player = self.player
                            self.platform_list.add(block)
                        elif y != 6 and rand2 is 1:
                            if x-1 >= 0 and x+1 <= self.blocks_per_room_x and y-1 >= 0 and y+1 < self.blocks_per_room_y:
                                if rooms[pos][y][x-1] is 0:
                                    direction = 'left'
                                    blockType = 'middle'
                                elif rooms[pos][y][x+1] is 0:
                                    direction = 'right'
                                    blockType = 'middle'
                                elif rooms[pos][y-1][x] is 0:
                                    direction = 'up'
                                    blockType = 'top'
                                elif rooms[pos][y+1][x] is 0:
                                    direction = 'down'
                                    blockType = 'middle'
                            else:
                                direction = None
                            if direction is not None:
                                # use for both block and dart
                                rectX = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                                rectY = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height

                                block = Platform(self.block_width, self.block_height, blockType, self.theme)
                                block.rect.x = rectX
                                block.rect.y = rectY
                                block.player = self.player
                                self.platform_list.add(block)

                                dart = enemies.Darts(self.theme, direction)
                                dart.rect.x = rectX
                                dart.rect.y = rectY
                                dart.player = self.player
                                self.enemy_list.add(dart)
                    # this is the starting and ending points of the level
                    elif rooms[pos][y][x] is 7:
                        # exit of the game on the top row of the level
                        if pos // 5 is 0:
                            #calculate coordinates of the exit
                            self.exit_coords['x'] = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                            self.exit_coords['y'] = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                            exit = exit_door_sprite(self.block_width, self.block_height)
                            # print('width = ' + str(self.block_width) + ' height = ' + str(self.block_height))
                            exit.rect.x = self.exit_coords['x']
                            exit.rect.y = self.exit_coords['y']
                            exit.player = self.player
                            self.exit_sprite.add(exit)
                        #entance of the game on the bottom row of the level
                        elif pos // 5 is 4:
                            #calculate coordinates of the entrance
                            self.entrance_coords['x'] = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                            self.entrance_coords['y'] = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height

    def import_template(self, room_number):
        # if room type is 0 then import random file from r_type_0 directory
        # create empty list that will hold block types
        room = []
        path = "room_templates/"
        if room_number is 0:
            # path to room 0 files
            path += "r_type_0/"
        elif room_number is 1:
            path += "r_type_1/"
        elif room_number is 2:
            path += "r_type_2/"
        elif room_number is 3:
            path += "r_type_3/"
        elif room_number is 4:
            path += "r_type_4/"
        elif room_number is 5:
            path += "prob_block_5/"
        elif room_number is 6:
            path += "prob_block_6/"

        # create list of possible files
        file_list = os.listdir(path)
        # randomly choose file
        file = random.choice(file_list)
        # add filename to path string
        path += file
        # open file and read
        # (help from http://stackoverflow.com/questions/12271503/python-read-numbers-from-text-file-and-put-into-list)
        with open(path) as f:
            for line in f:
                # split numbers according to spaces
                line = line.split()
                if line:
                    line = [int(i) for i in line]
                    room.append(line)
        return room

    def enemy_generation(self, coord_x, coord_y):
        """
        :Description: Uses probability to decide whether or not to spawn an enemy.  If an enemy is to be spawned then
        :             it uses randomization again to choose which enemy to spawn with less difficult enemies at a higher
        :             likelihood than more difficult enemies.
        :param coord_x:
        :param coord_y:
        :return:
        """
        total_value = 0
        #randomization of whether or not spawn an enemy, the higher the level the more likely an enemy will spawn
        gen_chance = 42//((self.levelNum - 1) % 3 + 1)
        if random.randrange(0, gen_chance) is 1:
            #generate value based on total of values in the enemy_types ordered dictionary
            enemy_choice = random.randrange(0, self.total_enemies)
            #iterate through list and check enemy choice value against enemy likelihood
            for enemy, value in self.enemy_types.items():
                value += total_value
                if enemy_choice < value:
                    print(enemy, " spawned in level ", self.levelNum)
                    enemy_class = getattr(enemies, enemy)
                    enemy_instance = enemy_class()
                    enemy_instance.rect.x = coord_x
                    enemy_instance.rect.y = coord_y
                    enemy_instance.player = self.player
                    self.enemy_list.add(enemy_instance)
                    print(coord_x, coord_y)
                    break
                total_value += value



    def draw_screen_path(self, screen):
        """
        :Description: draws the path through the level onto screen
        :param screen:
        :return:
        """
        screen.fill(WHITE)
        # screen.blit(constants.TILEDICT['ice block wall'], constants.TILEDICT['ice block wall'].get_rect())
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                # if a room is on the path then color the cell blue on the screen
                if self.room_type[x][y] != 0:
                    # NOTE: we are multiplying current_room.y and cell_side_length.x because cell_side_length refers to the x and
                    # y axis as pygame.draw uses it, while current_room.x or y refers to the row major array that python uses
                    # for 2-d arrays. the location of the top left corner of the rectangle we are going to draw is the y array
                    # value multiplied by the x row number (I know this is disorienting)
                    pygame.draw.rect(screen, BLUE, [y * self.room_side_length_x,
                                                    x * self.room_side_length_y,
                                                    self.room_side_length_x - 10,
                                                    self.room_side_length_y - 10], 0)

    def shift_world_x(self, shift_x):
        """ When the user moves left/right and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift_x += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
            # shift x for projectiles
            if enemy.total_snowballs > 0:
                snowballs = enemy.snowballGroup.sprites()
                for ball in snowballs:
                    ball.rect.x += shift_x
            if enemy.numOfDarts > 0:
                darts = enemy.dartGroup.sprites()
                for dart in darts:
                    dart.rect.x += shift_x

        for exit_door in self.exit_sprite:
            exit_door.rect.x += shift_x

        for bag in self.bagGroup:
            bag.rect.x += shift_x


    def shift_world_y(self, shift_y):
        """ When the user moves up/down and we need to scroll
        everything: """

        # Keep track of the shift amount
        self.world_shift_y += shift_y

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y += shift_y

        for enemy in self.enemy_list:
            enemy.rect.y += shift_y
            # shift y for projectiles
            if enemy.total_snowballs > 0:
                snowballs = enemy.snowballGroup.sprites()
                for ball in snowballs:
                    ball.rect.y += shift_y
            if enemy.numOfDarts > 0:
                darts = enemy.dartGroup.sprites()
                for dart in darts:
                    dart.rect.y += shift_y

        for exit_door in self.exit_sprite:
            exit_door.rect.y += shift_y

        for bag in self.bagGroup:
            bag.rect.y += shift_y

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.exit_sprite.update()
        self.bagGroup.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(constants.WHITE)
        if self.theme == 'dirt':
            screen.blit(graphics.TILEDICT['dirt block wall'], graphics.TILEDICT['dirt block wall'].get_rect())
        elif self.theme == 'snow':
            screen.blit(graphics.TILEDICT['ice block wall'], graphics.TILEDICT['ice block wall'].get_rect())
        elif self.theme == 'castle':
            screen.blit(graphics.TILEDICT['castle wall'], graphics.TILEDICT['castle wall'].get_rect())

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.exit_sprite.draw(screen)
        self.bagGroup.draw(screen)


class dirt_level(Level):
    """
    create the dirt level themed levels
    """
    def __init__(self, numRow, numCol, level_width, level_height, player, levelNum):

        #make a dictionary of enemies for this level theme.  I am using an order dictionary for the enemy generation function
        self.enemy_types = collections.OrderedDict()

        #enter the likelihood of an enemy being spawned (make sure that it is in descending order starting with the
        #most likely enemy to spawn in a level
        self.enemy_types['green_snake'] = 4
        self.enemy_types['BlueSnake'] = 2
        self.enemy_types['ghost'] = 1

        self.total_enemies = sum(self.enemy_types.values())

        #specify theme
        self.theme = 'dirt'

        super().__init__(numRow, numCol, level_width, level_height, player, levelNum, self.theme)

class snow_level(Level):
    """
    create the snow level themed levels
    """
    def __init__(self, numRow, numCol, level_width, level_height, player, levelNum):

        #make a dictionary of enemies for this level theme.  I am using an order dictionary for the enemy generation function
        self.enemy_types = collections.OrderedDict()

        # enter the likelihood of an enemy being spawned (make sure that it is in descending order starting with the
        # most likely enemy to spawn in a level
        # self.enemy_types['green_snake'] = 4
        self.enemy_types['Yeti'] = 5
        self.enemy_types['SnowMan'] = 4
        self.enemy_types['BlueSnake'] = 2
        # self.enemy_types['Yeti'] = 1
        self.enemy_types['ghost'] = 1

        self.total_enemies = sum(self.enemy_types.values())

        #specify theme
        self.theme = 'snow'

        super().__init__(numRow, numCol, level_width, level_height, player, levelNum, self.theme)

class castle_level(Level):
    """
    create the castle level themed levels
    """
    def __init__(self, numRow, numCol, level_width, level_height, player, levelNum):

        #make a dictionary of enemies for this level theme.  I am using an order dictionary for the enemy generation function
        self.enemy_types = collections.OrderedDict()

        #enter the likelihood of an enemy being spawned (make sure that it is in descending order starting with the
        #most likely enemy to spawn in a level
        self.enemy_types['BlueSnake'] = 4
        self.enemy_types['HiredHand'] = 3
        self.enemy_types['Viking'] = 2
        self.enemy_types['ghost'] = 1

        self.total_enemies = sum(self.enemy_types.values())

        #specify theme
        self.theme = 'castle'

        super().__init__(numRow, numCol, level_width, level_height, player, levelNum, self.theme)




class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height, platformType, theme):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        if platformType == 'edge':
            self.image.fill(constants.DARK_GREY)

        else:
            self.image.fill(constants.WHITE)
            self.image.set_colorkey(constants.WHITE)
            if theme == 'dirt':
                if platformType == 'top':
                    self.image.blit(graphics.TILEDICT['dirt mid top'], graphics.TILEDICT['dirt mid top'].get_rect())
                elif platformType == 'round top':
                    self.image.blit(graphics.TILEDICT['dirt round top'], graphics.TILEDICT['dirt round top'].get_rect())
                elif platformType == 'right':
                    self.image.blit(graphics.TILEDICT['dirt plat right'], graphics.TILEDICT['dirt plat right'].get_rect())
                elif platformType == 'left':
                    self.image.blit(graphics.TILEDICT['dirt plat left'], graphics.TILEDICT['dirt plat left'].get_rect())
                elif platformType == 'top left':
                    self.image.blit(graphics.TILEDICT['dirt top left'], graphics.TILEDICT['dirt top left'].get_rect())
                elif platformType == 'top right':
                    self.image.blit(graphics.TILEDICT['dirt top right'], graphics.TILEDICT['dirt top right'].get_rect())
                else:
                    self.image.blit(graphics.TILEDICT['dirt center'], graphics.TILEDICT['dirt center'].get_rect())
            elif theme == 'snow':
                if platformType == 'top':
                    self.image.blit(graphics.TILEDICT['snow mid top'], graphics.TILEDICT['snow mid top'].get_rect())
                elif platformType == 'round top':
                    self.image.blit(graphics.TILEDICT['snow round top'], graphics.TILEDICT['snow round top'].get_rect())
                elif platformType == 'right':
                    self.image.blit(graphics.TILEDICT['snow plat right'],graphics.TILEDICT['snow plat right'].get_rect())
                elif platformType == 'left':
                    self.image.blit(graphics.TILEDICT['snow plat left'], graphics.TILEDICT['snow plat left'].get_rect())
                elif platformType == 'top left':
                    self.image.blit(graphics.TILEDICT['snow top left'], graphics.TILEDICT['snow top left'].get_rect())
                elif platformType == 'top right':
                    self.image.blit(graphics.TILEDICT['snow top right'], graphics.TILEDICT['snow top right'].get_rect())
                else:
                    self.image.blit(graphics.TILEDICT['snow center'], graphics.TILEDICT['snow center'].get_rect())
            elif theme == 'castle':
                if platformType == 'top':
                    self.image.blit(graphics.TILEDICT['castle mid top'], graphics.TILEDICT['castle mid top'].get_rect())
                elif platformType == 'round top':
                    self.image.blit(graphics.TILEDICT['castle round top'], graphics.TILEDICT['castle round top'].get_rect())
                elif platformType == 'right':
                    self.image.blit(graphics.TILEDICT['castle plat right'],graphics.TILEDICT['castle plat right'].get_rect())
                elif platformType == 'left':
                    self.image.blit(graphics.TILEDICT['castle plat left'], graphics.TILEDICT['castle plat left'].get_rect())
                elif platformType == 'top left':
                    self.image.blit(graphics.TILEDICT['castle top left'], graphics.TILEDICT['castle top left'].get_rect())
                elif platformType == 'top right':
                    self.image.blit(graphics.TILEDICT['castle top right'], graphics.TILEDICT['castle top right'].get_rect())
                else:
                    self.image.blit(graphics.TILEDICT['castle center'], graphics.TILEDICT['castle center'].get_rect())

        self.rect = self.image.get_rect()

class exit_door_sprite(pygame.sprite.Sprite):
    """ The exit sprite for the level """

    def __init__(self, width, height):
        """ Creates a sprite that, when the player collides with it, will
            prompt the user to exit. """

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(constants.BLUE)
        door = pygame.image.load('Graphics/Door.png')
        self.image.blit(door, door.get_rect())
        self.image.set_colorkey(constants.BLUE)
        self.rect = self.image.get_rect()

class pickupSprite(pygame.sprite.Sprite):

    def __init__(self, pickupType):

        super().__init__()

        self.image = pygame.image.load('Graphics/bag.png')
        self.rect = self.image.get_rect()
        self.type = pickupType