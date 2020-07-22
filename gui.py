# ******************************************************
#
# The GUI module provides classes for the user interfaces
#
# ******************************************************

# Import libraries
import variables
try:
    import Tkinter as tk
    from Tkinter import N, E, S, W, NE, SE, SW, NW, END
except:
    import tkinter as tk
    from tkinter import N, E, S, W, NE, SE, SW, NW, END



#
# The Window class provides the overall GUI window
#
class Window:
    #Construct the window
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Battleships")

    def close(self):
        self.window.destroy()


#
# The PopupWindow class extends the tk.Toplevel class, and provides custom methods and default variables
# Use self.contents as the master for any widgets inside the window
#
class PopupWindow(tk.Toplevel):
    def __init__(self, init_frame=True):
        # Init the tk.Toplevel superclass
        super().__init__()
        # Block interaction to the parent window
        self.grab_set()
        # Set a default size and prevent resizing
        self.geometry("400x350")
        self.resizable(False, False)
        # Set up the grid and tk.Frame for the window contents
        if (init_frame):
            # Creates an empty row and column around a central Frame widget to centre it in the window
            self.rowconfigure(0, weight=1)
            self.columnconfigure(0, weight=1)
            self.rowconfigure(2, weight=1)
            self.columnconfigure(2, weight=1)
            self.contents = tk.Frame(self)
            self.contents.grid(row=1, column=1)

    # Call the .close() method to destroy the popup window
    # This will also release control and allow interaction on the parent window
    def close(self):
        self.destroy()
        del self


#
# The Tutorial class provides the popup tutorial window, using the custom PopupWindow class
#
class Tutorial(PopupWindow):
    # Construct the GUI
    def __init__(self):
        super().__init__()

        #self.resizable(True, True)
        #self.contents.config(bg="salmon")
        
        self.title = tk.Label(self.contents, text="Tutorial", fg=variables.title_colour, font=variables.title_font)
        self.title.grid(row=0, column=0, pady=(0,10), columnspan=2)
        self.text = tk.Text(self.contents, wrap=tk.WORD)
        self.text.grid(row=1, column=0, columnspan=2)
        self.text.config(bg="white", height=13, width=35, state="disabled")

        # Set up tags for custom text styles
        self.text.tag_configure("bold", font=("Helvetica", 10, "bold"))
        self.text.tag_configure("regular", font=("Helvetica", 10))

        self.write_text("Load tutorial, please wait...", ("bold"))

        self.left_button = tk.Button(self.contents, text="◀ Previous page", command=self.previous_page)
        self.left_button.config(width=14)
        self.left_button.grid(row=2, column=0, pady=(5,10))

        self.right_button = tk.Button(self.contents, text="Next page ▶", command=self.next_page)
        self.right_button.config(width=14)
        self.right_button.grid(row=2, column=1, pady=(5,10))

        self.exit_button = tk.Button(self.contents, text="Back to the game", command=self.close)
        self.exit_button.grid(row=3, column=0, columnspan=2)
        
        self.load_tutorial_file()

    # Loads the tutorial.txt into the self.tutorial_text array, split by page
    def load_tutorial_file(self):
        try:
            with open("tutorial.txt", 'r') as tutorial_file:
                self.tutorial_pages = tutorial_file.read().split("###PAGEBREAK###")
        except FileNotFoundError:
            self.tutorial_pages = ["Error: tutorial.txt file not found"]
        finally:
            self.page_number = 0
            self.write_page()
            

    # Writes text to the Text widget
    def write_text(self, text, tags=("regular")):
        self.text.config(state="normal")
        self.text.insert(END, text, tags)
        self.text.config(state="disabled")

    # Clears the Text widget
    def clear_text(self):
        self.text.config(state="normal")
        self.text.delete(1.0, END)
        self.text.config(state="disabled")

    # Navigates between pages
    def previous_page(self):
        if (self.page_number > 0):
            self.page_number -= 1
            self.write_page()
    def next_page(self):
        if (self.page_number < len(self.tutorial_pages) - 1):
            self.page_number += 1
            self.write_page()

    # Prints the current page
    def write_page(self):
        self.clear_text()
        self.write_text(self.tutorial_pages[self.page_number].strip())

    # Closes the window
    def close(self):
        self.destroy()
        del self


class Game_Setup:
    #Construct the GUI
    def __init__(self, show_tutorial_callback, close_tutorial_callback):
        #Assign local variables
        self.width = 500
        self.height = 500
        self.colour = "floral white"
        self.fontTitle = ("verdana", 20)
        self.font = ("verdana", 13)
        self.label = ("verdana", 8)

        self.loginCallback = lambda: print("Login:")
        self.registerCallback = lambda: print("Register user")
        self.show_tutorial_callback = show_tutorial_callback
        self.close_tutorial_callback = close_tutorial_callback

        #Create canvas & window
        self.canvas = tk.Canvas(variables.window.window, bg=self.colour, height=self.height, width=self.width)
        self.canvas.grid()

        label = tk.Label(self.canvas, text="Music Quiz Game", font=self.fontTitle, bg=self.colour)
        label.grid(row=1, columnspan=2)
        label = tk.Label(self.canvas, text="Welcome to the music quiz!", font=self.font, bg=self.colour)
        label.grid(row=2, columnspan=2)
        
        self.statusLabel = tk.Label(self.canvas, text="Please authenticate to continue", font=self.label, bg=self.colour, width=40)
        self.statusLabel.grid(row=3, columnspan=2)

        line = tk.Frame(self.canvas, height=1, width=200, bg="grey")
        line.grid(row=4, columnspan=2, pady=10)

        self.loginFrame = tk.Frame(self.canvas, bg=self.colour)
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

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        label = tk.Label(self.loginFrame, text="Username", font=self.label, bg=self.colour)
        self.fieldUsername = tk.Entry(self.loginFrame, textvariable=self.username)
        self.fieldUsername.focus()

        label.grid(row=1, column=0, sticky=E)
        self.fieldUsername.grid(row=1, column=1, sticky=W)

        label = tk.Label(self.loginFrame, text="Password", font=self.label, bg=self.colour)
        self.fieldPassword = tk.Entry(self.loginFrame, textvariable=self.password, show="*")

        label.grid(row=2, column=0, sticky=E)
        self.fieldPassword.grid(row=2, column=1, sticky=W)

        buttonFrame = tk.Frame(self.loginFrame, bg=self.colour)
        buttonFrame.grid(row=3, columnspan=2, pady=5)

        
        self.loginButton = tk.Button(buttonFrame, text="Login", command=self.close_tutorial_callback)
        self.registerButton = tk.Button(buttonFrame, text="Register", command=self.show_tutorial_callback)

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

        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.password2 = tk.StringVar()

        label = tk.Label(self.loginFrame, text="Username", font=self.label, bg=self.colour)
        self.fieldUsername = tk.Entry(self.loginFrame, textvariable=self.username)
        self.fieldUsername.focus()

        label.grid(row=1, column=0, sticky=E)
        self.fieldUsername.grid(row=1, column=1, sticky=W)

        label = tk.Label(self.loginFrame, text="Password", font=self.label, bg=self.colour)
        self.fieldPassword = tk.Entry(self.loginFrame, textvariable=self.password, show="*")

        label.grid(row=2, column=0, sticky=E)
        self.fieldPassword.grid(row=2, column=1, sticky=W)

        label = tk.Label(self.loginFrame, text="Confirm Password", font=self.label, bg=self.colour)
        self.fieldPassword2 = tk.Entry(self.loginFrame, textvariable=self.password2, show="*")

        label.grid(row=3, column=0, sticky=E)
        self.fieldPassword2.grid(row=3, column=1, sticky=W)

        buttonFrame = tk.Frame(self.loginFrame, bg=self.colour)
        buttonFrame.grid(row=4, columnspan=2, pady=5)

        
        self.registerButton = tk.Button(buttonFrame, text="Register", command=self.Register_RegisterButtonPressed)
        self.loginButton = tk.Button(buttonFrame, text="Login", command=self.Register_LoginButtonPressed)

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

        label = tk.Label(self.loginFrame, text="Please wait for your account to be validated", font=self.label, bg=self.colour)
        label.grid(row=0, column=0, sticky=E)

        buttonFrame = tk.Frame(self.loginFrame, bg=self.colour)
        buttonFrame.grid(row=4, columnspan=2, pady=5)

        self.loginButton = tk.Button(buttonFrame, text="Login", command=self.Register_LoginButtonPressed)
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