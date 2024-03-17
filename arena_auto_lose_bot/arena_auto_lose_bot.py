import pyautogui
import ctypes
import sys
import os
import time
import tkinter as tk
from tkinter import messagebox, simpledialog


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from options import show_options_dialog

# Variable declarations
folder_location = 'arena_auto_lose_bot/'
window_name = "Arena Fight To Lose Points"
game_location = "Arena"
image_hint = "Season Text"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Set uniform values here
uniform_delay = 0.5
uniform_confidence = 0.8
uniform_click_delay = 0.25

# Arena coordinates
select_dragon_1 = (227, 807)
select_dragon_2 = (848, 809)
select_dragon_3 = (1455, 808)
sort_select = (1404, 261)
order_by_rarity_asc = (1260, 733)
first_dragon_select = (1002, 411)
right_arrow_sort = (1500, 922)
fight_button = (957, 911)
claim_button = (959, 962)

def locate_and_click(image_path, success_message, click=True, set_confidence=0.8, move_to_duration=0.5, delay_execution=0):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=set_confidence)

        if position is not None:
            print(GREEN + f"Found {success_message} at: {position}" + RESET)
            if click:
                time.sleep(delay_execution)
                pyautogui.moveTo(position, duration=move_to_duration)
                pyautogui.click(position, duration=0.01)
            return True
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate the {image_path} on the screen." + RESET)
    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)

def auto_click(coordinates, delay_duration=0.2):
    time.sleep(delay_duration)
    pyautogui.moveTo(coordinates, duration=0.2)
    pyautogui.click(coordinates, duration=0.01)

def show_dialog(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Bot Notification", 1)

# Bot sequence of tasks
def bot_cycle():
    for _ in range (selected_cycles):
        time.sleep(0.66)
        if locate_and_click(folder_location + 'change.png', 'Change Button'):
            # Select Dragon 1
            auto_click(select_dragon_1)
            auto_click(sort_select)
            auto_click(order_by_rarity_asc)
            auto_click(right_arrow_sort)
            auto_click(right_arrow_sort)
            auto_click(first_dragon_select)
            # Select Dragon 2
            auto_click(select_dragon_2)
            auto_click(sort_select)
            auto_click(order_by_rarity_asc)
            auto_click(right_arrow_sort)
            auto_click(right_arrow_sort)
            auto_click(first_dragon_select)
            # Select Dragon 3
            auto_click(select_dragon_3)
            auto_click(sort_select)
            auto_click(order_by_rarity_asc)
            auto_click(right_arrow_sort)
            auto_click(right_arrow_sort)
            auto_click(first_dragon_select)
            locate_and_click(folder_location + 'close.png', 'Close Button')
            auto_click(fight_button, delay_duration=0.4)
            locate_and_click(folder_location + 'close.png', 'Close Button', delay_execution=4)
            locate_and_click(folder_location + 'yes.png', 'Yes Button', move_to_duration=0.2)
            auto_click(claim_button, delay_duration=5)

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

# Bot Cycles Dropdown
class BotCyclesDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.dialog_title = "Fight Times"
        self.prompt = "Choose the number of times you want to lose in the Arena Fight:"
        super().__init__(parent, self.dialog_title)

    def body(self, master):
        self.bot_cycle_choices = [str(i) for i in range(1, 7)]
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
confirmation = messagebox.askquestion(window_name, "Open " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. \n\nHave you followed everything?")

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate 
while confirmation == 'yes':
    try:
        season = pyautogui.locateOnScreen(folder_location + 'season.png', confidence=0.8)
        if season is not None:
            print(GREEN + f"{image_hint} is found at: {season}" + RESET)
            bot_cycle()
            show_dialog(f"Done Fighting for {selected_cycles} times.")
            show_options_dialog()
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