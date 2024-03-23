import pyautogui
import ctypes
import sys
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from options import show_options_dialog

# Variable declarations
folder_location = 'dragon_rescue_bot/'
window_name = "Dragon Rescue Bot"
game_location = "Dragon Rescue"
image_hint = "Dragon Rescue Text"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Set uniform values here
uniform_delay = 0.5
uniform_confidence = 0.8
uniform_click_delay = 0.25

def locate_and_click(image_path, image_description, click_times=1, duration=0.01, click=True, set_confidence=0.8):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=set_confidence)

        if position is not None:
            print(GREEN + f"Found {image_description} at: {position}" + RESET)
            if click:
                pyautogui.moveTo(position, duration=0.66)
                for _ in range(1, click_times + 1):
                    pyautogui.click(position, duration=duration)
        return True
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate the {image_path} on the screen." + RESET)
    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)

def show_dialog(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Bot Notification", 1)

# Bot sequence of tasks
def bot_cycle():
    while True:
        if locate_and_click(folder_location + 'claim.png', "Claim Button"):
            break
        elif locate_and_click(folder_location + 'key.png', "Key Button"):
            break
        elif locate_and_click(folder_location + 'close.png', "Close Button"):
            break
        elif (locate_and_click(folder_location + 'skip-all.png', 'Skip All Button', click=False) or locate_and_click(folder_location + 'skip-all-red.png', 'Red Skip All Button', click=False)):
            if locate_and_click(folder_location + 'disabled-choose-forward.png', "Disabled Choose Forward Button", set_confidence=0.90, click=False):
                show_dialog("Time to take a break!")
                show_options_dialog()
                break
            else:
                locate_and_click(folder_location + 'choose-forward.png', "Choose Forward Button", set_confidence=0.90)
            continue
        elif locate_and_click(folder_location + 'missing-dragon-rescue-text.png', 'Missing Dragon Rescue Text', click=False):
            break
        tasks = [
                (folder_location + 'ok.png', 'Ok Button'),
                (folder_location + 'start.png', 'Start Button'),
                (folder_location + 'tap-to-open.png', 'Tap To Open Text'),
            ]
        for task in tasks:
                locate_and_click(*task)

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

# Confirmation Message
confirmation = messagebox.askquestion(window_name, "Open " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. \n\nHave you followed everything?")

# Team Selection Dropdown
class TeamSelectionDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt):
        self.prompt = prompt
        super().__init__(parent, title)

    def body(self, master):
        self.team_selection_choices = [str(i) for i in range(1, 25)]
        self.var = tk.StringVar()
        self.var.set(self.team_selection_choices[0])

        tk.Label(master, text=self.prompt).pack()
        team_selection_dropdown = tk.OptionMenu(master, self.var, *self.team_selection_choices)
        team_selection_dropdown.pack()

    def apply(self):
        self.result = self.var.get()

selected_team_instance = TeamSelectionDialog(root, "Select Team", "Choose up to which nth team will fight first (This will pick a team away from the strongest):")
selected_team = selected_team_instance.result
if selected_team is not None:
    selected_team = int(selected_team)
else:
    selected_team = 0
    show_options_dialog()

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate 
while confirmation == 'yes':
    try:
        team_selected_executed = False 
        position = pyautogui.locateOnScreen(folder_location + 'missing-dragon-rescue-text.png', confidence=0.8)
        print(GREEN + f"{image_hint} is found at: {position}" + RESET)
        while position is not None:
            locate_and_click(folder_location + 'tap-to-open.png', 'Tap To Open Text')
            locate_and_click(folder_location + 'claim.png', "Claim Button")
            locate_and_click(folder_location + 'key.png', "Key Button")
            locate_and_click(folder_location + 'ok.png', 'Ok Button')
            locate_and_click(folder_location + 'start.png', 'Start Button')
            locate_and_click(folder_location + 'claim-end.png', 'Claim End Button')
            if locate_and_click(folder_location + 'new-rank.png', 'You Achieved A New Rank Text', click=False):
                locate_and_click(folder_location + 'close.png', "Close Button")
                continue
            elif locate_and_click(folder_location + 'rescue-over.png', 'Rescue Over Text', click=False):
                show_dialog("Congratulations, Rescue's Over!")
                show_options_dialog()
                break

            battle = locate_and_click(folder_location + 'battle.png', 'Battle Icon')
            while battle:
                if team_selected_executed is False: 
                    team_selected = locate_and_click(folder_location + 'choose-backward.png', 'Choose Backward Button', click_times=selected_team, duration=0.5, set_confidence=0.9)
                    while team_selected:
                        team_selected_executed = True
                        bot_cycle()
                        break
                elif team_selected_executed is True:
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