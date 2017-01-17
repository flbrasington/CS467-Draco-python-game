import pygame
import random

random.seed()

WHITE = (255, 255, 255)
BLUE = (50, 50, 255)

# set height and width of window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class Level:
    """This class will create procedurally generated levels including
    a path of cells from entrance to exit and random cells"""

    def __init__(self, numRow, numCol, screen_width, screen_height):
        #constructor for level class

        #http://tinysubversions.com/spelunkyGen/
        #0 = a room that is not part of the solution path
        #1 = room with exits left and right
        #2 = room with exits left right and bottom
        #3 = room with exits left right and top
        #NOTE: room 2 and three ALWAYS have completely open tops with no walls.  This is because cells rely on the
        #opening of the cell, or the floor of the cell,  above it to filter the player to the next cell

        #create 2-d array and fill with 0's
        self.room_type = [[0]*numCol for _ in range(numRow)]
        #save number of rows and columns (cell grid) of level
        self.num_rows = numRow
        self.num_cols = numCol
        #the cell_side_length is how big each cell in the level is going to be
        self.cell_side_length_x = screen_width/numCol
        self.cell_side_length_y = screen_height/numRow
        #variables to keep track of start and end rooms
        self.end_room = {'row': None, 'column': None}

        #------RANDOMLY GENERATE ENTRANCE CELL AT BOTTOM OF LEVEL------#
        self.current_room_x = 4
        self.current_room_y = random.randrange(0, self.num_cols)
        self.room_type[self.current_room_x][self.current_room_y] = 1

        # save start room location
        self.start_room = {'row': self.current_room_x, 'column': self.current_room_y}

        # variable to keep track of randomized path direction
        path_direction = None

        # boolean variable to see if we moved up to the next row due to hitting the edge of level
        # initially starts as true so that we don't immediately jump up if we start on an edge
        self.edge_row_jump = True
        #--------------------------------------------------------------#

        #just a check to make sure algorithm is behaving correctly
        for row in self.room_type:
            print(row)



    def path(self):
        """Create a path through level"""

        path_direction = random.randrange(1, 6)
        print(path_direction)

        #if current room is on the edge of the level (column 0 or column 4 and we did not jump to that room
        #because of hitting an edge in the previous assignment, assign the current room to be of type 2 and the
        #new room above it to be of type 3 so that the rooms connect
        if (self.current_room_y == 0 or self.current_room_y == 4) and self.edge_row_jump == False:
            self.room_type[self.current_room_x][self.current_room_y] = 2
            self.current_room_x -= 1
            self.room_type[self.current_room_x][self.current_room_y] = 3

            # if we are at top of level and attempt to go up again, we will have found our end room.  In this
            # we save the parameter and exit the loop
            if self.current_room_x < 0:
                self.end_room['row'] = self.current_room_x + 1
                self.end_room['column'] = self.current_room_y
                return True
            #this is set to true so that we don't continue jumping up the side of the level
            self.edge_row_jump = True

        # if random number is 1 or 2 we move the path left and give that new room left/right exits
        elif path_direction == 1 or path_direction == 2:

            #if we are on the left edge of level then we shouldn't move left any further
            #if cell we are moving to has already been assigned then we should not move there either
            if self.current_room_y > 0  and self.room_type[self.current_room_x][self.current_room_y - 1] == 0:
                # we now have a new direction without jumping rows because of hitting an edge
                self.edge_row_jump = False
                #move current room to the left
                self.current_room_y -= 1
                #assign that room with a left/right exit
                self.room_type[self.current_room_x][self.current_room_y] = 1

        #if random number is 3 or 4 we move right and give that new room left/right exits
        elif path_direction == 3 or path_direction == 4:
            #check if the room we are moving to has already been assigned or is off the screen
            if self.current_room_y < 4  and self.room_type[self.current_room_x][self.current_room_y + 1] == 0:
                # we now have a new direction without jumping rows because of hitting an edge
                self.edge_row_jump = False
                #move current room to the right
                self.current_room_y += 1
                # assign that room with a left/right exit
                self.room_type[self.current_room_x][self.current_room_y] = 1

        #if random number is 5 then we are moving up
        elif path_direction == 5:
            self.edge_row_jump = False
            self.room_type[self.current_room_x][self.current_room_y] = 2
            # print cell to screen
            self.current_room_x -= 1
            self.room_type[self.current_room_x][self.current_room_y] = 3
            #if we are at top of level and attempt to go up again, we will have found our end room.  In this
            #we save the parameter and exit the loop
            if self.current_room_x < 0:
                self.end_room['row'] = self.current_room_x + 1
                self.end_room['column'] = self.current_room_y
                return True

        #print array to see if movements are correct
        for row in self.room_type:
            print(row)
        return False



    def draw_screen(self, screen):
        """Print path to screen
        NOTE:  You must pass in the output destination
        """
        screen.fill(WHITE)
        for x in range(self.num_cols):
            for y in range(self.num_rows):
                #if a room is on the path then color the cell blue on the screen
                if self.room_type[x][y] != 0:
                    # NOTE: we are multiplying current_room.y and cell_side_length.x because cell_side_length refers to the x and
                    # y axis as pygame.draw uses it, while current_room.x or y refers to the row major array that python uses
                    # for 2-d arrays. the location of the top left corner of the rectangle we are going to draw is the y array
                    # value multiplied by the x row number (I know this is disorienting)
                    pygame.draw.rect(screen, BLUE, [y * self.cell_side_length_x,
                                                    x * self.cell_side_length_y,
                                                    self.cell_side_length_x - 10,
                                                    self.cell_side_length_y - 10], 0)



def main():
    #Call this function so the pygame library can initialize itself
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    #Set the title of the window
    pygame.display.set_caption("Level Path Algorithm")

    #Loop until the user clicks the close button
    done = False
    clock = pygame.time.Clock()
    level = Level(5, 5, SCREEN_WIDTH, SCREEN_HEIGHT)

    #-----MAIN PROGRAM LOOP-----#
    while not done:

        #ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        #ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        #ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT

        done = level.path()

        #ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        #ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT

        #clear the screen and set the screen background

        if not done:
            level.draw_screen(screen)


        #ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        #update the screen with what has been drawn
        pygame.display.flip()

        #limits the loop to 60 times per second
        clock.tick(4)

    pygame.quit()

#Call the main function, start up the game
if __name__ == "__main__":
    main()