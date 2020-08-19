# ******************************************************
#
# The Game module provides game functionality
#
# ******************************************************

import variables, gui

# Displays the tutorial popup window
def show_tutorial():
    variables.tutorial_window = gui.Tutorial()


#
# Use this class to create a new Game instance
#
class Game():
    # New game
    def __init__(self):
        self.init_variables()
        self.init_ships_available()
        self.show_game_setup()
    
    # Displays the game setup window, shown at the start of the game
    # Called when the Game object is initialised when the program loads
    def show_game_setup(self):
        variables.window.clear_frame()
        variables.game_setup_window = gui.GameSetup(show_tutorial, self.start_ship_placement)

    # After the game setup screen, show the ship placement screen
    # Called from the start game button on the setup window
    def start_ship_placement(self):
        variables.window.clear_frame()
        variables.ship_placement_window = gui.ShipPlacement(lambda: print("Ships placed"))

    # Init the game variables, such as the grids
    def init_variables(self):
        variables.grid_player1 = create_game_grid(variables.rows_number, variables.columns_number)
        variables.grid_player2 = create_game_grid(variables.rows_number, variables.columns_number)

    # Populate variables.ships_available
    def init_ships_available(self):
        # Edit this to change ships
        variables.ships_available.append(Ship("Carrier", 5))
        variables.ships_available.append(Ship("Battleship", 4))
        variables.ships_available.append(Ship("Destroyer", 3))
        variables.ships_available.append(Ship("Submarine", 3))
        variables.ships_available.append(Ship("Patrol Boat", 2))


#
# Empty ship class used to create ship instaces
#
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