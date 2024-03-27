import subprocess
import os
import tkinter as tk
from tkinter import simpledialog,messagebox

options = ["Collect All Gold and Food", 
           "Watch DTV Ads", 
           "Watch Greenhouse Ads", 
           "League Auto Combat", 
           "Skip 6h Ads", 
           "Dragon Rescue Auto Combat", 
           "Unli Terra Breed",
           "Unli Terra Hatch", 
           "Arena Fight to Lose Points",]

class OptionDialog(simpledialog.Dialog):
    def __init__(self, parent, title, options, execute_func):
        self.options = options
        self.execute_func = execute_func
        self.dialog_closed = False  
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Master, ask me what to do. You can choose from the options below.").pack()

        self.var = tk.StringVar(master)
        self.var.set(self.options[0])  # Set the default option

        option_menu = tk.OptionMenu(master, self.var, *self.options)
        option_menu.pack()

    def apply(self):
        selected_option = self.var.get()
        if selected_option:
            self.execute_func(selected_option)
        else:
            self.dialog_closed = True

def show_options_dialog():
    root = tk.Tk()
    root.withdraw()

    dlg = OptionDialog(root, "Dragon City Bot", options, execute_selected_option)

    if dlg.dialog_closed:
        print("Options dialog closed thus closing the program.")
    else:
        print("Options dialog canceled thus closing the program.")

def execute_selected_option(selected_option):
    if selected_option == "Collect All Gold and Food":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "collect_gold_food_bot", "collect_gold_food_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Watch DTV Ads":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "watch_dtv_ad_bot", "watch_dtv_ad_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Watch Greenhouse Ads":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "watch_greenhouse_ad_bot", "watch_greenhouse_ad_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Skip 6h Ads":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "skip_6h_bot", "skip_6h_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "League Auto Combat":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "league_auto_combat_bot", "league_auto_combat_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Dragon Rescue Auto Combat":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "dragon_rescue_bot", "dragon_rescue_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Unli Terra Breed":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "terra_breed_bot", "terra_breed_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Unli Terra Hatch":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "terra_hatch_bot", "terra_hatch_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Arena Fight to Lose Points":  
        print(f"Selected: {selected_option}")
        script_path = os.path.join(os.path.dirname(__file__), "arena_auto_lose_bot", "arena_auto_lose_bot.py")
        subprocess.run(["python", script_path])
    else:
        print(f"Selected: Unknown Option")

# For testing
# if __name__ == '__main__':
#     show_options_dialog()