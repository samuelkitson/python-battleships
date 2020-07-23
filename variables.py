# ******************************************************
#
# The Variables module provides global variables and functions
#
# ******************************************************

# Game options
rows_number = 10
columns_number = 10

# Size of grid buttons in pixels
grid_image_width = 35
grid_image_height = 35

# Create variables to store windows instances
window = None
tutorial_window = None
game_setup_window = None
ship_placement_window = None
game = None

# Game variables
# 1st layer is the row (A-J), 2nd layer is the column (1-10)
# eg, space C5 would be stored at grid[2][4]
grid_player1 = [] # Ships belonging to player 1
grid_player2 = [] # Ships belonging to player 2, usually the computer
difficulty_levels = ("Easy", "Medium", "Hard")
game_difficulty =  None

# GUI styling variables
title_colour = "#000000"
title_font = ("Helvetica", 20, "bold")
subtitle_colour = "#555555"
subtitle_font = ("Helvetica", 14, "bold")
monospace_font = ("Courier", 12, "bold")