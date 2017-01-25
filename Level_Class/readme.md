Changes:

1) The view is now more zoomed in.  This was accomplished by taking the level view (800x600) and multiplying by five so that the view is the size of one room.  Changes were made to the constructor and the parameters for calling the Level constructor (the parameters now take the total level size instead of the screen size  
2) An outer edge was added around the whole level so that the player cannot fall off of the map (level_edge function in the Level class.  This also made it so that I had to change the equation for where to put platforms given the new edge width)
3) The screen follows the player as they move around the level (shift_world_x function and shift_world_y function)

Issues:

1) The start screen does not seem to start on first room of the level unless the room is in column 0.  This could be due to the constructor or the some interplay between the contructor, where the player is being placed and the shift world functions
