import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random
from PIL import Image, ImageTk
import re

class DiceRollerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("General RPG Dice Roller")
        self.root.geometry("950x800")  # Increased height for new features
        self.root.configure(bg="#121212")
        self.root.resizable(True, True)
        
        # Configure dark theme colors
        self.bg_color = "#121212"
        self.card_color = "#1e1e1e"
        self.text_color = "#e0e0e0"
        self.accent_color = "#bb86fc"
        self.critical_color = "#ff5252"
        self.success_color = "#69f0ae"
        self.warning_color = "#ffab40"
        
        # Initialize variables
        self.shadowrun_mode = tk.BooleanVar(value=False)
        self.opposed_roll = tk.BooleanVar(value=False)
        self.dice_history = []
        self.dice_buttons = []
        self.dice_selections = []  # Store multiple dice selections
        self.success_threshold = tk.IntVar(value=0)  # Success threshold
        
        # Create UI
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('.', background=self.bg_color, foreground=self.text_color)
        style.configure('TFrame', background=self.card_color)
        style.configure('TLabel', background=self.card_color, foreground=self.text_color)
        style.configure('TButton', background="#333333", foreground=self.text_color, 
                        borderwidth=1, focusthickness=3, focuscolor='none')
        style.map('TButton', background=[('active', '#424242'), ('disabled', '#2a2a2a')])
        style.configure('TCheckbutton', background=self.card_color, foreground=self.text_color)
        style.configure('TRadiobutton', background=self.card_color, foreground=self.text_color)
        style.configure('TEntry', fieldbackground="#333333", foreground=self.text_color)
        style.configure('TCombobox', fieldbackground="#333333", foreground=self.text_color)
        style.configure('TScrollbar', background="#333333")
        style.configure('Listbox', background="#333333", foreground=self.text_color)
        
        # Custom style for accent buttons
        style.configure('Accent.TButton', background=self.accent_color, foreground="#000000")
        style.map('Accent.TButton', 
                 background=[('active', '#d1b2ff'), ('disabled', '#7a5ca8')])
        
        # Custom style for card frames
        style.configure('Card.TFrame', background=self.card_color, 
                       borderwidth=1, relief='solid', bordercolor="#333333")
        
    def create_widgets(self):
        # Configure styles
        self.setup_styles()
        
        # Create main frames
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - controls
        left_frame = ttk.Frame(main_frame, width=300, style='Card.TFrame')
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        # Right panel - results
        right_frame = ttk.Frame(main_frame, style='Card.TFrame')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Control panel
        control_frame = ttk.Frame(left_frame, padding=10)
        control_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # Dice selection header
        ttk.Label(control_frame, text="DICE SELECTION", font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        
        # Dice buttons
        dice_frame = ttk.Frame(control_frame)
        dice_frame.grid(row=1, column=0, pady=5)
        
        dice_types = ["d4", "d6", "d8", "d10", "d12", "d20", "d100"]
        for i, dice in enumerate(dice_types):
            btn = ttk.Button(dice_frame, text=dice, width=4,
                            command=lambda d=dice: self.add_dice_selection(d))
            btn.grid(row=0, column=i, padx=2)
            self.dice_buttons.append(btn)
        
        # Quantity selection
        ttk.Label(control_frame, text="QUANTITY:", font=('Segoe UI', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        self.quantity_var = tk.IntVar(value=1)
        ttk.Spinbox(control_frame, from_=1, to=100, width=5, textvariable=self.quantity_var, 
                   font=('Segoe UI', 10)).grid(row=3, column=0, sticky=tk.W)
        
        # Selected dice list
        ttk.Label(control_frame, text="SELECTED DICE:", font=('Segoe UI', 9, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(10, 0))
        self.selected_list = tk.Listbox(control_frame, height=4, bg="#333333", fg=self.text_color,
                                      selectbackground=self.accent_color, selectforeground="#000000")
        self.selected_list.grid(row=5, column=0, sticky=tk.W+tk.E, pady=(0, 5))
        
        # Remove selected button
        remove_btn = ttk.Button(control_frame, text="REMOVE SELECTED", command=self.remove_selected_dice)
        remove_btn.grid(row=6, column=0, pady=(0, 10))
        
        # Modifier section
        ttk.Label(control_frame, text="MODIFIER:", font=('Segoe UI', 9, 'bold')).grid(row=7, column=0, sticky=tk.W)
        mod_frame = ttk.Frame(control_frame)
        mod_frame.grid(row=8, column=0, sticky=tk.W, pady=(0, 10))
        self.modifier_var = tk.IntVar(value=0)
        ttk.Button(mod_frame, text="-", width=2, 
                  command=lambda: self.modifier_var.set(self.modifier_var.get() - 1)).pack(side=tk.LEFT)
        ttk.Entry(mod_frame, width=5, textvariable=self.modifier_var, justify=tk.CENTER, 
                 font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        ttk.Button(mod_frame, text="+", width=2, 
                  command=lambda: self.modifier_var.set(self.modifier_var.get() + 1)).pack(side=tk.LEFT)
        
        # Success threshold
        ttk.Label(control_frame, text="SUCCESS THRESHOLD:", font=('Segoe UI', 9, 'bold')).grid(row=9, column=0, sticky=tk.W, pady=(10, 0))
        threshold_frame = ttk.Frame(control_frame)
        threshold_frame.grid(row=10, column=0, sticky=tk.W, pady=(0, 10))
        ttk.Entry(threshold_frame, width=5, textvariable=self.success_threshold, 
                 font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(threshold_frame, text="(0 = disabled)", font=('Segoe UI', 8)).pack(side=tk.LEFT)
        
        # Options frame
        options_frame = ttk.Frame(control_frame)
        options_frame.grid(row=11, column=0, sticky=tk.W+tk.E, pady=(10, 0))
        
        # Shadowrun mode
        shadowrun_frame = ttk.Frame(options_frame)
        shadowrun_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(shadowrun_frame, text="Shadowrun Mode", variable=self.shadowrun_mode,
                       command=self.toggle_shadowrun).pack(side=tk.LEFT)
        
        # Opposed roll
        opposed_frame = ttk.Frame(options_frame)
        opposed_frame.pack(fill=tk.X, pady=5)
        ttk.Checkbutton(opposed_frame, text="Opposed Roll", variable=self.opposed_roll,
                       command=self.toggle_opposed).pack(side=tk.LEFT)
        
        # Opponent modifier (only shown when opposed roll is enabled)
        self.opponent_frame = ttk.Frame(control_frame)
        ttk.Label(self.opponent_frame, text="OPPONENT MODIFIER:", font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky=tk.W)
        opp_mod_frame = ttk.Frame(self.opponent_frame)
        opp_mod_frame.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        self.opp_modifier_var = tk.IntVar(value=0)
        ttk.Button(opp_mod_frame, text="-", width=2, 
                  command=lambda: self.opp_modifier_var.set(self.opp_modifier_var.get() - 1)).pack(side=tk.LEFT)
        ttk.Entry(opp_mod_frame, width=5, textvariable=self.opp_modifier_var, justify=tk.CENTER, 
                 font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=5)
        ttk.Button(opp_mod_frame, text="+", width=2, 
                  command=lambda: self.opp_modifier_var.set(self.opp_modifier_var.get() + 1)).pack(side=tk.LEFT)
        
        # Action buttons
        action_frame = ttk.Frame(control_frame)
        action_frame.grid(row=13, column=0, sticky=tk.W+tk.E, pady=(15, 0))
        
        roll_btn = ttk.Button(action_frame, text="ROLL DICE", command=self.roll_dice, 
                             style='Accent.TButton')
        roll_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(action_frame, text="CLEAR", command=self.clear_results)
        clear_btn.pack(side=tk.LEFT)
        
        # Results display
        results_header = ttk.Frame(right_frame)
        results_header.pack(fill=tk.X, padx=10, pady=(10, 0))
        ttk.Label(results_header, text="RESULTS", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        
        self.results_text = scrolledtext.ScrolledText(
            right_frame, wrap=tk.WORD, bg=self.card_color, fg=self.text_color,
            font=('Consolas', 11), padx=15, pady=15, state=tk.DISABLED
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure tags for coloring
        self.results_text.tag_configure("critical", foreground=self.success_color)
        self.results_text.tag_configure("failure", foreground=self.critical_color)
        self.results_text.tag_configure("shadowrun_success", foreground=self.success_color)
        self.results_text.tag_configure("shadowrun_fail", foreground=self.critical_color)
        self.results_text.tag_configure("glitch", foreground=self.warning_color)
        self.results_text.tag_configure("header", font=('Segoe UI', 11, 'bold'))
        self.results_text.tag_configure("subheader", font=('Segoe UI', 10, 'bold'))
        self.results_text.tag_configure("total", font=('Segoe UI', 10, 'bold'))
        self.results_text.tag_configure("opponent", foreground="#ff9800")
        self.results_text.tag_configure("player", foreground="#4fc3f7")
        self.results_text.tag_configure("winner", font=('Segoe UI', 11, 'bold'), foreground=self.success_color)
        self.results_text.tag_configure("loser", font=('Segoe UI', 11, 'bold'), foreground=self.critical_color)
        self.results_text.tag_configure("success", foreground=self.success_color)
        self.results_text.tag_configure("fail", foreground=self.critical_color)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready to roll")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Initialize
        self.toggle_opposed()
    
    def add_dice_selection(self, dice_type):
        if self.shadowrun_mode.get():
            return  # Disable dice selection in Shadowrun mode
        
        quantity = self.quantity_var.get()
        self.dice_selections.append((dice_type, quantity))
        self.selected_list.insert(tk.END, f"{quantity}{dice_type}")
        self.status_var.set(f"Added: {quantity}{dice_type}")
    
    def remove_selected_dice(self):
        selected = self.selected_list.curselection()
        if selected:
            index = selected[0]
            self.dice_selections.pop(index)
            self.selected_list.delete(index)
            self.status_var.set("Dice selection removed")
    
    def toggle_shadowrun(self):
        if self.shadowrun_mode.get():
            # Disable dice buttons and clear selections
            for btn in self.dice_buttons:
                btn.state(['disabled'])
            self.dice_selections = []
            self.selected_list.delete(0, tk.END)
            self.status_var.set("Shadowrun mode enabled - rolling d6s")
        else:
            # Enable dice buttons
            for btn in self.dice_buttons:
                btn.state(['!disabled'])
            self.status_var.set("Shadowrun mode disabled")
    
    def toggle_opposed(self):
        if self.opposed_roll.get():
            self.opponent_frame.grid(row=12, column=0, sticky=tk.W, pady=(10, 0))
        else:
            self.opponent_frame.grid_forget()
    
    def roll_dice(self):
        # Clear previous results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        
        # Handle Shadowrun mode
        if self.shadowrun_mode.get():
            self.roll_shadowrun()
        else:
            self.roll_standard()
        
        self.results_text.config(state=tk.DISABLED)
    
    def roll_standard(self):
        modifier = self.modifier_var.get()
        threshold = self.success_threshold.get()
        opposed = self.opposed_roll.get()
        opp_modifier = self.opp_modifier_var.get() if opposed else 0
        
        # Player roll
        player_total = 0
        player_rolls = []
        criticals = {"success": False, "failure": False}
        
        # Roll all selected dice
        for dice_type, quantity in self.dice_selections:
            sides = int(dice_type[1:])
            
            for _ in range(quantity):
                roll = random.randint(1, sides)
                player_total += roll
                player_rolls.append((dice_type, roll))
                
                # Check for criticals
                if roll == 1:
                    criticals["failure"] = True
                elif roll == sides:
                    criticals["success"] = True
        
        player_total += modifier
        
        # Display player results
        self.results_text.insert(tk.END, "PLAYER ROLL:\n", "header")
        self.results_text.insert(tk.END, f"Rolling: {', '.join([f'{q}{t}' for t, q in self.dice_selections])} + {modifier}\n\n", "subheader")
        
        # Display individual rolls
        self.results_text.insert(tk.END, "Rolls: ")
        for dice_type, roll in player_rolls:
            sides = int(dice_type[1:])
            if roll == 1:
                self.results_text.insert(tk.END, f"{roll} ", "failure")
            elif roll == sides:
                self.results_text.insert(tk.END, f"{roll} ", "critical")
            else:
                self.results_text.insert(tk.END, f"{roll} ")
        
        # Add modifier information
        if modifier != 0:
            self.results_text.insert(tk.END, f"\nModifier: {'+' if modifier >= 0 else ''}{modifier}\n")
        
        self.results_text.insert(tk.END, f"\nTotal: {player_total}", "total")
        
        # Add critical notifications
        if criticals["success"] and criticals["failure"]:
            self.results_text.insert(tk.END, " - Mixed Criticals!\n", "total")
        elif criticals["success"]:
            self.results_text.insert(tk.END, " - Critical Success!\n", "critical")
        elif criticals["failure"]:
            self.results_text.insert(tk.END, " - Critical Failure!\n", "failure")
        else:
            self.results_text.insert(tk.END, "\n")
        
        # Check success threshold (non-opposed only)
        if not opposed and threshold > 0:
            self.results_text.insert(tk.END, "\nSUCCESS CHECK:\n", "header")
            if player_total >= threshold:
                self.results_text.insert(tk.END, f"SUCCESS! ({player_total} >= {threshold})\n", "success")
            else:
                self.results_text.insert(tk.END, f"FAILURE! ({player_total} < {threshold})\n", "fail")
        
        # Opponent roll if needed
        if opposed:
            self.results_text.insert(tk.END, "\n\nOPPONENT ROLL:\n", "header")
            self.results_text.insert(tk.END, f"Rolling: {', '.join([f'{q}{t}' for t, q in self.dice_selections])} + {opp_modifier}\n\n", "subheader")
            
            # Opponent rolls the same dice as player
            opponent_total = 0
            opponent_rolls = []
            opp_criticals = {"success": False, "failure": False}
            
            for dice_type, quantity in self.dice_selections:
                sides = int(dice_type[1:])
                
                for _ in range(quantity):
                    roll = random.randint(1, sides)
                    opponent_total += roll
                    opponent_rolls.append((dice_type, roll))
                    
                    # Check for criticals
                    if roll == 1:
                        opp_criticals["failure"] = True
                    elif roll == sides:
                        opp_criticals["success"] = True
            
            opponent_total += opp_modifier
            
            # Display opponent rolls
            self.results_text.insert(tk.END, "Rolls: ")
            for dice_type, roll in opponent_rolls:
                sides = int(dice_type[1:])
                if roll == 1:
                    self.results_text.insert(tk.END, f"{roll} ", "failure")
                elif roll == sides:
                    self.results_text.insert(tk.END, f"{roll} ", "critical")
                else:
                    self.results_text.insert(tk.END, f"{roll} ")
            
            if opp_modifier != 0:
                self.results_text.insert(tk.END, f"\nModifier: {'+' if opp_modifier >= 0 else ''}{opp_modifier}\n")
            
            self.results_text.insert(tk.END, f"\nTotal: {opponent_total}\n", "total")
            
            # Add critical notifications for opponent
            if opp_criticals["success"] and opp_criticals["failure"]:
                self.results_text.insert(tk.END, " - Mixed Criticals!\n", "total")
            elif opp_criticals["success"]:
                self.results_text.insert(tk.END, " - Critical Success!\n", "critical")
            elif opp_criticals["failure"]:
                self.results_text.insert(tk.END, " - Critical Failure!\n", "failure")
            
            # Compare results
            self.results_text.insert(tk.END, "\n\nRESULT:\n", "header")
            if player_total > opponent_total:
                self.results_text.insert(tk.END, "PLAYER WINS!\n", "winner")
            elif player_total < opponent_total:
                self.results_text.insert(tk.END, "OPPONENT WINS!\n", "loser")
            else:
                self.results_text.insert(tk.END, "TIE!\n", "total")
    
    def roll_shadowrun(self):
        quantity = self.quantity_var.get()
        modifier = self.modifier_var.get()
        threshold = self.success_threshold.get()
        total_dice = quantity + modifier
        opposed = self.opposed_roll.get()
        opp_modifier = self.opp_modifier_var.get() if opposed else 0
        
        if total_dice <= 0:
            self.results_text.insert(tk.END, "Invalid dice pool size!\n", "failure")
            return
        
        # Player roll
        player_rolls = [random.randint(1, 6) for _ in range(total_dice)]
        player_successes = sum(1 for roll in player_rolls if roll >= 5)
        player_failures = sum(1 for roll in player_rolls if roll == 1)
        player_glitch = player_failures > total_dice / 2
        
        # Display player results
        self.results_text.insert(tk.END, "PLAYER ROLL:\n", "header")
        self.results_text.insert(tk.END, f"Rolling: {total_dice}d6 (Base: {quantity} + Mod: {modifier})\n\n", "subheader")
        
        # Display individual dice
        self.results_text.insert(tk.END, "Rolls: ")
        for roll in player_rolls:
            if roll >= 5:
                self.results_text.insert(tk.END, f"{roll} ", "shadowrun_success")
            elif roll == 1:
                self.results_text.insert(tk.END, f"{roll} ", "shadowrun_fail")
            else:
                self.results_text.insert(tk.END, f"{roll} ")
        
        # Display results
        self.results_text.insert(tk.END, "\n\n")
        self.results_text.insert(tk.END, f"Successes: {player_successes}\n", "shadowrun_success")
        self.results_text.insert(tk.END, f"Failures: {player_failures}\n", "shadowrun_fail")
        self.results_text.insert(tk.END, f"Net Hits: {player_successes}\n", "total")
        
        # Check success threshold (non-opposed only)
        if not opposed and threshold > 0:
            self.results_text.insert(tk.END, "\nSUCCESS CHECK:\n", "header")
            if player_successes >= threshold:
                self.results_text.insert(tk.END, f"SUCCESS! ({player_successes} >= {threshold} successes)\n", "success")
            else:
                self.results_text.insert(tk.END, f"FAILURE! ({player_successes} < {threshold} successes)\n", "fail")
        
        # Add glitch notification
        if player_glitch:
            if player_successes == 0:
                self.results_text.insert(tk.END, "\nCRITICAL GLITCH!\n", "glitch")
                self.results_text.insert(tk.END, "Failure with complications\n", "failure")
            else:
                self.results_text.insert(tk.END, "\nGLITCH!\n", "glitch")
                self.results_text.insert(tk.END, "Success with complications\n")
        
        # Opponent roll if needed
        if opposed:
            opp_quantity = self.quantity_var.get()  # Same as player for simplicity
            opp_total_dice = opp_quantity + opp_modifier
            
            if opp_total_dice <= 0:
                self.results_text.insert(tk.END, "\nInvalid opponent dice pool size!\n", "failure")
                return
            
            opp_rolls = [random.randint(1, 6) for _ in range(opp_total_dice)]
            opp_successes = sum(1 for roll in opp_rolls if roll >= 5)
            opp_failures = sum(1 for roll in opp_rolls if roll == 1)
            opp_glitch = opp_failures > opp_total_dice / 2
            
            # Display opponent results
            self.results_text.insert(tk.END, "\n\nOPPONENT ROLL:\n", "header")
            self.results_text.insert(tk.END, f"Rolling: {opp_total_dice}d6 (Base: {opp_quantity} + Mod: {opp_modifier})\n\n", "subheader")
            
            # Display individual dice
            self.results_text.insert(tk.END, "Rolls: ")
            for roll in opp_rolls:
                if roll >= 5:
                    self.results_text.insert(tk.END, f"{roll} ", "shadowrun_success")
                elif roll == 1:
                    self.results_text.insert(tk.END, f"{roll} ", "shadowrun_fail")
                else:
                    self.results_text.insert(tk.END, f"{roll} ")
            
            # Display results
            self.results_text.insert(tk.END, "\n\n")
            self.results_text.insert(tk.END, f"Successes: {opp_successes}\n", "shadowrun_success")
            self.results_text.insert(tk.END, f"Failures: {opp_failures}\n", "shadowrun_fail")
            self.results_text.insert(tk.END, f"Net Hits: {opp_successes}\n", "total")
            
            # Add glitch notification for opponent
            if opp_glitch:
                if opp_successes == 0:
                    self.results_text.insert(tk.END, "\nOPPONENT CRITICAL GLITCH!\n", "glitch")
                else:
                    self.results_text.insert(tk.END, "\nOPPONENT GLITCH!\n", "glitch")
            
            # Compare results
            self.results_text.insert(tk.END, "\n\nRESULT:\n", "header")
            net_difference = player_successes - opp_successes
            
            if net_difference > 0:
                self.results_text.insert(tk.END, f"PLAYER WINS by {net_difference} hit{'s' if net_difference > 1 else ''}!\n", "winner")
            elif net_difference < 0:
                self.results_text.insert(tk.END, f"OPPONENT WINS by {-net_difference} hit{'s' if -net_difference > 1 else ''}!\n", "loser")
            else:
                self.results_text.insert(tk.END, "TIE!\n", "total")
    
    def clear_results(self):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Results cleared\n", "header")
        self.results_text.config(state=tk.DISABLED)
        self.status_var.set("Results cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = DiceRollerApp(root)
    root.mainloop()
