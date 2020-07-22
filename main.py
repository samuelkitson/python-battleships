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

def start2():
    #variables.tutorial_window.close()
    gui.Game_Setup(show_tutorial, lambda: variables.tutorial_window.close())

# Called to start the game
def start_program():
    # Init variables
    #variables.init()
    # Create the base window that will host the game
    variables.window = gui.Window()
    #variables.tutorial_window = gui.Tutorial(start2)
    start2()


if __name__ == "__main__":
    # Start the game
    start_program()
    # Start the GUI infinite loop
    variables.window.window.mainloop()

