import pyautogui
import time
import ctypes
import sys
import os
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from options import show_options_dialog

# Variable declarations
folder_location = 'watch_greenhouse_ad_bot/'
window_name = "Watch Greenhouse Ads Bot"
game_location = "Greenhouse Building"
image_hint = "Greenhouse Text"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Set uniform values here
uniform_delay = 0.5
uniform_confidence = 0.8

def locate_and_click(image_path, success_message, click=True, delay_execution=0):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=uniform_confidence)

        if position is not None:
            print(GREEN + f"Found {success_message} at: {position}" + RESET)
            if click:
                time.sleep(delay_execution)
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
    try:
        while True:
            if locate_and_click(folder_location + 'out-of-ads.png', "Out of Ads found", click=False):
                show_dialog("No Ads this time, try again later.")
                show_options_dialog()
                break
            elif locate_and_click(folder_location + 'close-reward.png', 'Close Reward Button found', delay_execution=5):
                continue
            tasks = [
                (folder_location + 'play-ad.png', 'Play Ad Button found'),
                # (folder_location + 'greenhouse-building.png', 'Greenhouse Building found'),
                # (folder_location + 'greenhouse-status.png', 'Greenhouse Status found'),
            ]
            for task in tasks:
                locate_and_click(*task)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Stopping the loop.")
        show_dialog("Keyboard interrupt received. Stopping the loop.")
        show_options_dialog()

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

confirmation = messagebox.askquestion(window_name, "Open " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. \n\nHave you followed everything?")

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate 
while confirmation == 'yes':
    try:
        position = pyautogui.locateOnScreen(folder_location + 'greenhouse.png', confidence=0.8)
        if position is not None:
            print(GREEN + f"{image_hint} is found at: {position}" + RESET)
            bot_cycle()
            break
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate {image_hint}." + RESET)
        answer = messagebox.askyesno(window_name, "Are you sure " + game_location + " is open?\n\n"
                                                        "Open " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program.\n\n"
                                                        "Would you like to try scanning again?")
        if not answer:
            show_options_dialog()
            break
        else:
            print(f"Searching for the {image_hint}...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")