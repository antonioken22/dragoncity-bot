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
folder_location = 'skip_6h_bot/'
window_name = "Skip 6h Bot"
game_location = "Hatchery, Breeding, and Buildings"
image_hint = "Skip 6h Text Button"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def locate_and_click(image_path, success_message, click=True, delay_execution=0):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=0.8)
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
    close_reward_flag = 0
    while True:
        if locate_and_click(folder_location + 'out-of-ads.png', "Out of Ads", click=False):
                show_dialog("No Ads this time, try again later.")
                show_options_dialog()
                break
        elif locate_and_click(folder_location + 'close-reward.png', 'Close Reward Button', delay_execution=5):
                close_reward_flag = close_reward_flag + 1
                continue
        elif locate_and_click(folder_location + 'place.png', 'Place Button', click=False):
                locate_and_click(folder_location + 'close.png', 'Close Button')
                continue
        elif (close_reward_flag == selected_cycles):
            show_dialog(f"Done watching ads for {selected_cycles} times.")
            show_options_dialog()
            break
        tasks = [
            (folder_location + 'skip-6h-play-button.png', 'Skip 6h Play Button'),
            (folder_location + 'skip-6h.png', 'Skip 6h Text Button'),
        ]
        for task in tasks:
            locate_and_click(*task)

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

# Confirmation Message
confirmation = messagebox.askquestion(window_name, "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Click which of it you want its time to be reduced by 6 hours. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. "
                                                        "\n\nHave you followed everything?")

# Bot Cycles Dropdown
class BotCyclesDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.dialog_title = "Skip 6h Watch Video Times"
        self.prompt = "Choose the number of times you want to SKIP 6H for this operation:"
        super().__init__(parent, self.dialog_title)

    def body(self, master):
        self.bot_cycle_choices = [str(i) for i in range(1, 9)]
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

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate
while confirmation == 'yes':
    try:
        skip_6h_text = pyautogui.locateOnScreen(folder_location + 'skip-6h.png', confidence=0.8)
        if skip_6h_text is not None:
            print(GREEN + f"{image_hint} is found at: {skip_6h_text}" + RESET) or print
            pyautogui.moveTo(skip_6h_text, duration=0.66)
            pyautogui.click(skip_6h_text, duration=0.01)
            bot_cycle()
            break
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate {image_hint}." + RESET)
        answer = messagebox.askyesno(window_name, "Are you sure " + game_location + " is located?\n\n"
                                                        "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Click which of it you want its time to be reduced by 6 hours. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. "
                                                        "\n\nWould you like to try scanning again?")
        if not answer:
            show_options_dialog()
            break
        else:
            print(f"Searching for the {image_hint}...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")