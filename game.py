# ******************************************************
#
# The Game module provides game functionality
#
# ******************************************************

import variables, gui

# Empty ship class used to create ship instaces
class Ship():
    # Init the ship instance
    def __init__(self, name, spaces):
        self.name = name
        self.spaces = spaces

# Create an empty game grid and store in a 2D array
def create_game_grid(rows, columns):
    blank_column = [""] * columns
    grid = [blank_column] * rows
    return grid

# Init the game variables, such as the grids
def init_variables():
    variables.grid_player1 = create_game_grid(10, 10)
    variables.grid_player2 = create_game_grid(10, 10)