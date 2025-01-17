# ******************************************************
#
# The Game module provides game functionality
#
# ******************************************************

import variables, gui, ai

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
        #self.start_game_view() # temporary
    
    # Displays the game setup window, shown at the start of the game
    # Called when the Game object is initialised when the program loads
    def show_game_setup(self):
        variables.window.clear_frame()
        variables.game_setup_window = gui.GameSetup(show_tutorial, self.save_game_setup)

    # Store the options selected on the game setup screen, and init computer players as necessary
    # Called from the start game button on the setup window
    def save_game_setup(self):
        self.difficulty = variables.game_setup_window.game_difficulty.get()
        self.player_mode = variables.game_setup_window.player_number_value.get()
        # Check that the selected options are valid
        if not self.player_mode == 1:
            gui.messagebox.showinfo("Coming soon", "2 player mode is coming soon!\nFor now, please select single player mode to play against the computer")
            return
        if not self.difficulty == "Medium":
            gui.messagebox.showinfo("Coming soon", "Difficulty levels are coming soon!\nFor now, please select Medium difficulty")
            return
        # Init any computer players
        if self.player_mode == 1:
            self.computer = ai.Player(self.difficulty, 1)
        self.start_ship_placement()


    # After the game setup screen, show the ship placement screen
    # Called from the start game button on the setup window
    def start_ship_placement(self):
        variables.window.clear_frame()
        variables.ship_placement_window = gui.ShipPlacement(self.start_game_view)

    # After the ships have been placed, start the game and show the GameView screen
    # Called from the start game button on the ship placement screen
    def start_game_view(self):
        print(variables.player_ships[0])
        variables.window.clear_frame()
        variables.game_view_window = gui.GameView(lambda:print("Game finished"))

    # Init the game variables, such as the grids
    def init_variables(self):
        variables.player_grids[0] = create_game_grid(variables.rows_number, variables.columns_number)
        variables.player_ships[0] = create_ships_list()
        variables.player_grids[1] = create_game_grid(variables.rows_number, variables.columns_number)
        variables.player_ships[1] = create_ships_list()

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
        ship_dict["direction"] = ""
        output.append(ship_dict)
    return output