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
folder_location = 'terra_hatch_bot/'
window_name = "Unlimited Terra Hatching"
game_location = "Divine Orbs Habitat 2 & Hatchery 6"
image_hint = "Divine Orbs Habitat 2 & Hatchery 6"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def locate_and_click(image_path, success_message, click=True, set_confidence=0.9):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=set_confidence)

        if position is not None:
            print(GREEN + f"Found {success_message} at: {position}" + RESET)
            if click:
                pyautogui.moveTo(position, duration=0.4)
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
        time.sleep(1)
        if locate_and_click(folder_location + 'divine-orbs-habitat-2.png', 'Divine Orbs Habitat 2', set_confidence=0.8):
            time.sleep(1)
            if locate_and_click(folder_location + 'get-egg.png', 'Get Egg Button', set_confidence=0.8):
                time.sleep(0.4)
                if locate_and_click(folder_location + 'gold.png', 'Gold Button'):
                    time.sleep(0.4)
                    if locate_and_click(folder_location + 'terra-buy.png', 'Terra Buy Button', set_confidence=0.8):
                        time.sleep(16)
                        if locate_and_click(folder_location + 'terra-hatch.png', 'Terra Hatch Button'):
                            time.sleep(0.4)
                            if locate_and_click(folder_location + 'place.png', 'Place Button'):
                                time.sleep(1)
                                if locate_and_click(folder_location + 'divine-orbs-habitat-2.png', 'Divine Orbs Habitat 2', set_confidence=0.8):
                                    time.sleep(1)
                                    if locate_and_click(folder_location + 'terra-dragon.png', 'Terra Dragon'):
                                        time.sleep(0.4)
                                        if locate_and_click(folder_location + 'sell.png', 'Sell Button'):
                                            time.sleep(0.4)
                                            locate_and_click(folder_location + 'sell-green.png', 'Green Sell Button')

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

# Bot Cycles Dropdown
class BotCyclesDialog(simpledialog.Dialog):
    def __init__(self, parent):
        self.dialog_title = "Terra Hatching Times"
        self.prompt = "Choose the number of times you want to hatch Terra Dragons:"
        super().__init__(parent, self.dialog_title)

    def body(self, master):
        self.bot_cycle_choices = [str(i) for i in range(1, 41)]
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
                                                        "\nThen make sure the the HATCHERY 6 is the CLOSEST to the " + game_location + " and you go AFK while this bot is running."
                                                        "\n\nHave you followed everything?")

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate 
while confirmation == 'yes':
    try:
        hatchery_6 = pyautogui.locateOnScreen(folder_location + 'hatchery-6.png', confidence=0.8)
        divine_orbs_habitat_2 = pyautogui.locateOnScreen(folder_location + 'divine-orbs-habitat-2.png', confidence=0.8)
        if hatchery_6 and divine_orbs_habitat_2 is not None:
            print(GREEN + f"{image_hint} is found at: {hatchery_6}" + RESET)
            print(GREEN + f"{image_hint} is found at: {divine_orbs_habitat_2}" + RESET)
            bot_cycle()
            show_dialog(f"Done hatching Terra Dragons for {selected_cycles} times.")
            show_options_dialog()
            break
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate {image_hint}." + RESET)
        answer = messagebox.askyesno(window_name, "Are you sure " + game_location + " is located?\n\n"
                                                        "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "\nIn order for this to work well, MAX the ZOOM OUT first then ZOOM IN TWO(2) times by pressing the PLUS(+) button."
                                                        "\nThen make sure the the HATCHERY 6 is the CLOSEST to the " + game_location + " and you go AFK while this bot is running."
                                                        "\n\nWould you like to try scanning again?")
        if not answer:
            show_options_dialog()
            break
        else:
            print(f"Searching for the {image_hint}...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")