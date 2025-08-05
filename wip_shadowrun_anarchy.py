import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from PIL import Image, ImageTk
import json
import os

class ShadowrunCharacter:
    def __init__(self):
        self.name = "New Runner"
        self.metatype = "Human"
        self.role = "Street Samurai"
        self.age = 25
        self.reputation = 0
        self.heat = 0
        self.karma = 0
        self.nuyen = 5000
        self.edge = 2
        self.background = ""
        
        # Attributes with base values
        self.attributes = {
            "Body": 3, "Agility": 3, "Reaction": 3, "Strength": 3,
            "Willpower": 3, "Logic": 3, "Intuition": 3, "Charisma": 3,
            "Edge": 2, "Magic": 0, "Resonance": 0
        }
        
        # Derived attributes
        self.physical_track = 0
        self.stun_track = 0
        self.condition_monitor = {"Physical": 0, "Stun": 0}
        self.initiative = 0
        self.initiative_dice = 0
        self.damage_resistance = 0
        
        # Qualities
        self.qualities = {
            "Positive": [],
            "Negative": []
        }
        
        # Skills
        self.skills = {
            "Combat": {"Archery": 0, "Automatics": 0, "Blades": 0, "Clubs": 0, "Heavy Weapons": 0,
                      "Longarms": 0, "Pistols": 0, "Throwing Weapons": 0, "Unarmed Combat": 0},
            "Physical": {"Animal Handling": 0, "Artisan": 0, "Athletics": 0, "Con": 0, "Disguise": 0,
                        "Escape Artist": 0, "Etiquette": 0, "First Aid": 0, "Forgery": 0},
            "Social": {"Hacking": 0, "Hardware": 0, "Gymnastics": 0, "Intimidation": 0, "Leadership": 0,
                      "Negotiation": 0, "Perception": 0, "Performance": 0},
            "Vehicle": {"Pilot Ground Craft": 0, "Pilot Watercraft": 0, "Pilot Aircraft": 0,
                       "Pilot Walker": 0, "Pilot Exotic": 0, "Navigation": 0},
            "Magical": {"Alchemy": 0, "Arcana": 0, "Artificing": 0, "Assensing": 0, "Astral Combat": 0,
                       "Banishing": 0, "Binding": 0, "Counterspelling": 0, "Disenchanting": 0, "Ritual Spellcasting": 0,
                       "Spellcasting": 0, "Summoning": 0, "Tracking": 0},
            "Technical": {"Biotech": 0, "Chemistry": 0, "Computer": 0, "Cybercombat": 0, "Demolitions": 0,
                         "Electronic Warfare": 0, "Hardware": 0, "Software": 0, "Locksmith": 0, "Palming": 0,
                         "Perception": 0, "Running": 0, "Swimming": 0, "Tracking": 0}
        }
        
        # Gear inventory
        self.gear = []
        self.amps = []
        self.weapons = []
        self.armor = []
        self.cyberware = []
        
        # Combat state
        self.in_combat = False
        self.combat_turn = 0
        self.current_initiative = 0
        self.active_effects = []
        
        self.calculate_derived_attributes()
    
    def calculate_derived_attributes(self):
        # Physical track = Body + 8
        self.physical_track = self.attributes["Body"] + 8
        
        # Stun track = Willpower + 8
        self.stun_track = self.attributes["Willpower"] + 8
        
        # Initiative = Reaction + Intuition
        self.initiative = self.attributes["Reaction"] + self.attributes["Intuition"]
        
        # Damage resistance = Body + Armor rating
        armor_rating = sum([item.get("armor", 0) for item in self.armor if item.get("equipped", False)])
        self.damage_resistance = self.attributes["Body"] + armor_rating
        
        # Initiative dice (1 by default, more with certain amps)
        self.initiative_dice = 1
        for amp in self.amps:
            if amp.get("type") == "Initiative" and amp.get("equipped", False):
                self.initiative_dice += amp.get("dice", 0)
    
    def add_quality(self, quality, quality_type):
        if quality_type == "Positive":
            if quality not in self.qualities["Positive"]:
                self.qualities["Positive"].append(quality)
        else:
            if quality not in self.qualities["Negative"]:
                self.qualities["Negative"].append(quality)
    
    def remove_quality(self, quality, quality_type):
        if quality_type == "Positive":
            if quality in self.qualities["Positive"]:
                self.qualities["Positive"].remove(quality)
        else:
            if quality in self.qualities["Negative"]:
                self.qualities["Negative"].remove(quality)
    
    def add_gear(self, gear_item):
        self.gear.append(gear_item)
    
    def remove_gear(self, gear_item):
        if gear_item in self.gear:
            self.gear.remove(gear_item)
    
    def add_amp(self, amp_item):
        self.amps.append(amp_item)
    
    def remove_amp(self, amp_item):
        if amp_item in self.amps:
            self.amps.remove(amp_item)
    
    def add_weapon(self, weapon):
        self.weapons.append(weapon)
    
    def remove_weapon(self, weapon):
        if weapon in self.weapons:
            self.weapons.remove(weapon)
    
    def add_armor(self, armor_item):
        self.armor.append(armor_item)
    
    def remove_armor(self, armor_item):
        if armor_item in self.armor:
            self.armor.remove(armor_item)
    
    def add_cyberware(self, cyberware_item):
        self.cyberware.append(cyberware_item)
    
    def remove_cyberware(self, cyberware_item):
        if cyberware_item in self.cyberware:
            self.cyberware.remove(cyberware_item)
    
    def apply_damage(self, damage_type, amount):
        if damage_type == "Physical":
            self.condition_monitor["Physical"] += amount
            if self.condition_monitor["Physical"] >= self.physical_track:
                self.condition_monitor["Physical"] = self.physical_track
                # Character is dead
        else:  # Stun damage
            self.condition_monitor["Stun"] += amount
            if self.condition_monitor["Stun"] >= self.stun_track:
                self.condition_monitor["Stun"] = self.stun_track
                # Character is unconscious
    
    def use_medkit(self, medkit):
        if medkit in self.gear:
            rating = medkit.get("rating", 3)
            healing = min(rating, self.condition_monitor["Physical"])
            self.condition_monitor["Physical"] -= healing
            # Medkit has limited uses
            medkit["uses"] = medkit.get("uses", rating) - 1
            if medkit["uses"] <= 0:
                self.gear.remove(medkit)
            return healing
        return 0
    
    def roll_dice(self, pool, bonus=0, edge_spent=0, wild_die=False):
        # Calculate final dice pool
        final_pool = pool + bonus
        
        # Cap dice pool at 20 for balance
        final_pool = min(final_pool, 20)
        
        # Roll the dice
        rolls = [random.randint(1, 6) for _ in range(final_pool)]
        
        # Handle edge spending
        if edge_spent > 0 and self.edge >= edge_spent:
            self.edge -= edge_spent
            # Add extra dice for edge spent
            rolls.extend([6] * edge_spent)
        
        # Handle wild die
        if wild_die:
            wild_roll = random.randint(1, 6)
            rolls.append(wild_roll)
            # If wild die is 1, it cancels a hit; if 6, it adds an extra hit
            if wild_roll == 1:
                # Remove one hit if available
                if 5 in rolls or 6 in rolls:
                    rolls.remove(max([r for r in rolls if r >= 5], default=0))
            elif wild_roll == 6:
                # Add an extra hit
                rolls.append(6)
        
        # Calculate hits (5 or 6 is a hit)
        hits = sum(1 for roll in rolls if roll >= 5)
        
        # Check for glitch (more than half the dice show 1)
        glitch = False
        if sum(1 for roll in rolls if roll == 1) > len(rolls) / 2:
            glitch = True
        
        return {
            "rolls": rolls,
            "hits": hits,
            "glitch": glitch,
            "pool": final_pool
        }
    
    def roll_initiative(self):
        initiative_roll = sum(random.randint(1, 6) for _ in range(self.initiative_dice))
        self.current_initiative = self.initiative + initiative_roll
        return self.current_initiative
    
    def save_character(self, filename):
        data = {
            "name": self.name,
            "metatype": self.metatype,
            "role": self.role,
            "attributes": self.attributes,
            "qualities": self.qualities,
            "skills": self.skills,
            "gear": self.gear,
            "amps": self.amps,
            "weapons": self.weapons,
            "armor": self.armor,
            "cyberware": self.cyberware,
            "background": self.background,
            "age": self.age,
            "reputation": self.reputation,
            "heat": self.heat,
            "edge": self.edge,
            "nuyen": self.nuyen,
            "karma": self.karma,
            "condition_monitor": self.condition_monitor
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_character(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.name = data.get("name", "New Runner")
            self.metatype = data.get("metatype", "Human")
            self.role = data.get("role", "Street Samurai")
            self.attributes = data.get("attributes", self.attributes)
            self.qualities = data.get("qualities", self.qualities)
            self.skills = data.get("skills", self.skills)
            self.gear = data.get("gear", [])
            self.amps = data.get("amps", [])
            self.weapons = data.get("weapons", [])
            self.armor = data.get("armor", [])
            self.cyberware = data.get("cyberware", [])
            self.background = data.get("background", "")
            self.age = data.get("age", 25)
            self.reputation = data.get("reputation", 0)
            self.heat = data.get("heat", 0)
            self.edge = data.get("edge", 2)
            self.nuyen = data.get("nuyen", 5000)
            self.karma = data.get("karma", 0)
            self.condition_monitor = data.get("condition_monitor", {"Physical": 0, "Stun": 0})
            
            self.calculate_derived_attributes()
            return True
        except:
            return False


class ShadowrunApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shadowrun: Anarchy Gameplay Assistant")
        self.geometry("1200x800")
        self.configure(bg="#1e1e1e")
        
        # Initialize character
        self.character = ShadowrunCharacter()
        
        # Create style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background='#2d2d2d', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#2d2d2d', foreground='#cccccc', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#4a6584')], foreground=[('selected', 'white')])
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TLabel', background='#2d2d2d', foreground='#cccccc', font=('Arial', 10))
        self.style.configure('TButton', background='#4a6584', foreground='white', font=('Arial', 10), borderwidth=1)
        self.style.map('TButton', background=[('active', '#5a7da4')])
        self.style.configure('TEntry', fieldbackground='#3a3a3a', foreground='white')
        self.style.configure('TCombobox', fieldbackground='#3a3a3a', foreground='white')
        self.style.configure('TScrollbar', background='#3a3a3a')
        self.style.configure('Treeview', background='#3a3a3a', foreground='white', fieldbackground='#3a3a3a')
        self.style.map('Treeview', background=[('selected', '#4a6584')])
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_character_tab()
        self.create_skills_tab()
        self.create_gear_tab()
        self.create_combat_tab()
        self.create_background_tab()
        self.create_dice_tab()
        
        # Status bar
        self.status_bar = tk.Label(self, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                                 bg='#2d2d2d', fg='#cccccc')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Menu
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0, bg='#2d2d2d', fg='white')
        file_menu.add_command(label="New Character", command=self.new_character)
        file_menu.add_command(label="Load Character", command=self.load_character)
        file_menu.add_command(label="Save Character", command=self.save_character)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(self.menu_bar, tearoff=0, bg='#2d2d2d', fg='white')
        edit_menu.add_command(label="Add Gear", command=self.add_gear_dialog)
        edit_menu.add_command(label="Add Amp", command=self.add_amp_dialog)
        self.menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        self.update_status("Shadowrun: Anarchy Gameplay Assistant Ready")
    
    def update_status(self, message):
        self.status_bar.config(text=message)
    
    def new_character(self):
        self.character = ShadowrunCharacter()
        self.update_character_tab()
        self.update_skills_tab()
        self.update_gear_tab()
        self.update_background_tab()
        self.update_status("New character created")
    
    def load_character(self):
        # In a real app, you'd implement file dialog
        if self.character.load_character("character.json"):
            self.update_character_tab()
            self.update_skills_tab()
            self.update_gear_tab()
            self.update_background_tab()
            self.update_status("Character loaded successfully")
        else:
            messagebox.showerror("Error", "Failed to load character")
    
    def save_character(self):
        self.character.save_character("character.json")
        self.update_status("Character saved successfully")
    
    def add_gear_dialog(self):
        # Simplified for this example
        gear_dialog = tk.Toplevel(self)
        gear_dialog.title("Add Gear")
        gear_dialog.geometry("300x200")
        gear_dialog.configure(bg="#2d2d2d")
        
        tk.Label(gear_dialog, text="Gear Name:", bg="#2d2d2d", fg="#cccccc").pack(pady=5)
        name_entry = ttk.Entry(gear_dialog)
        name_entry.pack(pady=5, fill=tk.X, padx=20)
        
        tk.Label(gear_dialog, text="Rating:", bg="#2d2d2d", fg="#cccccc").pack(pady=5)
        rating_entry = ttk.Entry(gear_dialog)
        rating_entry.pack(pady=5, fill=tk.X, padx=20)
        
        def add_gear():
            name = name_entry.get()
            rating = rating_entry.get()
            if name:
                self.character.add_gear({"name": name, "rating": int(rating) if rating.isdigit() else 0})
                self.update_gear_tab()
                gear_dialog.destroy()
        
        ttk.Button(gear_dialog, text="Add", command=add_gear).pack(pady=10)
    
    def add_amp_dialog(self):
        amp_dialog = tk.Toplevel(self)
        amp_dialog.title("Add Amp")
        amp_dialog.geometry("300x250")
        amp_dialog.configure(bg="#2d2d2d")
        
        tk.Label(amp_dialog, text="Amp Name:", bg="#2d2d2d", fg="#cccccc").pack(pady=5)
        name_entry = ttk.Entry(amp_dialog)
        name_entry.pack(pady=5, fill=tk.X, padx=20)
        
        tk.Label(amp_dialog, text="Type:", bg="#2d2d2d", fg="#cccccc").pack(pady=5)
        type_combobox = ttk.Combobox(amp_dialog, values=["Combat", "Magic", "Resonance", "Skill", "Initiative"])
        type_combobox.pack(pady=5, fill=tk.X, padx=20)
        type_combobox.set("Combat")
        
        tk.Label(amp_dialog, text="Bonus:", bg="#2d2d2d", fg="#cccccc").pack(pady=5)
        bonus_entry = ttk.Entry(amp_dialog)
        bonus_entry.pack(pady=5, fill=tk.X, padx=20)
        
        def add_amp():
            name = name_entry.get()
            amp_type = type_combobox.get()
            bonus = bonus_entry.get()
            if name:
                self.character.add_amp({"name": name, "type": amp_type, "bonus": int(bonus) if bonus.isdigit() else 0})
                self.update_gear_tab()
                amp_dialog.destroy()
        
        ttk.Button(amp_dialog, text="Add", command=add_amp).pack(pady=10)
    
    def create_character_tab(self):
        self.char_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.char_tab, text="Character")
        
        # Left frame for attributes
        left_frame = ttk.Frame(self.char_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(left_frame, text="Attributes", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        # Create attribute controls
        self.attribute_vars = {}
        self.attribute_controls = {}
        
        for attr in self.character.attributes:
            frame = ttk.Frame(left_frame)
            frame.pack(fill=tk.X, pady=2)
            
            lbl = ttk.Label(frame, text=f"{attr}:", width=12, anchor=tk.W)
            lbl.pack(side=tk.LEFT)
            
            var = tk.IntVar(value=self.character.attributes[attr])
            self.attribute_vars[attr] = var
            
            spinbox = ttk.Spinbox(frame, from_=1, to=10, width=5, textvariable=var, 
                                command=lambda a=attr: self.update_attribute(a))
            spinbox.pack(side=tk.LEFT, padx=5)
            
            # Display attribute value
            val_lbl = ttk.Label(frame, text=str(self.character.attributes[attr]), width=3)
            val_lbl.pack(side=tk.LEFT)
            
            self.attribute_controls[attr] = (spinbox, val_lbl)
        
        # Metatype selection
        ttk.Label(left_frame, text="Metatype:", font=("Arial", 10)).pack(anchor=tk.W, pady=(20, 5))
        self.metatype_var = tk.StringVar(value=self.character.metatype)
        metatype_cb = ttk.Combobox(left_frame, textvariable=self.metatype_var, 
                                  values=["Human", "Elf", "Dwarf", "Ork", "Troll", "Other"])
        metatype_cb.pack(fill=tk.X, pady=5)
        metatype_cb.bind("<<ComboboxSelected>>", self.update_metatype)
        
        # Role selection
        ttk.Label(left_frame, text="Role:", font=("Arial", 10)).pack(anchor=tk.W, pady=(20, 5))
        self.role_var = tk.StringVar(value=self.character.role)
        role_cb = ttk.Combobox(left_frame, textvariable=self.role_var, 
                              values=["Street Samurai", "Decker", "Rigger", "Mage", "Shaman", 
                                      "Face", "Adept", "Technomancer", "Mystic Adept"])
        role_cb.pack(fill=tk.X, pady=5)
        role_cb.bind("<<ComboboxSelected>>", self.update_role)
        
        # Right frame for derived attributes and qualities
        right_frame = ttk.Frame(self.char_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Derived attributes
        ttk.Label(right_frame, text="Derived Attributes", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        derived_frame = ttk.Frame(right_frame)
        derived_frame.pack(fill=tk.X, pady=5)
        
        self.physical_track_var = tk.StringVar(value=f"Physical Track: {self.character.physical_track}")
        ttk.Label(derived_frame, textvariable=self.physical_track_var).pack(anchor=tk.W)
        
        self.stun_track_var = tk.StringVar(value=f"Stun Track: {self.character.stun_track}")
        ttk.Label(derived_frame, textvariable=self.stun_track_var).pack(anchor=tk.W)
        
        self.initiative_var = tk.StringVar(value=f"Initiative: {self.character.initiative}")
        ttk.Label(derived_frame, textvariable=self.initiative_var).pack(anchor=tk.W)
        
        self.damage_resistance_var = tk.StringVar(value=f"Damage Resistance: {self.character.damage_resistance}")
        ttk.Label(derived_frame, textvariable=self.damage_resistance_var).pack(anchor=tk.W)
        
        # Condition Monitor
        ttk.Label(right_frame, text="Condition Monitor", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        cond_frame = ttk.Frame(right_frame)
        cond_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cond_frame, text="Physical:").grid(row=0, column=0, sticky=tk.W)
        self.physical_damage_var = tk.StringVar(value=f"{self.character.condition_monitor['Physical']}/{self.character.physical_track}")
        ttk.Label(cond_frame, textvariable=self.physical_damage_var).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(cond_frame, text="Stun:").grid(row=1, column=0, sticky=tk.W)
        self.stun_damage_var = tk.StringVar(value=f"{self.character.condition_monitor['Stun']}/{self.character.stun_track}")
        ttk.Label(cond_frame, textvariable=self.stun_damage_var).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Qualities
        ttk.Label(right_frame, text="Qualities", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        qualities_frame = ttk.Frame(right_frame)
        qualities_frame.pack(fill=tk.BOTH, expand=True)
        
        # Positive qualities
        pos_frame = ttk.LabelFrame(qualities_frame, text="Positive Qualities")
        pos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.pos_qualities_list = tk.Listbox(pos_frame, bg="#3a3a3a", fg="white", selectbackground="#4a6584")
        self.pos_qualities_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Negative qualities
        neg_frame = ttk.LabelFrame(qualities_frame, text="Negative Qualities")
        neg_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.neg_qualities_list = tk.Listbox(neg_frame, bg="#3a3a3a", fg="white", selectbackground="#4a6584")
        self.neg_qualities_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons to add/remove qualities
        btn_frame = ttk.Frame(qualities_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Add Positive", command=self.add_positive_quality).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Negative", command=self.add_negative_quality).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self.remove_quality).pack(side=tk.RIGHT, padx=5)
    
    def update_character_tab(self):
        # Update attributes
        for attr, value in self.character.attributes.items():
            self.attribute_vars[attr].set(value)
            self.attribute_controls[attr][1].config(text=str(value))
        
        # Update metatype and role
        self.metatype_var.set(self.character.metatype)
        self.role_var.set(self.character.role)
        
        # Update derived attributes
        self.physical_track_var.set(f"Physical Track: {self.character.physical_track}")
        self.stun_track_var.set(f"Stun Track: {self.character.stun_track}")
        self.initiative_var.set(f"Initiative: {self.character.initiative}")
        self.damage_resistance_var.set(f"Damage Resistance: {self.character.damage_resistance}")
        
        # Update condition monitor
        self.physical_damage_var.set(f"{self.character.condition_monitor['Physical']}/{self.character.physical_track}")
        self.stun_damage_var.set(f"{self.character.condition_monitor['Stun']}/{self.character.stun_track}")
        
        # Update qualities
        self.pos_qualities_list.delete(0, tk.END)
        for quality in self.character.qualities["Positive"]:
            self.pos_qualities_list.insert(tk.END, quality)
        
        self.neg_qualities_list.delete(0, tk.END)
        for quality in self.character.qualities["Negative"]:
            self.neg_qualities_list.insert(tk.END, quality)
    
    def update_attribute(self, attribute):
        value = self.attribute_vars[attribute].get()
        if 1 <= value <= 10:
            self.character.attributes[attribute] = value
            self.attribute_controls[attribute][1].config(text=str(value))
            self.character.calculate_derived_attributes()
            self.update_character_tab()
        else:
            self.attribute_vars[attribute].set(self.character.attributes[attribute])
    
    def update_metatype(self, event=None):
        self.character.metatype = self.metatype_var.get()
        self.character.calculate_derived_attributes()
        self.update_character_tab()
    
    def update_role(self, event=None):
        self.character.role = self.role_var.get()
    
    def add_positive_quality(self):
        # In a real app, this would show a dialog with all qualities
        quality = "Quick Healer"  # Example quality
        self.character.add_quality(quality, "Positive")
        self.pos_qualities_list.insert(tk.END, quality)
    
    def add_negative_quality(self):
        quality = "Allergy (Common)"  # Example quality
        self.character.add_quality(quality, "Negative")
        self.neg_qualities_list.insert(tk.END, quality)
    
    def remove_quality(self):
        if self.pos_qualities_list.curselection():
            index = self.pos_qualities_list.curselection()[0]
            quality = self.pos_qualities_list.get(index)
            self.character.remove_quality(quality, "Positive")
            self.pos_qualities_list.delete(index)
        
        if self.neg_qualities_list.curselection():
            index = self.neg_qualities_list.curselection()[0]
            quality = self.neg_qualities_list.get(index)
            self.character.remove_quality(quality, "Negative")
            self.neg_qualities_list.delete(index)
    
    def create_skills_tab(self):
        self.skills_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.skills_tab, text="Skills")
        
        # Create notebook for skill categories
        skills_notebook = ttk.Notebook(self.skills_tab)
        skills_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.skill_frames = {}
        self.skill_vars = {}
        
        # Create a tab for each skill category
        for category in self.character.skills:
            frame = ttk.Frame(skills_notebook)
            skills_notebook.add(frame, text=category)
            self.skill_frames[category] = frame
            
            # Create a canvas with scrollbar
            canvas = tk.Canvas(frame, bg="#2d2d2d", highlightthickness=0)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Add skills to the frame
            row = 0
            for skill in self.character.skills[category]:
                frame = ttk.Frame(scrollable_frame)
                frame.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
                
                lbl = ttk.Label(frame, text=skill, width=25, anchor="w")
                lbl.pack(side="left")
                
                var = tk.IntVar(value=self.character.skills[category][skill])
                self.skill_vars[(category, skill)] = var
                
                spinbox = ttk.Spinbox(frame, from_=0, to=10, width=5, textvariable=var,
                                     command=lambda c=category, s=skill: self.update_skill(c, s))
                spinbox.pack(side="left", padx=5)
                
                row += 1
    
    def update_skills_tab(self):
        for (category, skill), var in self.skill_vars.items():
            var.set(self.character.skills[category][skill])
    
    def update_skill(self, category, skill):
        value = self.skill_vars[(category, skill)].get()
        if 0 <= value <= 10:
            self.character.skills[category][skill] = value
    
    def create_gear_tab(self):
        self.gear_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.gear_tab, text="Gear & Amps")
        
        # Create notebook for different gear types
        gear_notebook = ttk.Notebook(self.gear_tab)
        gear_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Regular Gear
        gear_frame = ttk.Frame(gear_notebook)
        gear_notebook.add(gear_frame, text="Gear")
        
        self.gear_list = ttk.Treeview(gear_frame, columns=("rating", "equipped"), show="headings")
        self.gear_list.heading("#0", text="Name")
        self.gear_list.heading("rating", text="Rating")
        self.gear_list.heading("equipped", text="Equipped")
        
        scrollbar = ttk.Scrollbar(gear_frame, orient="vertical", command=self.gear_list.yview)
        self.gear_list.configure(yscrollcommand=scrollbar.set)
        
        self.gear_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Amps
        amps_frame = ttk.Frame(gear_notebook)
        gear_notebook.add(amps_frame, text="Amps")
        
        self.amps_list = ttk.Treeview(amps_frame, columns=("type", "bonus", "equipped"), show="headings")
        self.amps_list.heading("#0", text="Name")
        self.amps_list.heading("type", text="Type")
        self.amps_list.heading("bonus", text="Bonus")
        self.amps_list.heading("equipped", text="Equipped")
        
        scrollbar = ttk.Scrollbar(amps_frame, orient="vertical", command=self.amps_list.yview)
        self.amps_list.configure(yscrollcommand=scrollbar.set)
        
        self.amps_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Weapons
        weapons_frame = ttk.Frame(gear_notebook)
        gear_notebook.add(weapons_frame, text="Weapons")
        
        self.weapons_list = ttk.Treeview(weapons_frame, columns=("damage", "accuracy", "equipped"), show="headings")
        self.weapons_list.heading("#0", text="Name")
        self.weapons_list.heading("damage", text="Damage")
        self.weapons_list.heading("accuracy", text="Accuracy")
        self.weapons_list.heading("equipped", text="Equipped")
        
        scrollbar = ttk.Scrollbar(weapons_frame, orient="vertical", command=self.weapons_list.yview)
        self.weapons_list.configure(yscrollcommand=scrollbar.set)
        
        self.weapons_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Armor
        armor_frame = ttk.Frame(gear_notebook)
        gear_notebook.add(armor_frame, text="Armor")
        
        self.armor_list = ttk.Treeview(armor_frame, columns=("armor", "equipped"), show="headings")
        self.armor_list.heading("#0", text="Name")
        self.armor_list.heading("armor", text="Armor")
        self.armor_list.heading("equipped", text="Equipped")
        
        scrollbar = ttk.Scrollbar(armor_frame, orient="vertical", command=self.armor_list.yview)
        self.armor_list.configure(yscrollcommand=scrollbar.set)
        
        self.armor_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cyberware
        cyber_frame = ttk.Frame(gear_notebook)
        gear_notebook.add(cyber_frame, text="Cyberware")
        
        self.cyber_list = ttk.Treeview(cyber_frame, columns=("type", "rating", "equipped"), show="headings")
        self.cyber_list.heading("#0", text="Name")
        self.cyber_list.heading("type", text="Type")
        self.cyber_list.heading("rating", text="Rating")
        self.cyber_list.heading("equipped", text="Equipped")
        
        scrollbar = ttk.Scrollbar(cyber_frame, orient="vertical", command=self.cyber_list.yview)
        self.cyber_list.configure(yscrollcommand=scrollbar.set)
        
        self.cyber_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        btn_frame = ttk.Frame(self.gear_tab)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Equip Selected", command=self.equip_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Unequip Selected", command=self.unequip_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Use Medkit", command=self.use_medkit).pack(side=tk.RIGHT, padx=5)
    
    def update_gear_tab(self):
        # Update gear list
        self.gear_list.delete(*self.gear_list.get_children())
        for item in self.character.gear:
            self.gear_list.insert("", "end", text=item.get("name", "Unknown"), 
                                values=(item.get("rating", ""), "Yes" if item.get("equipped", False) else "No"))
        
        # Update amps list
        self.amps_list.delete(*self.amps_list.get_children())
        for amp in self.character.amps:
            self.amps_list.insert("", "end", text=amp.get("name", "Unknown"), 
                                values=(amp.get("type", ""), amp.get("bonus", ""), 
                                       "Yes" if amp.get("equipped", False) else "No"))
        
        # Update weapons list
        self.weapons_list.delete(*self.weapons_list.get_children())
        for weapon in self.character.weapons:
            self.weapons_list.insert("", "end", text=weapon.get("name", "Unknown"), 
                                   values=(weapon.get("damage", ""), weapon.get("accuracy", ""), 
                                          "Yes" if weapon.get("equipped", False) else "No"))
        
        # Update armor list
        self.armor_list.delete(*self.armor_list.get_children())
        for armor in self.character.armor:
            self.armor_list.insert("", "end", text=armor.get("name", "Unknown"), 
                                 values=(armor.get("armor", ""), "Yes" if armor.get("equipped", False) else "No"))
        
        # Update cyberware list
        self.cyber_list.delete(*self.cyber_list.get_children())
        for cyber in self.character.cyberware:
            self.cyber_list.insert("", "end", text=cyber.get("name", "Unknown"), 
                                 values=(cyber.get("type", ""), cyber.get("rating", ""), 
                                        "Yes" if cyber.get("equipped", False) else "No"))
    
    def equip_item(self):
        # This would equip the selected item in the current list
        # Simplified for this example
        self.update_status("Item equipped")
    
    def unequip_item(self):
        # This would unequip the selected item
        self.update_status("Item unequipped")
    
    def use_medkit(self):
        # Find a medkit in gear
        medkit = None
        for item in self.character.gear:
            if "medkit" in item.get("name", "").lower():
                medkit = item
                break
        
        if medkit:
            healing = self.character.use_medkit(medkit)
            self.update_character_tab()
            self.update_gear_tab()
            self.update_status(f"Used medkit, healed {healing} physical damage")
        else:
            self.update_status("No medkit available")
    
    def create_combat_tab(self):
        self.combat_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.combat_tab, text="Combat")
        
        # Initiative section
        initiative_frame = ttk.LabelFrame(self.combat_tab, text="Initiative")
        initiative_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(initiative_frame, text="Base Initiative:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.base_init_var = tk.StringVar(value=str(self.character.initiative))
        ttk.Label(initiative_frame, textvariable=self.base_init_var).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(initiative_frame, text="Initiative Dice:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.init_dice_var = tk.StringVar(value=str(self.character.initiative_dice))
        ttk.Label(initiative_frame, textvariable=self.init_dice_var).grid(row=0, column=3, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(initiative_frame, text="Current Initiative:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.curr_init_var = tk.StringVar(value="0")
        ttk.Label(initiative_frame, textvariable=self.curr_init_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Button(initiative_frame, text="Roll Initiative", command=self.roll_initiative).grid(row=1, column=3, padx=5, pady=5)
        
        # Condition monitor
        cond_frame = ttk.LabelFrame(self.combat_tab, text="Condition Monitor")
        cond_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Physical damage
        ttk.Label(cond_frame, text="Physical Damage:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.phys_damage_var = tk.StringVar(value="0")
        ttk.Entry(cond_frame, textvariable=self.phys_damage_var, width=5).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(cond_frame, text="Apply", command=lambda: self.apply_damage("Physical")).grid(row=0, column=2, padx=5, pady=2)
        
        # Stun damage
        ttk.Label(cond_frame, text="Stun Damage:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.stun_damage_var = tk.StringVar(value="0")
        ttk.Entry(cond_frame, textvariable=self.stun_damage_var, width=5).grid(row=1, column=1, padx=5, pady=2)
        ttk.Button(cond_frame, text="Apply", command=lambda: self.apply_damage("Stun")).grid(row=1, column=2, padx=5, pady=2)
        
        # Combat log
        log_frame = ttk.LabelFrame(self.combat_tab, text="Combat Log")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.combat_log = scrolledtext.ScrolledText(log_frame, bg="#3a3a3a", fg="white", wrap=tk.WORD)
        self.combat_log.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.combat_log.config(state=tk.DISABLED)
    
    def roll_initiative(self):
        initiative = self.character.roll_initiative()
        self.curr_init_var.set(str(initiative))
        self.log_combat_event(f"Rolled initiative: {initiative}")
    
    def apply_damage(self, damage_type):
        try:
            amount = int(self.phys_damage_var.get() if damage_type == "Physical" else self.stun_damage_var.get())
            self.character.apply_damage(damage_type, amount)
            self.update_character_tab()
            self.log_combat_event(f"Applied {amount} {damage_type} damage")
        except ValueError:
            self.update_status("Invalid damage amount")
    
    def log_combat_event(self, message):
        self.combat_log.config(state=tk.NORMAL)
        self.combat_log.insert(tk.END, message + "\n")
        self.combat_log.see(tk.END)
        self.combat_log.config(state=tk.DISABLED)
    
    def create_background_tab(self):
        self.bg_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.bg_tab, text="Background")
        
        # Background info
        bg_frame = ttk.LabelFrame(self.bg_tab, text="Character Background")
        bg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.bg_text = scrolledtext.ScrolledText(bg_frame, bg="#3a3a3a", fg="white", wrap=tk.WORD, height=10)
        self.bg_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.bg_text.insert("1.0", self.character.background)
        self.bg_text.bind("<KeyRelease>", self.update_background)
        
        # Personal info
        info_frame = ttk.Frame(self.bg_tab)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Age
        ttk.Label(info_frame, text="Age:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.age_var = tk.IntVar(value=self.character.age)
        age_spin = ttk.Spinbox(info_frame, from_=16, to=100, width=5, textvariable=self.age_var,
                              command=self.update_age)
        age_spin.grid(row=0, column=1, padx=5, pady=2)
        
        # Reputation
        ttk.Label(info_frame, text="Reputation:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.rep_var = tk.IntVar(value=self.character.reputation)
        rep_spin = ttk.Spinbox(info_frame, from_=0, to=20, width=5, textvariable=self.rep_var,
                              command=self.update_reputation)
        rep_spin.grid(row=0, column=3, padx=5, pady=2)
        
        # Heat
        ttk.Label(info_frame, text="Heat:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=2)
        self.heat_var = tk.IntVar(value=self.character.heat)
        heat_spin = ttk.Spinbox(info_frame, from_=0, to=20, width=5, textvariable=self.heat_var,
                               command=self.update_heat)
        heat_spin.grid(row=0, column=5, padx=5, pady=2)
        
        # Edge
        ttk.Label(info_frame, text="Edge:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.edge_var = tk.IntVar(value=self.character.edge)
        edge_spin = ttk.Spinbox(info_frame, from_=0, to=10, width=5, textvariable=self.edge_var,
                               command=self.update_edge)
        edge_spin.grid(row=1, column=1, padx=5, pady=2)
        
        # Karma
        ttk.Label(info_frame, text="Karma:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.karma_var = tk.IntVar(value=self.character.karma)
        karma_spin = ttk.Spinbox(info_frame, from_=0, to=100, width=5, textvariable=self.karma_var,
                                command=self.update_karma)
        karma_spin.grid(row=1, column=3, padx=5, pady=2)
        
        # Nuyen
        ttk.Label(info_frame, text="Nuyen:").grid(row=1, column=4, sticky=tk.W, padx=5, pady=2)
        self.nuyen_var = tk.IntVar(value=self.character.nuyen)
        nuyen_spin = ttk.Spinbox(info_frame, from_=0, to=1000000, width=10, textvariable=self.nuyen_var,
                                command=self.update_nuyen)
        nuyen_spin.grid(row=1, column=5, padx=5, pady=2)
    
    def update_background_tab(self):
        self.bg_text.delete("1.0", tk.END)
        self.bg_text.insert("1.0", self.character.background)
        self.age_var.set(self.character.age)
        self.rep_var.set(self.character.reputation)
        self.heat_var.set(self.character.heat)
        self.edge_var.set(self.character.edge)
        self.karma_var.set(self.character.karma)
        self.nuyen_var.set(self.character.nuyen)
    
    def update_background(self, event):
        self.character.background = self.bg_text.get("1.0", tk.END).strip()
    
    def update_age(self):
        self.character.age = self.age_var.get()
    
    def update_reputation(self):
        self.character.reputation = self.rep_var.get()
    
    def update_heat(self):
        self.character.heat = self.heat_var.get()
    
    def update_edge(self):
        self.character.edge = self.edge_var.get()
    
    def update_karma(self):
        self.character.karma = self.karma_var.get()
    
    def update_nuyen(self):
        self.character.nuyen = self.nuyen_var.get()
    
    def create_dice_tab(self):
        self.dice_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.dice_tab, text="Dice Roller")
        
        # Dice pool configuration
        config_frame = ttk.LabelFrame(self.dice_tab, text="Dice Roll Configuration")
        config_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Dice pool
        ttk.Label(config_frame, text="Dice Pool:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.dice_pool_var = tk.IntVar(value=4)
        pool_spin = ttk.Spinbox(config_frame, from_=1, to=20, width=5, textvariable=self.dice_pool_var)
        pool_spin.grid(row=0, column=1, padx=5, pady=5)
        
        # Bonus
        ttk.Label(config_frame, text="Bonus/Penalty:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.bonus_var = tk.IntVar(value=0)
        bonus_spin = ttk.Spinbox(config_frame, from_=-5, to=10, width=5, textvariable=self.bonus_var)
        bonus_spin.grid(row=0, column=3, padx=5, pady=5)
        
        # Edge
        ttk.Label(config_frame, text="Edge to Spend:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.edge_spend_var = tk.IntVar(value=0)
        edge_spin = ttk.Spinbox(config_frame, from_=0, to=3, width=5, textvariable=self.edge_spend_var)
        edge_spin.grid(row=1, column=1, padx=5, pady=5)
        
        # Wild die
        self.wild_die_var = tk.BooleanVar()
        wild_check = ttk.Checkbutton(config_frame, text="Wild Die", variable=self.wild_die_var)
        wild_check.grid(row=1, column=2, padx=5, pady=5)
        
        # Roll button
        roll_btn = ttk.Button(config_frame, text="Roll Dice", command=self.roll_dice)
        roll_btn.grid(row=1, column=3, padx=5, pady=5)
        
        # Result display
        result_frame = ttk.LabelFrame(self.dice_tab, text="Roll Results")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.dice_canvas = tk.Canvas(result_frame, bg="#2d2d2d", highlightthickness=0)
        self.dice_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Result labels
        result_info = ttk.Frame(result_frame)
        result_info.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(result_info, text="Hits:").pack(side=tk.LEFT, padx=5)
        self.hits_var = tk.StringVar(value="0")
        ttk.Label(result_info, textvariable=self.hits_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(result_info, text="Glitch:").pack(side=tk.LEFT, padx=5)
        self.glitch_var = tk.StringVar(value="No")
        ttk.Label(result_info, textvariable=self.glitch_var).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(result_info, text="Total Dice:").pack(side=tk.LEFT, padx=5)
        self.total_dice_var = tk.StringVar(value="0")
        ttk.Label(result_info, textvariable=self.total_dice_var).pack(side=tk.LEFT, padx=5)
    
    def roll_dice(self):
        pool = self.dice_pool_var.get()
        bonus = self.bonus_var.get()
        edge_spent = self.edge_spend_var.get()
        wild_die = self.wild_die_var.get()
        
        result = self.character.roll_dice(pool, bonus, edge_spent, wild_die)
        
        # Display results
        self.display_dice_results(result)
        
        # Update result labels
        self.hits_var.set(str(result["hits"]))
        self.glitch_var.set("Yes" if result["glitch"] else "No")
        self.total_dice_var.set(str(result["pool"]))
        
        self.update_status(f"Rolled {result['hits']} hits{' with glitch' if result['glitch'] else ''}")
    
    def display_dice_results(self, result):
        self.dice_canvas.delete("all")
        
        rolls = result["rolls"]
        hits = result["hits"]
        glitch = result["glitch"]
        
        # Calculate positions
        num_dice = len(rolls)
        canvas_width = self.dice_canvas.winfo_width()
        canvas_height = self.dice_canvas.winfo_height()
        
        if canvas_width < 10 or canvas_height < 10:
            return
        
        max_cols = max(1, min(10, int(canvas_width // 50)))
        max_rows = (num_dice + max_cols - 1) // max_cols
        
        # Draw dice
        for i, roll in enumerate(rolls):
            row = i // max_cols
            col = i % max_cols
            
            x = 30 + col * 50
            y = 30 + row * 50
            
            # Draw dice background
            color = "#4caf50" if roll >= 5 else "#f44336"  # Green for hits, red for misses
            self.dice_canvas.create_rectangle(x-15, y-15, x+15, y+15, fill=color, outline="#cccccc")
            
            # Draw dice value
            self.dice_canvas.create_text(x, y, text=str(roll), fill="white", font=("Arial", 12, "bold"))
        
        # Draw summary
        summary_y = 40 + max_rows * 50
        self.dice_canvas.create_text(20, summary_y, text=f"Hits: {hits}", anchor=tk.W, fill="#cccccc", font=("Arial", 10))
        self.dice_canvas.create_text(20, summary_y+20, text=f"Glitch: {'Yes' if glitch else 'No'}", anchor=tk.W, fill="#cccccc", font=("Arial", 10))


if __name__ == "__main__":
    app = ShadowrunApp()
    app.mainloop()