# ******************************************************
#
# BATTLESHIPS
#
# This is the main file that must be run to start the game
# Note that all other python files in this directory must be accessible
#
# To build .exe use
# pyinstaller -w -F -y main.py
#
# ******************************************************

# Import libraries
import gui, variables
import time

def show_tutorial():
    variables.tutorial_window = gui.Tutorial()

# Called to start the game
def start_program():
    # Create the base window that will host the game
    variables.window = gui.Window()
    variables.game_setup_window = gui.GameSetup(show_tutorial)


if __name__ == "__main__":
    # Start the game
    start_program()
    # Start the GUI infinite loop
    variables.window.mainloop()

