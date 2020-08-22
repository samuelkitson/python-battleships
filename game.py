# ******************************************************
#
# The Game module provides game functionality
#
# ******************************************************

import variables, gui

# Displays the tutorial popup window
def show_tutorial(init_page=0):
    variables.tutorial_window = gui.Tutorial(init_page)


#
# Use this class to create a new Game instance
#
class Game():
    # New game
    def __init__(self):
        self.init_ships_available()
        self.init_variables()
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
        variables.ship_placement_window = gui.ShipPlacement(lambda:print("Ships placed"))

    # Init the game variables, such as the grids
    def init_variables(self):
        variables.grid_player1 = create_game_grid(variables.rows_number, variables.columns_number)
        variables.ships_player1 = create_ships_list()
        variables.grid_player2 = create_game_grid(variables.rows_number, variables.columns_number)
        variables.ships_player2 = create_ships_list()

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
    blank_cell = {"s":"e", "i":None, "t":None}
    """blank_column = [blank_cell.copy()] * columns
    grid = [blank_column] * rows"""
    grid = []
    for row in range(0, rows):
        grid.append([])
        for col in range(0, columns):
            cell = blank_cell.copy()
            grid[-1].append(cell)
    return grid

# Create an empty ship layout list to store ship positions and states for a player
def create_ships_list():
    output = []
    for ship in variables.ships_available:
        ship_dict = {}
        ship_dict["name"] = ship.name
        ship_dict["spaces"] = ship.spaces
        # During ship placement: unplaced, placed, active, review (same as active, but after placement), error
        # During play: normal, hit, sunk
        ship_dict["state"] = "unplaced"
        # Coordinates are placed in an array, with the (0-indexed) row number first, then the column number after
        # For example, location B5 would be recorded as [1, 4]
        ship_dict["locations"] = [[0,0]]*ship.spaces
        output.append(ship_dict)
    return output