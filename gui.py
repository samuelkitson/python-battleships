# ******************************************************
#
# The GUI module provides classes for the user interfaces
#
# ******************************************************

#Import libraries
import variables

"""try:
    import Tkinter as tk
except:
    import tkinter as tk"""

from tkinter import *


#
# The Window class provides the overall GUI window
#
class Window:
    #Construct the window
    def __init__(self):
        self.window = Tk()
        self.window.title("Battleships")

    def CloseGUI(self):
        self.window.destroy()

class Tutorial():
    #Construct the GUI
    def __init__(self, returnCallback):
        #Assign local variables
        self.width = 1500
        self.height = 800
        self.colour = "floral white"
        self.fontTitle = ("verdana", 20)
        self.font = ("verdana", 13)
        self.label = ("verdana", 8)

        self.returnCallback = returnCallback

        #Create canvas & window
        self.canvas = Canvas(variables.window.window, bg=self.colour, height=self.height, width=self.width)
        self.canvas.grid()

        label = Label(self.canvas, text="Tutorial", font=self.fontTitle, bg=self.colour)
        label.grid(row=1, columnspan=2)
        label = Label(self.canvas, text="Welcome to Battleships: Python Edition", font=self.font, bg=self.colour)
        label.grid(row=2, columnspan=2)
        self.loginButton = Button(self.canvas, text="Done", command=self.returnCallback)
        self.loginButton.grid(row=3, columnspan=1)

    #Closes the window
    def Close(self):
        self.canvas.destroy()
        del self


class Game_Setup:
    #Construct the GUI
    def __init__(self, loginCallback):
        #Assign local variables
        self.width = 500
        self.height = 500
        self.colour = "floral white"
        self.fontTitle = ("verdana", 20)
        self.font = ("verdana", 13)
        self.label = ("verdana", 8)

        self.loginCallback = lambda: print("Login:")
        self.registerCallback = lambda: print("Register user")

        #Create canvas & window
        self.canvas = Canvas(variables.window.window, bg=self.colour, height=self.height, width=self.width)
        self.canvas.grid()

        label = Label(self.canvas, text="Music Quiz Game", font=self.fontTitle, bg=self.colour)
        label.grid(row=1, columnspan=2)
        label = Label(self.canvas, text="Welcome to the music quiz!", font=self.font, bg=self.colour)
        label.grid(row=2, columnspan=2)
        
        self.statusLabel = Label(self.canvas, text="Please authenticate to continue", font=self.label, bg=self.colour, width=40)
        self.statusLabel.grid(row=3, columnspan=2)

        line = Frame(self.canvas, height=1, width=200, bg="grey")
        line.grid(row=4, columnspan=2, pady=10)

        self.loginFrame = Frame(self.canvas, bg=self.colour)
        self.loginFrame.grid(row=5, columnspan=2)

        self.SetUpLogin()
        
    #Called when the login button is pressed on the login screen - attempts login
    def Login_LoginButtonPressed(self):
        self.loginCallback(self.username.get(), self.password.get())

    #Called when the register button is pressed on the register screen - sets up the registration window
    def Login_RegisterButtonPressed(self):
        self.SetUpRegister()

    #Called if the password entered was invalid - notifies the user
    def InvalidPassword(self):
        self.username.set("")
        self.password.set("")

        self.statusLabel.config(text="Invalid credentials - please try again")
        self.statusLabel.config(fg="red")

    #Called if the account was not authorised - notifies the user
    def AccountNotAuthorised(self):
        self.password.set("")

        self.statusLabel.config(text="Your account has not been authorised")
        self.statusLabel.config(fg="red")

    #Sets up the login window
    def SetUpLogin(self):
        self.ClearLoginFrame()

        self.statusLabel.config(text="Please authenticate to continue")
        self.statusLabel.config(fg="black")

        self.username = StringVar()
        self.password = StringVar()

        label = Label(self.loginFrame, text="Username", font=self.label, bg=self.colour)
        self.fieldUsername = Entry(self.loginFrame, textvariable=self.username)
        self.fieldUsername.focus()

        label.grid(row=1, column=0, sticky=E)
        self.fieldUsername.grid(row=1, column=1, sticky=W)

        label = Label(self.loginFrame, text="Password", font=self.label, bg=self.colour)
        self.fieldPassword = Entry(self.loginFrame, textvariable=self.password, show="*")

        label.grid(row=2, column=0, sticky=E)
        self.fieldPassword.grid(row=2, column=1, sticky=W)

        buttonFrame = Frame(self.loginFrame, bg=self.colour)
        buttonFrame.grid(row=3, columnspan=2, pady=5)

        
        self.loginButton = Button(buttonFrame, text="Login", command=self.Login_LoginButtonPressed)
        self.registerButton = Button(buttonFrame, text="Register", command=self.Login_RegisterButtonPressed)

        self.loginButton.grid(row=0, column=0)
        self.registerButton.grid(row=0, column=1)

    #Called when the login button is pressed in the register window
    def Register_LoginButtonPressed(self):
        self.SetUpLogin()

    #Called when the register button is pressed in the register window
    def Register_RegisterButtonPressed(self):
        self.registerCallback(self.username.get(), self.password.get(), self.password2.get())

    #Sets up the registration window
    def SetUpRegister(self):
        self.ClearLoginFrame()

        self.statusLabel.config(text="Register an account")
        self.statusLabel.config(fg="black")

        self.username = StringVar()
        self.password = StringVar()
        self.password2 = StringVar()

        label = Label(self.loginFrame, text="Username", font=self.label, bg=self.colour)
        self.fieldUsername = Entry(self.loginFrame, textvariable=self.username)
        self.fieldUsername.focus()

        label.grid(row=1, column=0, sticky=E)
        self.fieldUsername.grid(row=1, column=1, sticky=W)

        label = Label(self.loginFrame, text="Password", font=self.label, bg=self.colour)
        self.fieldPassword = Entry(self.loginFrame, textvariable=self.password, show="*")

        label.grid(row=2, column=0, sticky=E)
        self.fieldPassword.grid(row=2, column=1, sticky=W)

        label = Label(self.loginFrame, text="Confirm Password", font=self.label, bg=self.colour)
        self.fieldPassword2 = Entry(self.loginFrame, textvariable=self.password2, show="*")

        label.grid(row=3, column=0, sticky=E)
        self.fieldPassword2.grid(row=3, column=1, sticky=W)

        buttonFrame = Frame(self.loginFrame, bg=self.colour)
        buttonFrame.grid(row=4, columnspan=2, pady=5)

        
        self.registerButton = Button(buttonFrame, text="Register", command=self.Register_RegisterButtonPressed)
        self.loginButton = Button(buttonFrame, text="Login", command=self.Register_LoginButtonPressed)

        self.registerButton.grid(row=0, column=0)
        self.loginButton.grid(row=0, column=1)

    #Called if there were errors in the registration data - notifies the user
    def InvalidRegistration(self, message):
        self.password.set("")
        self.password2.set("")

        self.statusLabel.config(text=message)
        self.statusLabel.config(fg="red")

    #Sets up the registration confirmation window
    def SetUpRegisterConfirm(self):
        self.ClearLoginFrame()
        
        self.statusLabel.config(text="Registration successful")
        self.statusLabel.config(fg="black")

        label = Label(self.loginFrame, text="Please wait for your account to be validated", font=self.label, bg=self.colour)
        label.grid(row=0, column=0, sticky=E)

        buttonFrame = Frame(self.loginFrame, bg=self.colour)
        buttonFrame.grid(row=4, columnspan=2, pady=5)

        self.loginButton = Button(buttonFrame, text="Login", command=self.Register_LoginButtonPressed)
        self.loginButton.grid(row=1, column=1, columnspan=2)

    #Clears the login frame
    def ClearLoginFrame(self):
        children = self.loginFrame.winfo_children()
        for child in children:
            child.destroy()

    #Closes the authenticator window
    def Close(self):
        self.canvas.destroy()
        del self