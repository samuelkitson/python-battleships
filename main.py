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

#Class for the game setup screen
class Game_Setup:
    #Construst the class and create the GUI
    def __init__(self, gameCallback):
        self.gameCallback = gameCallback
        self.ShowWindow()

    #Show the login window
    def ShowWindow(self):
        #Initialise the game setup window
        self.authenticateGui = gui.Game_Setup(self.gameCallback)

def Start2():
    tutorialWindow.Close()
    gui.Game_Setup(lambda: print("Starting game"))

#Called to start the game
def Start():
    global tutorialWindow
    #Init variables
    variables.init()
    #Create the window
    variables.window = gui.Window()
    #Authenticate
    #game_setup_object = Game_Setup(lambda: print("Starting game"))
    #gui.Game_Setup(lambda: print("Starting game"))
    tutorialWindow = gui.Tutorial(Start2)


if __name__ == "__main__":
    #Start the game
    Start()
    #Start the GUI infinite loop
    variables.window.window.mainloop()

