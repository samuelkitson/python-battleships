# ******************************************************
#
# Battleships
# This is the main file that must be run to start the game
# Note that all other python files in this directory must be accessible
#
# To build .exe use
# pyinstaller -w -F -y main.py
# ******************************************************

#Import libraries
import gui, variables
import time

if __name__ == "__main__":
    variables.app = gui.Game_Window()
    variables.app.mainloop()