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
import re

import time

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


# Load all required image files into Image instances
def load_all_images():
    # Load image files into the Image class
    for path in variables.images_to_load:
        image = Image.open(path)
        # Extract just the file name
        name = path.split("/")[-1]
        variables.loaded_images[name] = image

# Naming convention for boat images:
# boat_type_colour_rotation
# type options:
#   e: end
#   m: middle
# colour options:
#   g: grey (standard)
#   y: yellow (selected)
#   e: green (placed successfully)
# rotation options:
#   u, r, d, l: up, right, down left
#   h, v: horizontal, vertical

# Resize and rotate images from variables.load_images, creating PhotoImages for use in the grid
def create_edited_PhotoImages():
    height = variables.grid_image_height
    width = variables.grid_image_width
    # Boat End Grey Up
    variables.photo_images["boat_e_g_u"] = resize_Image(variables.loaded_images["boat_end_grey.png"], width, height, 90)
    variables.photo_images["boat_e_g_r"] = resize_Image(variables.loaded_images["boat_end_grey.png"], width, height)
    variables.photo_images["boat_e_g_d"] = resize_Image(variables.loaded_images["boat_end_grey.png"], width, height, 270)
    variables.photo_images["boat_e_g_l"] = resize_Image(variables.loaded_images["boat_end_grey.png"], width, height, 180)
    # Boat Middle Grey Horizontal
    variables.photo_images["boat_m_g_h"] = resize_Image(variables.loaded_images["boat_middle_grey.png"], width, height)
    variables.photo_images["boat_m_g_v"] = resize_Image(variables.loaded_images["boat_middle_grey.png"], width, height, 90)
    
    # Boat End Yellow Up
    variables.photo_images["boat_e_y_u"] = resize_Image(variables.loaded_images["boat_end_yellow.png"], width, height, 90)
    variables.photo_images["boat_e_y_r"] = resize_Image(variables.loaded_images["boat_end_yellow.png"], width, height)
    variables.photo_images["boat_e_y_d"] = resize_Image(variables.loaded_images["boat_end_yellow.png"], width, height, 270)
    variables.photo_images["boat_e_y_l"] = resize_Image(variables.loaded_images["boat_end_yellow.png"], width, height, 180)
    # Boat Middle Yellow Horizontal
    variables.photo_images["boat_m_y_h"] = resize_Image(variables.loaded_images["boat_middle_yellow.png"], width, height)
    variables.photo_images["boat_m_y_v"] = resize_Image(variables.loaded_images["boat_middle_yellow.png"], width, height, 90)

    # Boat End Green Up
    variables.photo_images["boat_e_e_u"] = resize_Image(variables.loaded_images["boat_end_green.png"], width, height, 90)
    variables.photo_images["boat_e_e_r"] = resize_Image(variables.loaded_images["boat_end_green.png"], width, height)
    variables.photo_images["boat_e_e_d"] = resize_Image(variables.loaded_images["boat_end_green.png"], width, height, 270)
    variables.photo_images["boat_e_e_l"] = resize_Image(variables.loaded_images["boat_end_green.png"], width, height, 180)
    # Boat Middle Green Horizontal
    variables.photo_images["boat_m_e_h"] = resize_Image(variables.loaded_images["boat_middle_green.png"], width, height)
    variables.photo_images["boat_m_e_v"] = resize_Image(variables.loaded_images["boat_middle_green.png"], width, height, 90)

    # Crosshairs
    variables.photo_images["crosshairs"] = resize_Image(variables.loaded_images["noentry.png"], width, height)

#Resize an Image using PIL
def resize_Image(img, width, height, rotation=0):
    #https://stackoverflow.com/a/52329796/8827535
    #img = Image.open(path)
    img = img.resize((width, height), Image.ANTIALIAS)
    if not rotation == 0:
        img = img.rotate(rotation)
    return ImageTk.PhotoImage(img)


# Close all windows and quit the game
def quit_game(confirm=True):
    if confirm:
        confirm_answer = messagebox.askokcancel("Quit game", "Are you sure you want to quit the game? Your progress will be lost")
        if not confirm_answer:
            return False
    variables.window.close()


# Calculate images from the ships variable into the grid variable
# You will need to GameGrid.redraw() after to update the visual grid
def calculate_images(player_num, colour_code, complete_reset=False):
    # Get the ships variable
    source_ships = variables.player_ships[player_num]
    ship_num = 0
    for ship in source_ships:
        part_num = 0
        for loc in ship["locations"]:
            # Draw the new ship on the grid
            if ship["direction"] == "h":
                # Horizontal
                if part_num == 0:
                    # Start of ship
                    image_code = "boat_e_"+colour_code+"_l"
                elif part_num == ship["spaces"]-1:
                    # End of ship
                    image_code = "boat_e_"+colour_code+"_r"
                else:
                    # Middle
                    image_code = "boat_m_"+colour_code+"_h"
            else:
                # Vertical
                if part_num == 0:
                    # Start of ship
                    image_code = "boat_e_"+colour_code+"_u"
                elif part_num == ship["spaces"]-1:
                    # End of ship
                    image_code = "boat_e_"+colour_code+"_d"
                else:
                    # Middle
                    image_code = "boat_m_"+colour_code+"_v"
            # Set the grid variable
            variables.player_grids[player_num][loc[0]][loc[1]]["t"] = image_code
            if complete_reset:
                variables.player_grids[player_num][loc[0]][loc[1]]["s"] = "n"
                variables.player_grids[player_num][loc[0]][loc[1]]["i"] = ship_num
            part_num += 1
        ship_num += 1


#
# Custom buttons used to create the grid, extends the tk.Button class
#
class GridButton(tk.Button):
    def __init__(self, master, hover_crosshairs=False):
        # Init the tk.Button superclass
        super().__init__(master)
        # Single pixel image used to set the button size in pixels
        self.pixel_image = tk.PhotoImage(width=1, height=1)
        # Configure the button using the tk.Button methods
        self.config(image=self.pixel_image, height=variables.grid_image_height, width=variables.grid_image_width, relief="ridge", bg="white")
        # Show cross hairs on hover, if set
        if hover_crosshairs:
            self.bind("<Enter>", self.on_hover)
            self.bind("<Leave>", self.on_hover_end)
    
    # Set the background to crosshairs when hovered over
    def on_hover(self, *args):
        self.before_image = self["image"]
        self.config(image=variables.photo_images["crosshairs"])
    def on_hover_end(self, *args):
        self.config(image=self.before_image)

#
# A grid of GridButtons (extending the tk.Frame class), with settings defined in the variables module and callbacks passed upon init
# To use, create and place a GameGrid instance as if it were a normal Frame
#
class GameGrid(tk.Frame):
    # Construct the grid within a frame
    def __init__(self, master, button_callback, player_num, hover_crosshairs=False):
        # Init the tk.Frame superclass
        super().__init__(master)
        # Create the button layout
        self.buttons_array = []
        # Save the player number so the grid variable can be accessed later
        self.player_num = player_num
        # Dimensions are taken from variables.rows/columns_number
        for row_num in range(0, variables.rows_number):
            self.buttons_array.append([None]*variables.columns_number)
            # Create the row label - this is a letter
            row_label = tk.Label(self, text=variables.number_to_letter(row_num+1))
            row_label.grid(row=row_num+1, column=0)
            for col_num in range(0, variables.columns_number):
                # If it's the first row, add the column labels as well - this is a number
                if (row_num == 0):
                    col_label = tk.Label(self, text=str(col_num+1))
                    col_label.grid(row=0, column=col_num+1)
                # Create a button widget (note: this uses the original tkinter button, not the new ttk button)
                self.buttons_array[row_num][col_num] = GridButton(self, hover_crosshairs)
                # Set the onclick handler (pass row and column number (0-indexed) to the grid_click_handler function)
                #self.buttons_array[row_num][col_num]['command'] = lambda row=row_num, col=col_num: self.grid_click_handler(row, col)
                self.buttons_array[row_num][col_num]['command'] = lambda row=row_num, col=col_num: button_callback(row, col)
                # Position the button
                self.buttons_array[row_num][col_num].grid(row=row_num+1, column=col_num+1)

    # Clear and redraw the grid from the grid variable
    def redraw(self):
        # Get the grid variable
        source_grid = variables.player_grids[self.player_num]
        row_num = 0
        for row in source_grid:
            col_num = 0
            for cell in row:
                # Redraw the image
                image_ref = cell["t"]
                if not image_ref is None and image_ref != "":
                    self.buttons_array[row_num][col_num].config(image=variables.photo_images[cell["t"]], text="")
                col_num += 1
            row_num += 1

    # Deselects all ships from the grid and turns all to grey
    def deselect_all(self):
        # Any boat image, as long as it is not grey
        check_pattern = re.compile("boat_[a-z]_[a-fh-z]_[a-z]")
        row_num = 0
        for row in variables.player_grids[self.player_num]:
            col_num = 0
            for cell in row:
                # Check if that cell already has an image, and that it isn't grey
                if cell["t"] != None and check_pattern.match(cell["t"]):
                    # If found, reset to the grey colour
                    cell["t"] = cell["t"][:7] + "g" + cell["t"][8:]
                    self.buttons_array[row_num][col_num].config(image=variables.photo_images[cell["t"]], text="")
                col_num += 1
            row_num += 1

    # Clear all ships from the grid
    def clear(self, clear_grid_var=False):
        # Iterate through 
        row_num = 0
        for row in variables.player_grids[self.player_num]:
            col_num = 0
            for cell in row:
                # Reset location state in grid var, if required
                if clear_grid_var:
                    variables.player_grids[self.player_num][row_num][col_num] = {"s":"e", "i":None, "t":None}
                # Reset grid image
                cell_button = self.buttons_array[row_num][col_num]
                cell_button.config(image=cell_button.pixel_image, text="")
                col_num += 1
            row_num += 1
    

#
# The Window class provides the overall GUI window and extends the tk.Tk class
# Closing this window will quit the application
#
class Window(tk.Tk):
    #Construct the window
    def __init__(self, show_tutorial_callback):
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

        # Record the callbacks
        self.show_tutorial_callback = show_tutorial_callback

        # Load and create images
        load_all_images()
        create_edited_PhotoImages()

    # Enables full screen mode
    # F11 to toggle, ESC to exit
    def full_screen(self):
        self.bind("<F11>", lambda event: self.attributes("-fullscreen", not self.attributes("-fullscreen")))
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        self.bind("<F10>", lambda event:self.exit_full_screen())
        self.attributes("-fullscreen", True)

    # Disables F11 key binding and exits full screen
    def exit_full_screen(self):
        self.unbind("<F11>")
        self.unbind("<Escape>")
        self.attributes("-fullscreen", False)

    # Enters the "zoomed" state
    def enter_zoomed(self):
        self.state("zoomed")

    # Exits the "zoomed" state
    def exit_zoomed(self):
        self.state("normal")

    # Shows the tutorial at a certain page when F11 is pressed
    def bind_tutorial_page(self, page_num):
        self.bind("<F1>", lambda event:self.show_tutorial_callback(page_num))

    # Destroys all child widgets within the contents Frame
    def clear_frame(self):
        for widget in self.contents.winfo_children():
            widget.destroy()

    def close(self):
        self.destroy()


#
# An inner window to sit inside of the main game Window instance
# Child of the main window.contents frame
#
class InnerWindow:
    def __init__(self, size, full_screen=False, resizeable=(True, True)):
        # Set up the Frame instance for this inner window
        self.contents = tk.Frame(variables.window.contents)
        self.contents.pack(fill=tk.BOTH, expand=1)
        # Set the window dimensions according to the passed arguments
        if size=="maximise":
            variables.window.enter_zoomed()
        else:
            variables.window.exit_zoomed()
            variables.window.geometry(size)
        if full_screen: variables.window.full_screen()
        variables.window.resizable(*resizeable)


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
    def __init__(self, init_page=None):
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

        if (init_page != None):
            self.to_page(init_page)

    # Loads the tutorial.txt into the self.tutorial_text array, split by page
    def load_tutorial_file(self):
        try:
            with open("tutorial.txt", 'r') as tutorial_file:
                raw_pages = tutorial_file.read().split("###PAGEBREAK###")
                self.tutorial_pages = []
                for page in raw_pages:
                    new_page = {}
                    if "~~" in page:
                        # Title on this page
                        split_page = page.split("~~")
                        new_page["title"] = split_page[1]
                        new_page["text"] = split_page[2]
                    else:
                        # No title
                        new_page["title"] = None
                        new_page["text"] = page
                    self.tutorial_pages.append(new_page)
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
    def to_page(self, page_num):
        if (page_num < len(self.tutorial_pages)) and (page_num >= 0):
            self.page_number = page_num
            self.write_page()

    # Prints the current page
    def write_page(self):
        self.clear_text()
        page_content = self.tutorial_pages[self.page_number]
        # Write title in bold, if applicable
        if not page_content["title"] is None:
            self.write_text(page_content["title"]+"\n", ("bold"))
        self.write_text(page_content["text"].strip())

    # Closes the window
    def close(self):
        self.destroy()
        del self


#
# The GameSetup class provides the window shown to players at the start of the game
#
class GameSetup(InnerWindow):
    # Construct the GUI
    def __init__(self, show_tutorial_callback, start_game_callback):
        # Init as an InnerWindow
        super().__init__("400x350", False, (False, False))
        # Set up the Frame instance for this window
        """self.contents = tk.Frame(variables.window.contents)
        self.contents.pack(fill=tk.BOTH, expand=1)
        variables.window.geometry("400x350")"""
        set_equal_columns(self.contents, 0, 1)


        # Record callbacks
        self.show_tutorial_callback = show_tutorial_callback
        self.start_game_callback = start_game_callback

        # Set up tutorial page
        variables.window.bind_tutorial_page(1)

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
        self.game_difficulty_select = ttk.OptionMenu(self.options_frame, self.game_difficulty, variables.difficulty_levels[0], *variables.difficulty_levels)
        self.game_difficulty_select.config(width=8)
        self.game_difficulty_select.grid(row=1, column=1, sticky="w")
        self.game_difficulty.set(variables.difficulty_levels[1]) # Default value

        self.start_button = ttk.Button(self.contents, text="Start game", command=self.start_game_callback)
        self.start_button.grid(row=3, column=0)

        self.tutorial_button = ttk.Button(self.contents, text="Tutorial", command=self.show_tutorial_callback)
        self.tutorial_button.grid(row=3, column=1)

        self.close_button = ttk.Button(self.contents, text="Quit", command=quit_game)
        self.close_button.grid(row=4, column=0)

        self.help_message = tk.Label(self.contents, text="Need help? Press the F1 key at any point to view the help page", wraplength=350)
        self.help_message.grid(row=5, column=0, columnspan=2, pady=(20,10))

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
# The ShipPlacement class allows the player(s) to place their ships using the GameGrid class
#
class ShipPlacement(InnerWindow):
    # Construct the GUI
    def __init__(self, next_screen_callback):
        # Init as an InnerWindow
        super().__init__("1000x600")
        # Set up the Frame instance for this window
        """self.contents = tk.Frame(variables.window.contents)
        self.contents.pack(fill=tk.BOTH, expand=1)
        variables.window.geometry("1000x600")
        #variables.window.full_screen()
        variables.window.resizable(True, True) # TEMPORARY"""

        # Record callbacks
        self.next_screen_callback = next_screen_callback

        # Link tutorial page
        variables.window.bind_tutorial_page(2)

        # Create the GUI
        self.title = tk.Label(self.contents, text="Ship Placement", fg=variables.title_colour, font=variables.title_font)
        self.title.grid(row=0, column=0, columnspan=3, pady=(10,0))

        self.subtitle = tk.Label(self.contents, text="You need to place 5 ships", fg=variables.subtitle_colour, font=variables.subtitle_font)
        self.subtitle.grid(row=1, column=0, columnspan=3, pady=(0,20))

        #self.close_button = ttk.Button(self.contents, text="Quit", command=quit_game)
        #self.close_button.grid(row=3, column=1, sticky="w")

        # Construct and place grid using GameGrid instance
        self.placement_grid = GameGrid(self.contents, self.grid_click_handler, 0, False)
        self.placement_grid.grid(row=3, rowspan=2, column=0, padx=(20,0), pady=20)

        # Create the ship inventory
        self.inventory_frame = tk.LabelFrame(self.contents, text="Your ships", width=50)
        self.inventory_frame.grid(row=3, column=1, sticky="nw", padx=(30,10), pady=(35,0))
        self.inventory_images_array = []
        self.inventory_labels_array = []
        ship_num = 0
        for ship in variables.player_ships[0]:
            # Ship image
            # 2D array: 1st layer is ship number, second layer is part number
            # Draw each ship in the inventory panel
            self.inventory_images_array.append([])
            for part_num in range(0, ship["spaces"]):
                if part_num == 0:
                    image_ref = variables.photo_images["boat_e_g_l"]
                elif part_num == ship["spaces"]-1:
                    image_ref = variables.photo_images["boat_e_g_r"]
                else:
                    image_ref = variables.photo_images["boat_m_g_h"]
                self.inventory_images_array[-1].append(tk.Label(self.inventory_frame, image=image_ref))   
                self.inventory_images_array[-1][-1].grid(row=ship_num, column=part_num, padx=0, pady=5)
                self.inventory_images_array[-1][-1].bind("<Button-1>", lambda e, s_index=ship_num, p_index=part_num: self.choose_ship(s_index, p_index)) #testing
            # Ship label
            self.inventory_labels_array.append(None)
            self.inventory_labels_array[-1] = tk.Label(self.inventory_frame, text=ship["name"]+" ("+str(ship["spaces"])+")")
            self.inventory_labels_array[-1].grid(row=ship_num, column=5, padx=(0,5), pady=(2,0), sticky=W)
            ship_num += 1

        # Create the ship placement tools frame
        # Ship direction buttons
        self.tools_frame = tk.LabelFrame(self.contents, text="Tools", width=50)
        self.tools_frame.grid(row=4, column=1, sticky="nw", padx=(30,10), pady=0)
        self.direction_label1 = tk.Label(self.tools_frame, text="Next ship direction:")
        self.direction_label1.grid(row=0, column=0, padx=10, pady=(5,0), sticky="w")
        self.direction_label2 = tk.Label(self.tools_frame, text="Horizontal")
        self.direction_label2.grid(row=1, column=0, padx=10, pady=(0,5), sticky="w")
        self.rotate_button = ttk.Button(self.tools_frame, text="Toggle direction", command=self.change_direction)
        self.rotate_button.config(width=18)
        self.rotate_button.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        # Game flow buttons
        self.start_game_button = ttk.Button(self.tools_frame, text="Reset grid", command=self.clear_grid)
        self.start_game_button.config(width=15)
        self.start_game_button.grid(row=0, column=1, padx=(30,10))
        """self.tutorial_button = ttk.Button(self.tools_frame, text="Tutorial", command=self.show_tutorial_callback)
        self.tutorial_button.config(width=15)
        self.tutorial_button.grid(row=1, column=1, padx=(30,10), pady=(5, 0))"""
        self.start_game_button = ttk.Button(self.tools_frame, text="Start game", command=self.next_screen)
        self.start_game_button.config(width=15, state=tk.DISABLED)
        self.start_game_button.grid(row=1, column=1, padx=(30,10), pady=(5, 0))

        # The index of the ship being placed, None if no ship is active
        self.active_ship_index = None

        # The direction of the next ship
        self.ship_direction = "h"

        #set_equal_columns(self.contents)
        self.contents.columnconfigure(2, weight=1)

    # Clean up the grid, then call the callback
    def next_screen(self):
        # Reset all ships on the grid (and in the grid variable) to default colours
        self.placement_grid.deselect_all()
        # Trigger the saved callback
        self.next_screen_callback()

    # Toggle the direction of the next ship (vertical or horizontal)
    def change_direction(self):
        if self.ship_direction == "h":
            self.ship_direction = "v"
            self.direction_label2.config(text="Vertical")
        else:
            self.ship_direction = "h"
            self.direction_label2.config(text="Horizontal")

    # Check if all ships have been placed and toggle the start game button accordingly
    def check_grid_complete(self):
        grid_complete = True
        for ship in variables.player_ships[0]:
            if ship["state"] != "placed" and ship["state"] != "review":
                grid_complete = False
                break
        if grid_complete:
            self.start_game_button.config(state=tk.NORMAL)
        else:
            self.start_game_button.config(state=tk.DISABLED)

    # Remove all ships from the grid, with confirmation
    def clear_grid(self):
        # Confirm grid clear
        confirm_answer = messagebox.askokcancel("Clear grid", "Are you sure you want to clear the entire grid? All your ships will be placed back into your inventory")
        if not confirm_answer:
            return False
        # Reset player ships list
        for ship in variables.player_ships[0]:
            ship["state"] = "unplaced"
            ship["locations"] = [[0,0]]*ship["spaces"]
        # Reset player grid and visual grid
        self.placement_grid.clear(True)
        self.set_inventory_colours()
        self.check_grid_complete()

    # Highlight a ship in yellow on the grid
    def select_ship_grid(self, ship_index, *args):
        self.placement_grid.deselect_all()
        # Get locations from player ships variable
        ship_locs = variables.player_ships[0][ship_index]["locations"]
        for loc in ship_locs:
            if loc == [0,0]:
                # Ship not placed yet
                return False
            old_image = variables.player_grids[0][loc[0]][loc[1]]["t"]
            new_image = old_image[:7] + "y" + old_image[8:]
            variables.player_grids[0][loc[0]][loc[1]]["t"] = new_image
            self.placement_grid.buttons_array[loc[0]][loc[1]].config(image=variables.photo_images[new_image], text="")
        return True

    # Place a ship starting at a specific location on the grid
    # Click location references the top-leftmost part of the ship, no matter if it's horizontal or vertical
    # The details of the ship to be placed will be fetched from the self.active_ship variable
    # Direction: "v" for vertical, "h" for horizontal
    def place_ship(self, top_left_row, top_left_col, direction):
        ship = variables.player_ships[0][self.active_ship_index]
        piece_row = top_left_row
        piece_col = top_left_col

        # Generate the list of positions for this ship's parts
        # 0-indexed row number, then 0-indexed column number
        locations_list = []
        piece_row = top_left_row
        piece_col = top_left_col
        for part_num in range(0, ship["spaces"]):
            if (piece_col+1 > variables.columns_number or piece_row+1 > variables.rows_number):
                # If the location won't fit on the grid
                messagebox.showwarning("Invalid position", "The selected ship will not fit in that location")
                return False
            if (variables.player_grids[0][piece_row][piece_col]["s"] != "e"):
                # If the location already has a ship part there, show an error
                messagebox.showwarning("Invalid position", "That location overlaps with another ship\nPlease choose a different position")
                return False
            locations_list.append([])
            locations_list[-1].extend([piece_row, piece_col])
            if direction == "h":
                piece_col += 1
            else:
                piece_row += 1

        # Iterate through piece locations
        # Add ship locations to player grid and ship location lists
        part_num = 0
        for loc in locations_list:
            # Draw the new ship on the grid
            if direction == "h":
                # Horizontal
                if part_num == 0:
                    # Start of ship
                    image_code = "boat_e_y_l"
                elif part_num == ship["spaces"]-1:
                    # End of ship
                    image_code = "boat_e_y_r"
                else:
                    # Middle
                    image_code = "boat_m_y_h"
            else:
                # Vertical
                if part_num == 0:
                    # Start of ship
                    image_code = "boat_e_y_u"
                elif part_num == ship["spaces"]-1:
                    # End of ship
                    image_code = "boat_e_y_d"
                else:
                    # Middle
                    image_code = "boat_m_y_v"
            self.placement_grid.buttons_array[loc[0]][loc[1]].config(image=variables.photo_images[image_code], text="")
            # Update the player grid
            variables.player_grids[0][loc[0]][loc[1]]["s"] = "n"
            variables.player_grids[0][loc[0]][loc[1]]["i"] = self.active_ship_index
            variables.player_grids[0][loc[0]][loc[1]]["t"] = image_code
            # Increment the part counter
            part_num += 1

        variables.player_ships[0][self.active_ship_index]["locations"] = locations_list
        # Successful ship placement, return True
        return True

    # Handler for any button presses from the grid
    def grid_click_handler(self, row, col):
        # Check that a ship has been selected
        if self.active_ship_index is None:
            messagebox.showwarning("No ship selected", "Please select a ship to place in the grid\nTo view the help page for this section, close this alert then press the F1 key")
            return
        # Has ship already been placed? If so, disallow another placement
        if variables.player_ships[0][self.active_ship_index]["state"] == "review" or variables.player_ships[0][self.active_ship_index]["state"] == "placed":
            return
        if not self.place_ship(row, col, self.ship_direction):
            # If failed to place ship, return
            return
        variables.player_ships[0][self.active_ship_index]["state"] = "placed"
        variables.player_ships[0][self.active_ship_index]["direction"] = self.ship_direction
        self.check_grid_complete()

    # Changes the colour of a ship in the inventory panel
    def change_inv_ship_colour(self, ship_index, colour_code):
        part_counter = 0
        for ship_image in self.inventory_images_array[ship_index]:
            if (part_counter == 0):
                image_ref = variables.photo_images["boat_e_"+colour_code+"_l"]
            elif (part_counter == len(self.inventory_images_array[ship_index])-1):
                image_ref = variables.photo_images["boat_e_"+colour_code+"_r"]
            else:
                image_ref = variables.photo_images["boat_m_"+colour_code+"_h"]
            ship_image.config(image=image_ref)
            part_counter += 1

    # Colours the ships in the inventory panel accordingly
    def set_inventory_colours(self):
        # Set colours for all ships in the player's list
        counter = 0
        for ship in variables.player_ships[0]:
            ship_state = ship["state"]
            # Choose colour
            if ship_state == "unplaced":
                colour_id = "g"
            elif ship_state == "placed":
                colour_id = "e"
            elif ship_state == "active" or ship_state == "review":
                colour_id = "y"
            else:
                colour_id = "g"
            # Change colour
            self.change_inv_ship_colour(counter, colour_id)
            counter += 1

    # Selects a new ship to place
    def choose_ship(self, ship_index, part_index):
        self.active_ship_index = ship_index
        # Sets ships under review to "placed" state
        for ship in variables.player_ships[0]:
            if ship["state"] == "review":
                ship["state"] = "placed"
        # Highlights the current location if it has already been placed
        if self.select_ship_grid(ship_index):
            variables.player_ships[0][ship_index]["state"] = "review"
            self.set_inventory_colours()
            return
        # Set currently active ships to the "unplaced" state
        for ship in variables.player_ships[0]:
            if ship["state"] == "active":
                ship["state"] = "unplaced"
        # Set new ship to "active" state
        variables.player_ships[0][ship_index]["state"] = "active"
        self.set_inventory_colours()


#
# The GameView window is the main game window, allowing players to see their own ships and attack their opponent's
#
class GameView(InnerWindow):
    # Construct the GUI
    def __init__(self, next_screen_callback):
        # Init as an InnerWindow
        super().__init__("maximise")

        # Record callbacks
        self.next_screen_callback = next_screen_callback

        # Link tutorial page
        variables.window.bind_tutorial_page(3)

        # Create the GUI
        self.title = tk.Label(self.contents, text="Battleships", fg=variables.title_colour, font=variables.title_font)
        self.title.grid(row=0, column=0, columnspan=2, pady=(10,0))

        # Construct and place the grids using GameGrid instance
        self.attack_title = tk.Label(self.contents, text="Opponent Ships", fg="red", font=variables.subtitle_font)
        self.attack_title.grid(row=1, column=0, pady=(30,10), padx=(28,0))
        self.attack_grid = GameGrid(self.contents, self.attack_grid_click, 1, True)
        self.attack_grid.grid(row=2, column=0, padx=(20,0), pady=(0,20))
        self.attack_grid.redraw()

        self.defence_title = tk.Label(self.contents, text="Your Ships", fg="green", font=variables.subtitle_font)
        self.defence_title.grid(row=1, column=1, pady=(30,10), padx=(28,0))
        self.defence_grid = GameGrid(self.contents, self.own_grid_click, 0, False)
        self.defence_grid.grid(row=2, column=1, padx=(20,0), pady=(0,20))
        self.defence_grid.redraw()

        set_equal_columns(self.contents)

    # Handle a click on the attacking grid
    def attack_grid_click(self, row_num, col_num):
        print("Attack grid", row_num, col_num)

    # Handle a click on the player's own grid
    def own_grid_click(self, row_num, col_num):
        print("Own grid", row_num, col_num)