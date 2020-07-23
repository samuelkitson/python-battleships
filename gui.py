# ******************************************************
#
# The GUI module provides classes for the user interfaces
#
# ******************************************************

# Import libraries
import variables
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import N, E, S, W, NE, SE, SW, NW, END
from PIL import Image, ImageTk


# Uses columnconfigure to set all columns to the same width in a provided grid
def set_equal_columns(grid, start_col=0, end_col=None):
    # If no end has been provided, default to all columns
    if (end_col == None):
        end_col = grid.grid_size()[0]
    else:
        end_col += 1
    for column_num in range(start_col, end_col):
        grid.columnconfigure(column_num, weight=1)


# Uses rowconfigure to set all rows to the same width in a provided grid
def set_equal_rows(grid, start_row=0, end_row=None):
    # If no end has been provided, default to all rows
    if (end_row == None):
        end_row = grid.grid_size()[0]
    else:
        end_row += 1
    for row_num in range(start_row, end_row):
        grid.rowconfigure(row_num, weight=1)


#Resize a PhotoImage using PIL
def resize_PhotoImage(path, width, height):
    #https://stackoverflow.com/a/52329796/8827535
    img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)


# Close all windows and quit the game
def quit_game(confirm=True):
    if confirm:
        confirm_answer = messagebox.askokcancel("Quit game", "Are you sure you want to quit the game? Your progress will be lost")
        if not confirm_answer:
            return False
    variables.window.close()
    

#
# The Window class provides the overall GUI window and extends the tk.Tk() class
# Closing this window will quit the application
#
class Window(tk.Tk):
    #Construct the window
    def __init__(self):
        #self.window = tk.Tk()
        super().__init__()
        self.title("Battleships")
        self.geometry("400x350")
        self.resizable(False, False)
        self.contents = tk.Frame(self)
        #self.contents.grid(row=1, column=1)
        self.contents.pack(fill=tk.BOTH, expand=1)
        
        # Catch the window close event and show a confirmation dialog
        self.protocol("WM_DELETE_WINDOW", quit_game)

    # Enables full screen mode
    # F11 to toggle, ESC to exit
    def full_screen(self):
        self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        self.bind("<F10>", lambda event:self.exit_full_screen())
        self.attributes("-fullscreen", True)

    # Disables key binding and exits full screen
    def exit_full_screen(self):
        self.unbind("<F11>")
        self.unbind("<Escape>")
        self.attributes("-fullscreen", False)

    # Destroys all child widgets within the contents Frame
    def clear_frame(self):
        for widget in self.contents.winfo_children():
            widget.destroy()

    def close(self):
        self.destroy()


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
        # Init the PopupWindow superclass
        super().__init__()
        
        # Create the GUI
        self.title = tk.Label(self.contents, text="Tutorial", fg=variables.title_colour, font=variables.title_font)
        self.title.grid(row=0, column=0, pady=(0,10), columnspan=3)
        self.text = tk.Text(self.contents, wrap=tk.WORD)
        self.text.grid(row=1, column=0, columnspan=3)
        self.text.config(bg="white", height=13, width=35, state="disabled")

        # Set up tags for custom text styles
        self.text.tag_configure("bold", font=("Helvetica", 10, "bold"))
        self.text.tag_configure("regular", font=("Helvetica", 10))

        self.write_text("Load tutorial, please wait...", ("bold"))

        self.left_button = ttk.Button(self.contents, text="◀ Previous", command=self.previous_page)
        self.left_button.config(width=10)
        self.left_button.grid(row=2, column=0, pady=(5,10), sticky="w")

        self.right_button = ttk.Button(self.contents, text="Next ▶", command=self.next_page)
        self.right_button.config(width=10)
        self.right_button.grid(row=2, column=2, pady=(5,10), sticky="e")

        self.exit_button = ttk.Button(self.contents, text="Back to the game", command=self.close)
        self.exit_button.grid(row=2, column=1, pady=(5,10))
        
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


#
# The GameSetup class provides the window shown to players at the start of the game
#
class GameSetup:
    # Construct the GUI
    def __init__(self, show_tutorial_callback, start_game_callback):
        # Set up the Frame instance for this window
        self.contents = tk.Frame(variables.window.contents)
        self.contents.pack(fill=tk.BOTH, expand=1)
        set_equal_columns(self.contents, 0, 1)
        variables.window.geometry("400x350")

        # Record callbacks
        self.show_tutorial_callback = show_tutorial_callback
        self.start_game_callback = start_game_callback

        # Create the GUI
        self.title = tk.Label(self.contents, text="Battleships", fg=variables.title_colour, font=variables.title_font)
        self.title.grid(row=0, column=0, columnspan=2, pady=(10,0))

        self.subtitle = tk.Label(self.contents, text="Python Edition", fg=variables.subtitle_colour, font=variables.subtitle_font)
        self.subtitle.grid(row=1, column=0, columnspan=2)

        self.options_frame = tk.LabelFrame(self.contents, text="Game options")
        self.options_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(10,20))

        self.player_number_value = tk.IntVar()
        self.player_number_value.set(1)
        self.single_player_radio = ttk.Radiobutton(self.options_frame, text="Single player", variable=self.player_number_value, value=1, command=lambda: self.enable_difficulty(True))
        self.single_player_radio.grid(row=0, column=0, sticky="w", padx=5)
        self.two_player_radio = ttk.Radiobutton(self.options_frame, text="Two players", variable=self.player_number_value, value=2, command=lambda: self.enable_difficulty(False))
        self.two_player_radio.grid(row=1, column=0, sticky="w", padx=5)

        self.difficulty_label = tk.Label(self.options_frame, text="Game difficulty:")
        self.difficulty_label.grid(row=0, column=1, sticky="w", padx=(5, 0))

        self.game_difficulty = tk.StringVar()
        self.game_difficulty.set(variables.difficulty_levels[0]) # default value
        self.game_difficulty_select = ttk.OptionMenu(self.options_frame, self.game_difficulty, variables.difficulty_levels[0], *variables.difficulty_levels)
        self.game_difficulty_select.config(width=8)
        self.game_difficulty_select.grid(row=1, column=1, sticky="w")

        self.resize_button = ttk.Button(self.contents, text="Start game", command=self.start_game_callback)
        self.resize_button.grid(row=3, column=0)

        self.tutorial_button = ttk.Button(self.contents, text="Tutorial", command=self.show_tutorial_callback)
        self.tutorial_button.grid(row=3, column=1)

        self.close_button = ttk.Button(self.contents, text="Quit", command=quit_game)
        self.close_button.grid(row=4, column=0)

        # Set the columns to equal width
        set_equal_columns(self.options_frame)


    # Enables or disables the difficulty selector
    def enable_difficulty(self, enabled):
        if enabled:
            mode = "normal"
        else:
            mode = "disabled"
        self.difficulty_label.config(state=mode)
        self.game_difficulty_select.config(state=mode)


    # Closes the window
    def close(self):
        self.contents.destroy()
        del self


#
# The ShipPlacement class allows the player(s) to place their ships
#
class ShipPlacement:
    # Construct the GUI
    def __init__(self, next_screen_callback):
        # Set up the Frame instance for this window
        self.contents = tk.Frame(variables.window.contents)
        self.contents.pack(fill=tk.BOTH, expand=1)
        variables.window.geometry("800x600")
        #variables.window.full_screen()
        variables.window.resizable(True, True) # TEMPORARY

        # Record callbacks
        self.next_screen_callback = next_screen_callback

        # Create the GUI
        self.title = tk.Label(self.contents, text="Ship Placement", fg=variables.title_colour, font=variables.title_font)
        self.title.grid(row=0, column=0, columnspan=2, pady=(10,0))

        self.subtitle = tk.Label(self.contents, text="You need to place 5 ships", fg=variables.subtitle_colour, font=variables.subtitle_font)
        self.subtitle.grid(row=1, column=0, columnspan=2)

        self.close_button = ttk.Button(self.contents, text="Quit", command=quit_game)
        self.close_button.grid(row=3, column=1, sticky="w")

        self.grid_frame = tk.Frame(self.contents)
        self.grid_frame.grid(row=3, column=0, padx=20, pady=20)
        self.grid_frame.config(bg="black")

        self.no_entry_image = resize_PhotoImage(r"images\noentry.png", variables.grid_image_width, variables.grid_image_height)
        self.pixel_image = tk.PhotoImage(width=1, height=1)

        self.buttons_array = []
        for row_num in range(0, variables.rows_number):
            self.buttons_array.append([None]*variables.columns_number)
            for col_num in range(0, variables.columns_number):
                # Create a button widget (note: this uses the original tkinter button, not the new ttk button)
                self.buttons_array[row_num][col_num] = tk.Button(self.grid_frame, image=self.pixel_image, height=variables.grid_image_height, width=variables.grid_image_width, text="X")
                # Set the onclick handler
                self.buttons_array[row_num][col_num]['command'] = lambda row=row_num, col=col_num: self.button_click_handler(row, col)
                # Position the button
                self.buttons_array[row_num][col_num].grid(row=row_num, column=col_num)

        set_equal_columns(self.contents)

    # Handler for any button presses from the grid
    def button_click_handler(self, row, col):
        print("Clicked: Row "+str(row+1)+" Column "+str(col+1)) 
        self.buttons_array[row][col].config(image=self.no_entry_image, text="")