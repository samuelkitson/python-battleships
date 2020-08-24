# ******************************************************
#
# The ai module provides the computer's ability to play
#
# ******************************************************

import variables, gui
from random import randrange

#
# Use this class to create a new computer player instance
#
class Player:
    # Init the class
    def __init__(self, difficulty, player_num):
        # The higher the difficultly, the better the computer will play
        self.skill = difficulty
        # The index of this player, used to get the correct objects from the grid and ship lists
        self.player_num = player_num
        # Get the player grid and ship list variables
        self.grid = variables.player_grids[player_num]
        self.ships = variables.player_ships[player_num]
        # Place the ships
        self.place_ships()
    
    # Place ships in the grid
    def place_ships(self):
        filled_locations = []
        # Iterate through the list of ships, placing each one in turn and starting with the largest
        ship_num = 0
        for ship in self.ships:
            # Set to true when all ship parts are in valid locations
            ship_placed = False
            # While not placed properly
            while not ship_placed:
                # Set to true if any ship part has an invalid location
                invalid_loc = False
                # Stores list of positions for this ship's parts
                ship_locs = []
                # Random vertical or horizontal
                if randrange(2) == 0:
                    direction = "h"
                else:
                    direction = "v"
                # Choose a start position
                if direction == "h":
                    start_row_num = randrange(0, variables.rows_number)
                    start_col_num = randrange(0, variables.columns_number-ship["spaces"]+1)
                else:
                    start_row_num = randrange(0, variables.rows_number-ship["spaces"]+1)
                    start_col_num = randrange(0, variables.columns_number)
                # Place all parts of the ship
                for part_num in range(0, ship["spaces"]):
                    if direction == "h":
                        ship_locs.append([start_row_num, start_col_num+part_num])
                    else:
                        ship_locs.append([start_row_num+part_num, start_col_num])
                    # Check that the position is not already occupied
                    if ship_locs[-1] in filled_locations:
                        invalid_loc = True
                        break
                # Move to next ship if placed in a valid location
                if not invalid_loc:
                    ship_placed = True
            # Update variables with new filled locations
            filled_locations.extend(ship_locs)
            # Edit ships list
            variables.player_ships[self.player_num][ship_num]["state"] = "placed"
            variables.player_ships[self.player_num][ship_num]["direction"] = direction
            variables.player_ships[self.player_num][ship_num]["locations"] = ship_locs
            # Next ship
            ship_num += 1
        # Calculate the grid images
        gui.calculate_images(self.player_num, "g", True)