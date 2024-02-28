import tkinter as tk
from tkinter import messagebox
import pyautogui
import time
import ctypes
import sys
import os

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

def locate_and_click(image_path, success_message, click=True, region=None):
    try:
        if region:
            position = pyautogui.locateOnScreen(image_path, confidence=uniform_confidence, region=region)
        else:
            position = pyautogui.locateOnScreen(image_path, confidence=uniform_confidence)

        if position is not None:
            print(GREEN + f"Found {success_message} at: {position}" + RESET)
            if click:
                time.sleep(uniform_delay)
                pyautogui.click(position)
                time.sleep(uniform_delay)
            return True
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate the {image_path} on the screen." + RESET)
    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)

def show_dialog(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Bot Notification", 1)

# Bot sequence of tasks
def bot_cycle():
    for _ in range (16):
        tasks = [
            (folder_location + 'gold.png', 'Gold found'),
            (folder_location + 'food.png', 'Food found'),
            (folder_location + 'gold-food.png', 'Gold and Food found'),
        ]

        for task in tasks:
            locate_and_click(*task)

def move_island(search_image, coordinate, drag_delay=2):
    position = pyautogui.locateOnScreen(folder_location + search_image, confidence=0.8)
    print(GREEN + f"{search_image} is found at: {position}" + RESET)
    pyautogui.moveTo(position, duration=uniform_delay)
    pyautogui.dragTo(coordinate, button='left', duration=drag_delay)
    time.sleep(uniform_click_delay)

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

confirmation = messagebox.askquestion(window_name, "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "\nIn order for this to work well, MAX the ZOOM OUT first then ZOOM IN TWO(2) times by pressing the PLUS(+) button."
                                                        "\nAnd you go AFK while this bot is running."
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
            pyautogui.moveTo(position, duration=uniform_delay)
            pyautogui.dragTo(drag_to_0, button='left', duration=2.5)
            bot_cycle()
            move_island('first-to-second-island.png', drag_to_1, 2)
            bot_cycle()
            move_island('second-to-third-island.png', drag_to_2, 2)
            bot_cycle()
            move_island('third-to-fourth-island.png', drag_to_3, 2)
            bot_cycle()
            move_island('fourth-to-fifth-island.png', drag_to_4, 2)
            bot_cycle()
            move_island('fifth-to-sixth-island.png', drag_to_5, 2)
            bot_cycle()
            move_island('sixth-to-fifth-island.png', drag_to_6, 2)
            move_island('fifth-to-seventh-island.png', drag_to_7, 2)
            bot_cycle()
            move_island('seventh-to-eighth-island.png', drag_to_8, 2)
            bot_cycle()
            move_island('eighth-to-ninth-island.png', drag_to_9, 2)
            bot_cycle()
            show_dialog("Now collect the rest you lazy ass.")
            break
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate {image_hint}." + RESET)
        answer = messagebox.askyesno(window_name, "Are you sure " + game_location + " is located?\n\n"
                                                        "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "\nIn order for this to work well, MAX the ZOOM OUT first then ZOOM IN TWO(2) times by pressing the PLUS(+) button."
                                                        "\nAnd you go AFK while this bot is running."
                                                        "\n\nWould you like to try scanning again?")
        if not answer:
            show_options_dialog()
            break
        else:
            print(f"Searching for the {image_hint}...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")