import pyautogui
import time
import ctypes
import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from options import show_options_dialog

# Variable declarations
folder_location = 'collect_gold_food_bot/'
window_name = "Collect Gold and Food Bot"
game_location = "Main Island"
image_hint = "First Island"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Set uniform values here
uniform_delay = 0.5
uniform_confidence = 0.8
uniform_click_delay = 0.25

# Island drag-to points / coordinates
drag_to_0 = (329, 306)
drag_to_1 = (621, 698)
drag_to_2 = (915, 248)
drag_to_3 = (1082, 173)
drag_to_4 = (1024, 152)
drag_to_5 = (717, 1009)
drag_to_6 = (1463, 286)
drag_to_7 = (1201, 195)
drag_to_8 = (1156, 781)
drag_to_9 = (1017, 858)

def locate_and_click(image_path, success_message, click=True, set_confidence=0.9):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=set_confidence)

        if position is not None:
            print(GREEN + f"Found {success_message} at: {position}" + RESET)
            if click:
                pyautogui.moveTo(position, duration=0.66)
                pyautogui.click(position, duration=0.01)
            return True
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate the {image_path} on the screen." + RESET)
    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)

def show_dialog(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Bot Notification", 1)

# Bot sequence of tasks
def bot_cycle():
    for _ in range (selected_cycles):
        tasks = [
            (folder_location + 'gold.png', 'Gold found'),
            (folder_location + 'food.png', 'Food found'),
            (folder_location + 'gold-food.png', 'Gold and Food found'),
            (folder_location + 'close-accidental-open.png', 'Close Accidental Open Button found'),
        ]

        for task in tasks:
            locate_and_click(*task)

def move_island(search_image, coordinate, drag_delay=2, confidence=0.8):
    position = pyautogui.locateOnScreen(folder_location + search_image, confidence=confidence)
    print(GREEN + f"{search_image} is found at: {position}" + RESET)
    pyautogui.moveTo(position, duration=uniform_delay)
    pyautogui.dragTo(coordinate, button='left', duration=drag_delay)
    time.sleep(uniform_click_delay)

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

# Island Selection Dropdown
class IslandSelectionDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title)

    def body(self, master):
        self.island_choices = [str(i) for i in range(1, 10)]
        self.var = tk.StringVar()
        self.var.set(self.island_choices[0])

        tk.Label(master, text=self.prompt).pack()
        island_dropdown = tk.OptionMenu(master, self.var, *self.island_choices)
        island_dropdown.pack()

    def apply(self):
        self.result = self.var.get()

island_dialog = IslandSelectionDialog(root, "Select Island", "Choose up to which island this bot will execute:")
selected_island = island_dialog.result
if selected_island is not None:
    selected_island = int(selected_island)
else:
    selected_island = 0
    show_options_dialog()

# Bot Cycles Dropdown
class BotCyclesDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.dialog_title = "Select Bot Cycles"
        self.prompt = "Choose the number of bot cycles (i.e. number of Highest number of Gold/Food in an island):"
        super().__init__(parent, self.dialog_title)

    def body(self, master):
        self.bot_cycle_choices = [str(i) for i in range(1, 25)]
        self.var = tk.StringVar()
        self.var.set(self.bot_cycle_choices[0])

        tk.Label(master, text=self.prompt).pack()
        bot_cycles_dropdown = tk.OptionMenu(master, self.var, *self.bot_cycle_choices)
        bot_cycles_dropdown.pack()

    def apply(self):
        self.result = self.var.get()

bot_cycles_dialog_instance = BotCyclesDialog(root)
selected_cycles = bot_cycles_dialog_instance.result
if selected_cycles is not None:
    selected_cycles = int(selected_cycles)
else:
    selected_cycles = 0
    show_options_dialog()

# Confirmation Message
confirmation = messagebox.askquestion(window_name, "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "\nIn order for this to work, MAX the ZOOM OUT first then ZOOM IN TWO(2) times by pressing the PLUS(+) button."
                                                        "\nThen make sure the the TREE OF LIFE is VISIBLE on your screen and you go AFK while this bot is running."
                                                        "\n\nHave you followed everything?")

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate 
while confirmation == 'yes':
    try:
        position = pyautogui.locateOnScreen(folder_location + 'main-island-hint.png', confidence=0.8)
        if position is not None:
            print(GREEN + f"{image_hint} is found at: {position}" + RESET)
            for i in range(1, selected_island + 1):
                if i == 1:
                    pyautogui.moveTo(position, duration=uniform_delay)
                    pyautogui.dragTo(drag_to_0, button='left', duration=2.5)
                elif i == 2:
                    move_island('first-to-second-island.png', drag_to_1, 2)
                elif i == 3:
                    move_island('second-to-third-island.png', drag_to_2, 2)
                elif i == 4:
                    move_island('third-to-fourth-island.png', drag_to_3, 2)
                elif i == 5:
                    move_island('fourth-to-fifth-island.png', drag_to_4, 2, 0.9)
                elif i == 6:
                    move_island('fifth-to-sixth-island.png', drag_to_5, 2)
                elif i == 7:
                    move_island('sixth-to-fifth-island.png', drag_to_6, 2)
                    move_island('fifth-to-seventh-island.png', drag_to_7, 2)
                elif i == 8:
                    move_island('seventh-to-eighth-island.png', drag_to_8, 2)
                elif i == 9:
                    move_island('eighth-to-ninth-island.png', drag_to_9, 2)

                bot_cycle()
            show_dialog("Now collect the rest you lazy ass.")
            show_options_dialog()
            break
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate {image_hint}." + RESET)
        answer = messagebox.askyesno(window_name, "Are you sure " + game_location + " is located?\n\n"
                                                        "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "\nIn order for this to work well, MAX the ZOOM OUT first then ZOOM IN TWO(2) times by pressing the PLUS(+) button."
                                                        "\nThen make sure the the TREE OF LIFE is VISIBLE on your screen and you go AFK while this bot is running."
                                                        "\n\nWould you like to try scanning again?")
        if not answer:
            show_options_dialog()
            break
        else:
            print(f"Searching for the {image_hint}...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")