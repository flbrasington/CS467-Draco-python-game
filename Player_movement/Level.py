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
import player

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

    def __init__(self, numRow, numCol, level_width, level_height, player):
        # constructor for level class

        # http://tinysubversions.com/spelunkyGen/
        # 0 = a room that is not part of the solution path
        # 1 = room with exits left and right
        # 2 = room with exits left right and bottom with open top with blocks, or some way to jump up to room above
        # 3 = room with exits left right and
        # NOTE: room 2 and three ALWAYS have completely open tops with no walls.  This is because cells rely on the
        # opening of the cell, or the floor of the cell,  above it to filter the player to the next cell

        # save height and width of level
        self.level_height = level_height
        self.level_width = level_width

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
        self.current_room_x = 0
        self.current_room_y = random.randrange(0, self.num_cols)
        self.room_type[self.current_room_x][self.current_room_y] = 1

        # save end room location
        self.end_room = {'row': self.current_room_x, 'column': self.current_room_y}

        # boolean variable to see if we moved up to the next row due to hitting the edge of level
        # initially starts as true so that we don't immediately jump up if we start on an edge
        self.edge_row_jump = True
        done = False
        while not done:
            done = self.path()

        # for rows in self.room_type:
        #    print(rows)
        # --------------------------------------------------------------#

        # -----CONSTRUCTOR VARIABLES FOR SPRITES AND ROOM GENERATION----#
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.blocks_per_room_x = constants.ROOM_WIDTH
        self.blocks_per_room_y = constants.ROOM_HEIGHT
        self.block_width = self.room_side_length_x / self.blocks_per_room_x
        self.block_height = self.room_side_length_y / self.blocks_per_room_y
        self.player = player
        
        self.level_edge()
        self.create_room()
        # --------------------------------------------------------------#

        # for rows in self.room_type:
        #    print(rows)

        print(self.start_room)

        #-----SHIFT WORLD SO THAT STARTING VIEW IS ON PLAYER------------#
        self.world_shift_x = self.block_width + self.start_room['column'] * self.room_side_length_x
        self.world_shift_y = self.level_height - self.room_side_length_y + self.block_height
        print('shift x = ', self.world_shift_x)
        print('shift y = ', self.world_shift_y)
        #shift world to the left
        self.shift_world_x(-self.world_shift_x)
        #shift world up
        self.shift_world_y(-self.world_shift_y)


    def level_edge(self):

        # setting parameters for level edge
        # edges[0] = left edge
        # edges[1] = right edge
        # edges[2] = top edge
        # edges[3] = bottom edge
        edges = [[self.block_width, self.level_height + self.block_height * 2, 0, 0],
                 [self.block_width, self.level_height + self.block_height * 2, self.level_width + self.block_width, 0],
                 [self.level_width, self.block_height, self.block_width, 0],
                 [self.level_width, self.block_height, self.block_width, self.level_height + self.block_height]]

        for edge in edges:
            block = Platform(edge[0], edge[1])
            block.rect.x = edge[2]
            block.rect.y = edge[3]
            self.platform_list.add(block)

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
            # if we are at top of level and attempt to go up again, we will have found our end room.  In this
            # we save the parameter and exit the loop
            if self.current_room_x > 4:
                self.room_type[self.current_room_x - 1][self.current_room_y] = 2
                self.start_room['row'] = self.current_room_x - 1
                self.start_room['column'] = self.current_room_y
                return True
            self.room_type[self.current_room_x][self.current_room_y] = 2
            # this is set to true so that we don't continue jumping up the side of the level
            self.edge_row_jump = True

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

        # if random number is 5 then we are moving down
        elif path_direction is 5:
            self.edge_row_jump = False
            self.room_type[self.current_room_x][self.current_room_y] = 3
            # print cell to screen
            self.current_room_x += 1
            # if we are at top of level and attempt to go up again, we will have found our end room.  In this
            # we save the parameter and exit the loop
            if self.current_room_x > 4:
                self.room_type[self.current_room_x - 1][self.current_room_y] = 2
                self.start_room['row'] = self.current_room_x - 1
                print('start room x =', self.current_room_x - 1)
                self.start_room['column'] = self.current_room_y
                return True
            self.room_type[self.current_room_x][self.current_room_y] = 2

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
                        block = Platform(self.block_width, self.block_height)
                        block.rect.x = self.block_width + (pos % 5) * self.room_side_length_x + x * self.block_width
                        block.rect.y = self.block_height + (pos // 5) * self.room_side_length_y + y * self.block_height
                        block.player = self.player
                        self.platform_list.add(block)
                    elif rooms[pos][y][x] is 5:
                        prob_block_5_list.append([pos, y, x])
                    elif rooms[pos][y][x] is 6:
                        prob_block_6_list.append([pos, y, x])
        # fill probability blocks depending on if it is a floor block (6) or a block in the air (5)
        # second parameter is used to import the correct block template
        self.fill_prob_block(prob_block_5_list, 5)
        self.fill_prob_block(prob_block_6_list, 6)

    def fill_prob_block(self, prob_block_list, block_type):
        for p_block in prob_block_list:
            prob_block = self.import_template(block_type)
            # height of a probability block
            for y in range(3):
                # width of a probability block
                for x in range(5):
                    if prob_block[y][x] is 1:
                        block = Platform(self.block_width, self.block_height)
                        block.rect.x = (p_block[0] % 5) * self.room_side_length_x + (p_block[2] + x) * self.block_width
                        block.rect.y = (p_block[0] // 5) * self.room_side_length_y + (
                                                                                     p_block[1] + y) * self.block_height
                        self.platform_list.add(block)

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

    def draw_screen_path(self, screen):
        """Print path to screen
        NOTE:  You must pass in the output destination
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

        #this shifts the rope_object as needed
        self.player.rope_object.rect.x += shift_x
        self.player.rope_object.rope_end_x += shift_x

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

        #this shifts the rope_object as needed
        self.player.rope_object.rect.y += shift_y
        self.player.rope_object.rope_end_y += shift_y

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(constants.WHITE)
        screen.blit(constants.TILEDICT['ice block wall'], constants.TILEDICT['ice block wall'].get_rect())

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(constants.GREEN)
        self.image.blit(constants.TILEDICT['tundra center'], constants.TILEDICT['tundra center'].get_rect())

        self.rect = self.image.get_rect()


# Function Main
def main():
    # this initializes pygame
    pygame.init()

    # this sets up the screen size for the user using the sizes defined in constants
    screen_size = [constants.SCREEN_WIDTH + constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT + constants.SCREEN_HEIGHT//2]
    screen = pygame.display.set_mode(screen_size)

    # this is the caption for the window
    pygame.display.set_caption("Climbing Game")

    # this time function is used to manage the frames per second
    clock = pygame.time.Clock()

    # this bit of code sets up the players for the game
    p = player.Player()

    # this bit create's the level for the program
    level_list = []
    level_list.append(Level(5, 5, constants.SCREEN_WIDTH * 5, constants.SCREEN_HEIGHT * 5, p))

    # set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    # List to hold all the sprites
    all_sprite_list = pygame.sprite.Group()
    p.level = current_level
    p.rope_object.level = current_level
    print(current_level.start_room['column'])
    p.rect.x = 0
    p.rect.y = constants.SCREEN_HEIGHT - p.rect.height - current_level.block_height
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(p)
    active_sprite_list.add(p.rope_object)

    # this is the heart of the main program.
    # currently the program runs on a loop until the python sheet is closed.
    done = False
    while not done:
        # for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        done = True
        # this updates the the display
        screen.fill(constants.WHITE)
        current_level.draw(screen)
        active_sprite_list.update()

        # If the player gets near the right side, shift the world left (-x)

        if p.rect.right >= 500:
            diff = p.rect.right - 500
            p.rect.right = 500
            current_level.shift_world_x(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if p.rect.left <= 300:
            diff = 300 - p.rect.left
            p.rect.left = 300
            current_level.shift_world_x(diff)

        # If the player gets near the bottom, shift the world up (-x)
        if p.rect.bottom >= 550:
            diff = p.rect.bottom - 550
            p.rect.bottom = 550
            current_level.shift_world_y(-diff)

        # If the player gets near the top, shift the world down (+x)
        if p.rect.top <= 150:
            diff = 150 - p.rect.top
            p.rect.top = 150
            current_level.shift_world_y(diff)

        active_sprite_list.draw(screen)
        # p.update()
        # pygame.draw.rect(screen, constants.BLACK, [p.lead_x, p.lead_y, 10,10])

        pygame.display.update()

        # this is for controlling the Frames per Second
        clock.tick(FPS)


# Call the main function, start up the game
if __name__ == "__main__":
    main()
