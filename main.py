import tkinter as tk
from tkinter import messagebox
from options import show_options_dialog
import pyautogui
import sys

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Step 1: Open a Dialogue for Dragon City Bot instructions
root = tk.Tk()
root.withdraw()

confirmation = messagebox.askquestion("Dragon City Bot", "Open Dragon City and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. \n\nHave you followed everything?")

root.destroy()

if confirmation == 'no':
    print("Closing the program.")
    sys.exit()

# Step 2: Attempt to locate the Dragon City icon
while confirmation == 'yes':
    try:
        position = pyautogui.locateOnScreen('dragoncity-icon.png', confidence=0.8)
        if position is not None:
            print(GREEN + f"Dragon City Icon is found at: {position}" + RESET)

            # Import and call options related functions
            show_options_dialog()
            break
    except pyautogui.ImageNotFoundException:
        print(RED + "Could not locate Dragon City Icon." + RESET)
        answer = messagebox.askyesno("Dragon City Bot", "Are you sure Dragon City is open?\n\n"
                                                        "Open Dragon City and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. \n\n"
                                                        "Would you like to try scanning again?")
        if not answer:
            print("Exiting the program.")
            break
        else:
            print("Searching for the Dragon City Icon...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
