# ******************************************************
#
# The Variables module provides global variables and functions
#
# ******************************************************

# Game options
rows_number = 10
columns_number = 10

# Image files to load
images_to_load = [
  "images/boat_middle_grey.png",
  "images/boat_end_grey.png",
  "images/boat_middle_yellow.png",
  "images/boat_end_yellow.png",
  "images/boat_middle_green.png",
  "images/boat_end_green.png"
]
loaded_images = {}
# Naming convention: eg "boat_e_g_u" meaning boat end part, grey, pointing up
photo_images = {}

def number_to_letter(number):
  # Assuming 1-indexed
  return chr(ord('@')+number)
def letter_to_number(letter):
  return ord(letter)-64

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

# Grid format:
# Each cell has a dictionary, with keys:
# s (state): a (active, in placement), e (empty), n (normal, ship placed but not hit), h (hit), s (sunk)
# i (ship index): 0-length of ships list, or None
# t (type, the image code): eg, "boat_e_y_u", or None

grid_player1 = [] # Grid belonging to player 1
grid_player2 = [] # Grid belonging to player 2, usually the computer
ships_player1 = [] # Ships belonging to player 1
ships_player2 = [] # Ships belonging to player 2, usually the computer
difficulty_levels = ("Easy", "Medium", "Hard")
game_difficulty =  None
ships_available = []

# GUI styling variables
title_colour = "#000000"
title_font = ("Helvetica", 20, "bold")
subtitle_colour = "#555555"
subtitle_font = ("Helvetica", 14, "bold")
monospace_font = ("Courier", 12, "bold")