import json
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk

class ShadowrunCharacter:
    METATYPES = ["Human", "Elf", "Dwarf", "Ork", "Troll"]
    ATTRIBUTES = ["Body", "Agility", "Reaction", "Strength", "Willpower", 
                 "Logic", "Intuition", "Charisma", "Edge", "Magic", 
                 "Resonance", "Essence"]
    SKILLS = ["Astral", "Athletics", "Biotech", "Close Combat", "Con", 
             "Conjuring", "Cracking", "Electronics", "Enchanting", "Engineering",
             "Exotic Weapons", "Firearms", "Influence", "Outdoors", "Perception",
             "Piloting", "Sorcery", "Stealth", "Tasking"]
    
    # Skill specializations
    SKILL_SPECIALIZATIONS = {
        "Firearms": ["Pistols", "Rifles", "Shotguns", "Machine Guns"],
        "Close Combat": ["Blades", "Clubs", "Unarmed Combat"],
        "Stealth": ["Urban", "Wilderness", "Vehicle"],
        "Perception": ["Visual", "Auditory", "Scent"],
        "Con": ["Fast Talk", "Impersonation", "Seduction"],
        "Electronics": ["Cyberdecks", "Commlinks", "Security Systems"],
        "Engineering": ["Aeronautics", "Automotive", "Marine"],
        "Biotech": ["First Aid", "Medicine", "Cybertechnology"],
        "Cracking": ["Hacking", "Cybercombat", "Electronic Warfare"],
        "Tasking": ["Compiling", "Decompiling", "Registering"],
        "Sorcery": ["Combat Spells", "Health Spells", "Illusion Spells"],
        "Conjuring": ["Summoning", "Banishing", "Binding"],
        "Enchanting": ["Alchemy", "Disenchanting", "Artificing"],
        "Influence": ["Leadership", "Negotiation", "Intimidation"],
        "Outdoors": ["Navigation", "Survival", "Tracking"],
        "Piloting": ["Ground Craft", "Aircraft", "Watercraft"],
        "Astral": ["Astral Combat", "Astral Tracking", "Astral Perception"]
    }
    
    MAGIC_TYPES = ["Mundane", "Magician", "Adept", "Aspected Magician", "Mystic Adept", "Technomancer"]
    LIFESTYLES = ["Street", "Squatter", "Low", "Middle", "High", "Luxury"]
    LIFESTYLE_NUYEN = {
        "Street": 1000,
        "Squatter": 2000,
        "Low": 5000,
        "Middle": 10000,
        "High": 100000,
        "Luxury": 1000000
    }
    
    # Define roles and their attribute bonuses
    ROLES = {
        "Street Samurai": {"Body": 1, "Agility": 1},
        "Decker": {"Logic": 2, "Intuition": 1},
        "Rigger": {"Reaction": 2, "Logic": 1},
        "Face": {"Charisma": 2, "Intuition": 1},
        "Mage": {"Magic": 2, "Willpower": 1},
        "Shaman": {"Magic": 2, "Charisma": 1},
        "Adept": {"Magic": 2, "Agility": 1},
        "Technomancer": {"Resonance": 2, "Logic": 1}
    }
    
    # Define magical traditions
    TRADITIONS = ["None", "Hermetic", "Shamanic", "Christian Theurgy", "Buddhist", "Islamic", "Voodoo"]
    
    QUALITIES = {
        "Positive": ["Adept", "Ambidextrous", "Analytical Mind", "Astral Chameleon", 
                    "Blandness", "Catlike", "Double-Jointed", "Guts", "High Pain Tolerance", 
                    "Home Ground", "Human-Looking", "Indomitable", "Juryrigger", "Lucky", 
                    "Magical Resistance", "Natural Athlete", "Photographic Memory", 
                    "Quick Healer", "Spirit Affinity", "Toughness", "Will to Live"],
        "Negative": ["Addiction", "Allergy", "Astral Beacon", "Bad Luck", "Bad Rep", 
                    "Code of Honor", "Dependents", "Gremlins", "Incompetent", "Insomnia", 
                    "Magic Sense", "Mild Phobia", "Sensitive System", "Simsense Vertigo", 
                    "Social Stress", "Spirit Bane", "Uncouth", "Uneducated"]
    }
    
    # Qualities with attribute effects
    QUALITY_EFFECTS = {
        "Analytical Mind": {"Logic": 1},
        "Toughness": {"Body": 1},
        "Indomitable": {"Willpower": 1},
        "Ambidextrous": {"Agility": 1},
        "Natural Athlete": {"Strength": 1, "Agility": 1},
        "Uncouth": {"Charisma": -2},
        "Uneducated": {"Logic": -2},
        "Incompetent": {"Logic": -1, "Intuition": -1}
    }
    
    GEAR_CATEGORIES = ["Weapons", "Armor", "Cyberware", "Bioware", "Magic Items", "Electronics", "Other"]
    WEAPON_TYPES = ["Blades", "Clubs", "Thrown", "Pistols", "Rifles", "Shotguns", "Machine Guns", "Special"]
    ARMOR_TYPES = ["Clothing", "Armor Jacket", "Full Body Armor", "Helmet", "Shield"]
    CYBERWARE_TYPES = ["Headware", "Eyeware", "Earware", "Bodyware", "Cyberlimbs", "Implants"]
    
    # Contact types and loyalty levels
    CONTACT_TYPES = ["Fixer", "Johnson", "Gang", "Corporate", "Police", "Media", "Talislegger", "Decker", "Street Doc"]
    LOYALTY_LEVELS = [str(i) for i in range(1, 7)]  # 1-6
    
    # Dice roll options
    DICE_ROLL_OPTIONS = [
        "Attack (Physical)",
        "Attack (Spell)",
        "Attack (Ranged)",
        "Defense (Physical)",
        "Defense (Astral)",
        "Hacking",
        "Con",
        "Perception",
        "Stealth",
        "First Aid",
        "Piloting",
        "Summoning",
        "Binding"
    ]
    
    def __init__(self):
        self.reset_character()
        
    def reset_character(self):
        self.name = ""
        self.metatype = "Human"
        self.role = ""
        self.background = ""
        self.lifestyle = "Low"
        self.karma = 0
        self.nuyen = 5000
        self.magic_type = "Mundane"
        self.tradition = ""
        self.mentor_spirit = ""
        self.initiation_grade = 0
        
        # Attributes
        self.attributes = {attr: 1 for attr in self.ATTRIBUTES}
        self.attributes["Edge"] = 1
        self.attributes["Essence"] = 6.0
        self.base_attributes = self.attributes.copy()  # Store base attributes without bonuses
        
        # Skills
        self.skills = {skill: 0 for skill in self.SKILLS}
        self.specializations = {}
        
        # Qualities
        self.qualities = []
        
        # Gear
        self.gear = {category: [] for category in self.GEAR_CATEGORIES}
        self.contacts = []
        
        # Spells/Powers
        self.spells = []  # Now stored as dictionaries: {"name": "", "description": "", "type": "", "drain": 0}
        self.powers = []  # Now stored as dictionaries: {"name": "", "description": "", "activation": "", "effect": ""}
        self.complex_forms = []
        self.foci = []    # Now stored as dictionaries: {"name": "", "description": "", "type": "", "force": 0}
        
        # Combat stats
        self.calculate_derived_stats()
        self.physical_damage = 0
        self.stun_damage = 0
        self.initiative_passed = 0
    
    def calculate_derived_stats(self):
        # Reset attributes to base before applying bonuses
        self.attributes = self.base_attributes.copy()
        
        # Apply metatype modifiers (p.53-56)
        if self.metatype == "Dwarf":
            self.attributes["Body"] = max(3, self.attributes["Body"])
            self.attributes["Willpower"] = max(3, self.attributes["Willpower"])
        elif self.metatype == "Elf":
            self.attributes["Agility"] = max(2, self.attributes["Agility"])
            self.attributes["Charisma"] = max(3, self.attributes["Charisma"])
        elif self.metatype == "Ork":
            self.attributes["Body"] = max(3, self.attributes["Body"])
            self.attributes["Strength"] = max(3, self.attributes["Strength"])
        elif self.metatype == "Troll":
            self.attributes["Body"] = max(5, self.attributes["Body"])
            self.attributes["Strength"] = max(5, self.attributes["Strength"])
            self.attributes["Logic"] = max(1, min(self.attributes["Logic"], 5))
            
        # Apply role bonuses
        if self.role in self.ROLES:
            for attr, bonus in self.ROLES[self.role].items():
                self.attributes[attr] = max(1, self.attributes[attr] + bonus)
            
        # Apply quality effects
        for quality in self.qualities:
            if quality in self.QUALITY_EFFECTS:
                for attr, bonus in self.QUALITY_EFFECTS[quality].items():
                    self.attributes[attr] = max(1, self.attributes[attr] + bonus)
        
        # Condition monitors (p.39)
        body = self.attributes["Body"]
        willpower = self.attributes["Willpower"]
        
        # Apply High Pain Tolerance quality
        pain_tolerance = 0
        if "High Pain Tolerance" in self.qualities:
            # Each level adds 1 box (we'll assume 1 level for simplicity)
            pain_tolerance = 2
            
        self.physical_boxes = (body + 1) // 2 + 8 + pain_tolerance
        self.stun_boxes = (willpower + 1) // 2 + 8 + pain_tolerance
        
        # Initiative (p.39)
        self.initiative_score = self.attributes["Reaction"] + self.attributes["Intuition"]
        self.initiative_dice = 1
        
        # Essence affects Magic (p.38)
        if self.magic_type != "Mundane" and self.magic_type != "Technomancer":
            essence = self.attributes["Essence"]
            magic = self.attributes["Magic"]
            for i in range(1, 7):
                if essence < i:
                    magic = min(magic, 6 - i)
            self.attributes["Magic"] = magic

    def add_gear(self, category, item):
        self.gear[category].append(item)
        self.calculate_gear_bonuses()
        
    def update_gear(self, category, index, item):
        if 0 <= index < len(self.gear[category]):
            self.gear[category][index] = item
            self.calculate_gear_bonuses()
        
    def calculate_gear_bonuses(self):
        # Apply cyberware essence cost
        essence_cost = 0
        for item in self.gear["Cyberware"] + self.gear["Bioware"]:
            if "Essence Cost" in item:
                essence_cost += float(item["Essence Cost"])
        self.attributes["Essence"] = max(0, 6.0 - essence_cost)
        
        # Reset armor bonuses
        self.attributes["Armor"] = 0
        
        # Apply armor bonuses
        for item in self.gear["Armor"]:
            if "Rating" in item:
                try:
                    self.attributes["Armor"] += int(item["Rating"])
                except ValueError:
                    pass
        
        # Apply weapon bonuses
        for item in self.gear["Weapons"]:
            if "Accuracy" in item:
                try:
                    self.attributes["Weapon Accuracy"] = max(self.attributes.get("Weapon Accuracy", 0), int(item["Accuracy"]))
                except ValueError:
                    pass
        
        # Recalculate derived stats
        self.calculate_derived_stats()
    
    def roll_dice(self, pool_size, edge_use=0):
        """Roll dice for Shadowrun system"""
        if pool_size <= 0:
            return {"dice": [], "hits": 0, "glitch": False, "critical_glitch": False}
        
        # Use Edge for re-rolls
        rerolls = edge_use
        dice = []
        while rerolls >= 0 and pool_size > 0:
            rolls = [random.randint(1, 6) for _ in range(pool_size)]
            dice.extend(rolls)
            
            # If we're using Edge, re-roll non-5s and non-6s
            if rerolls > 0:
                pool_size = sum(1 for r in rolls if r < 5)
                rerolls -= 1
            else:
                break
        
        hits = sum(1 for r in dice if r >= 5)
        ones = sum(1 for r in dice if r == 1)
        total_dice = len(dice)
        
        glitch = ones > total_dice / 2
        critical_glitch = glitch and hits == 0
        
        return {
            "dice": dice,
            "hits": hits,
            "glitch": glitch,
            "critical_glitch": critical_glitch
        }
    
    def roll_initiative(self):
        """Roll initiative dice and return result"""
        base_score = self.attributes["Reaction"] + self.attributes["Intuition"]
        dice_rolls = [random.randint(1, 6) for _ in range(self.initiative_dice)]
        return base_score + sum(dice_rolls), dice_rolls
    
    def heal_damage(self, damage_type, amount):
        """Heal physical or stun damage"""
        if damage_type == "physical":
            self.physical_damage = max(0, self.physical_damage - amount)
        elif damage_type == "stun":
            self.stun_damage = max(0, self.stun_damage - amount)
    
    def use_medkit(self):
        """Use a medkit to heal damage if available"""
        for item in self.gear["Bioware"] + self.gear["Electronics"] + self.gear["Other"]:
            if "Medkit" in item.get("name", ""):
                rating = item.get("Rating", 1)
                self.heal_damage("physical", rating * 2)
                self.heal_damage("stun", rating)
                return True
        return False
    
    def rest(self):
        """Rest to recover stun damage"""
        self.heal_damage("stun", 1)
    
    def to_dict(self):
        return {
            "name": self.name,
            "metatype": self.metatype,
            "role": self.role,
            "background": self.background,
            "lifestyle": self.lifestyle,
            "karma": self.karma,
            "nuyen": self.nuyen,
            "magic_type": self.magic_type,
            "tradition": self.tradition,
            "mentor_spirit": self.mentor_spirit,
            "initiation_grade": self.initiation_grade,
            "attributes": self.attributes,
            "base_attributes": self.base_attributes,
            "skills": self.skills,
            "specializations": self.specializations,
            "qualities": self.qualities,
            "gear": self.gear,
            "contacts": self.contacts,
            "spells": self.spells,
            "powers": self.powers,
            "complex_forms": self.complex_forms,
            "foci": self.foci,
            "physical_boxes": self.physical_boxes,
            "stun_boxes": self.stun_boxes,
            "initiative_score": self.initiative_score,
            "initiative_dice": self.initiative_dice,
            "physical_damage": self.physical_damage,
            "stun_damage": self.stun_damage
        }
    
    def from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Set base attributes if not present in saved data
        if not hasattr(self, 'base_attributes'):
            self.base_attributes = self.attributes.copy()
            
        self.calculate_derived_stats()
        return self

class DescriptionViewer(tk.Toplevel):
    """Dialog to view item descriptions (read-only)"""
    def __init__(self, parent, title, content):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x400")
        self.configure(bg="#1c1c1c")
        
        # Create text widget
        text_frame = ttk.Frame(self)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.text_area = scrolledtext.ScrolledText(
            text_frame, wrap=tk.WORD, 
            bg="#333", fg="#e0e0e0", 
            font=("Arial", 10)
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.insert(tk.END, content)
        self.text_area.config(state=tk.DISABLED)
        
        # Close button
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Close", command=self.destroy).pack()

class EditGearDialog(tk.Toplevel):
    GEAR_ATTRIBUTES = {
        "Weapons": ["Damage", "Accuracy", "AP", "Mode", "RC", "Ammo"],
        "Armor": ["Rating", "Social", "Capacity"],
        "Cyberware": ["Essence Cost", "Capacity", "Rating"],
        "Bioware": ["Essence Cost", "Rating", "Capacity"],
        "Magic Items": ["Force", "Type", "Binding"],
        "Electronics": ["Rating", "Capacity", "Function"],
        "Other": ["Effect", "Duration", "Potency"]
    }
    
    def __init__(self, parent, category, item=None):
        super().__init__(parent)
        self.parent = parent
        self.category = category
        self.item = item or {}
        self.result = None
        
        self.title(f"Edit {category}")
        self.geometry("400x500")
        self.configure(bg="#1c1c1c")
        self.resizable(True, True)
        
        self.create_widgets()
        self.grab_set()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.name_entry.insert(0, self.item.get("name", ""))
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=1, column=0, sticky=tk.NW, padx=5, pady=5)
        self.desc_text = scrolledtext.ScrolledText(main_frame, width=30, height=4, 
                                                  bg="#333", fg="#e0e0e0", insertbackground="white")
        self.desc_text.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.desc_text.insert(tk.END, self.item.get("description", ""))
        
        # Standard attributes for category
        row = 2
        self.attr_entries = {}
        for attr in self.GEAR_ATTRIBUTES.get(self.category, []):
            ttk.Label(main_frame, text=f"{attr}:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            entry = ttk.Entry(main_frame, width=15)
            entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
            entry.insert(0, str(self.item.get(attr, "")))
            self.attr_entries[attr] = entry
            row += 1
        
        # Custom attributes
        ttk.Label(main_frame, text="Custom Attributes:").grid(row=row, column=0, sticky=tk.NW, padx=5, pady=5)
        self.attr_text = scrolledtext.ScrolledText(main_frame, width=30, height=4, 
                                                  bg="#333", fg="#e0e0e0", insertbackground="white")
        self.attr_text.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        row += 1
        
        # Load existing custom attributes
        if self.item:
            custom_attrs = []
            for key, value in self.item.items():
                if key not in ["name", "description"] and key not in self.GEAR_ATTRIBUTES.get(self.category, []):
                    custom_attrs.append(f"{key}: {value}")
            self.attr_text.insert(tk.END, "\n".join(custom_attrs))
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=row, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
            
        # Get description
        description = self.desc_text.get("1.0", tk.END).strip()
        
        # Get standard attributes
        attributes = {}
        for attr, entry in self.attr_entries.items():
            value = entry.get().strip()
            if value:
                attributes[attr] = value
        
        # Parse custom attributes
        text = self.attr_text.get("1.0", tk.END)
        for line in text.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key:  # Only add if key is not empty
                    attributes[key] = value
        
        # Create result with all attributes
        self.result = {"name": name, "description": description}
        self.result.update(attributes)
        self.destroy()

class EditContactDialog(tk.Toplevel):
    def __init__(self, parent, contact=None):
        super().__init__(parent)
        self.parent = parent
        self.contact = contact or {}
        self.result = None
        
        self.title("Edit Contact")
        self.geometry("400x300")
        self.configure(bg="#1c1c1c")
        self.resizable(False, False)
        
        self.create_widgets()
        self.grab_set()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        fields = [
            ("Name:", "name", "entry"),
            ("Type:", "type", "combo"),
            ("Loyalty:", "loyalty", "combo"),
            ("Connection:", "connection", "entry"),
            ("Notes:", "notes", "text")
        ]
        
        self.entries = {}
        for i, (label, key, field_type) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            if field_type == "text":
                entry = scrolledtext.ScrolledText(main_frame, width=30, height=4, 
                                                bg="#333", fg="#e0e0e0", insertbackground="white")
                entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                if self.contact.get(key):
                    entry.insert(tk.END, self.contact[key])
            elif field_type == "combo":
                entry = ttk.Combobox(main_frame, width=27)
                if key == "type":
                    entry["values"] = ShadowrunCharacter.CONTACT_TYPES
                elif key == "loyalty":
                    entry["values"] = ShadowrunCharacter.LOYALTY_LEVELS
                entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                if self.contact.get(key):
                    entry.set(self.contact[key])
            else:
                entry = ttk.Entry(main_frame, width=30)
                entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                if self.contact.get(key):
                    entry.insert(0, self.contact[key])
            
            self.entries[key] = entry
        
        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        result = {}
        for key, widget in self.entries.items():
            if isinstance(widget, (ttk.Entry, ttk.Combobox)):
                result[key] = widget.get()
            else:  # ScrolledText
                result[key] = widget.get("1.0", tk.END).strip()
        
        if not result.get("name"):
            messagebox.showerror("Error", "Name is required")
            return
            
        self.result = result
        self.destroy()

class CharacterSheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shadowrun 6E Character Manager")
        self.root.geometry("1200x800")
        self.character = ShadowrunCharacter()
        
        # Configure dark theme for all widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Base colors
        bg_color = "#1c1c1c"
        fg_color = "#e0e0e0"
        entry_bg = "#333333"
        selected_bg = "#4a6984"
        
        # Configure styles
        self.style.configure(".", background=bg_color, foreground=fg_color, font=("Arial", 10))
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color)
        self.style.configure("TButton", background="#333", foreground=fg_color, 
                           borderwidth=1, focusthickness=3, focuscolor='#333')
        self.style.map("TButton", 
                      background=[('active', '#444')],
                      foreground=[('active', fg_color)])
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color, 
                           insertcolor=fg_color)
        self.style.configure("TCombobox", fieldbackground=entry_bg, foreground=fg_color, 
                           background=bg_color)
        self.style.configure("TSpinbox", fieldbackground=entry_bg, foreground=fg_color, 
                           background=bg_color)
        self.style.configure("Treeview", background=entry_bg, foreground=fg_color, 
                           fieldbackground=entry_bg, borderwidth=0)
        self.style.map("Treeview", background=[('selected', selected_bg)])
        self.style.configure("Treeview.Heading", background="#2d2d2d", foreground=fg_color)
        self.style.configure("Vertical.TScrollbar", background="#333", troughcolor=bg_color)
        self.style.configure("Horizontal.TScrollbar", background="#333", troughcolor=bg_color)
        self.style.configure("TNotebook", background=bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#2d2d2d", foreground=fg_color, 
                           padding=[10, 5])
        self.style.map("TNotebook.Tab", background=[("selected", bg_color)])
        
        # Create main frames
        self.header_frame = ttk.Frame(self.root)
        self.header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.footer_frame = ttk.Frame(self.root)
        self.footer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Header
        ttk.Label(self.header_frame, text="Shadowrun 6E Character Manager", 
                 font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Footer
        ttk.Button(self.footer_frame, text="New Character", command=self.new_character).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.footer_frame, text="Save Character", command=self.save_character).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.footer_frame, text="Load Character", command=self.load_character).pack(side=tk.LEFT, padx=5)
        
        # Create notebook
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.tabs = {}
        tab_names = ["Basic Info", "Skills", "Qualities", "Gear", 
                    "Magic/Resonance", "Contacts", "Background", "Combat Stats"]
        
        for name in tab_names:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=name)
            self.tabs[name] = tab
        
        # Set up tabs
        self.setup_basic_info_tab()
        self.setup_skills_tab()
        self.setup_qualities_tab()
        self.setup_gear_tab()
        self.setup_magic_tab()
        self.setup_contacts_tab()
        self.setup_background_tab()
        self.setup_combat_stats_tab()
        
        # Load default character
        self.update_all_fields()
    
    def setup_basic_info_tab(self):
        tab = self.tabs["Basic Info"]
        notebook = ttk.Notebook(tab)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Character info frame
        char_frame = ttk.Frame(notebook)
        notebook.add(char_frame, text="Character Info")
        
        # Name
        ttk.Label(char_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.name_entry = ttk.Entry(char_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.W)
        self.name_entry.bind("<FocusOut>", self.update_derived_stats)
        
        # Metatype
        ttk.Label(char_frame, text="Metatype:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        self.metatype_combo = ttk.Combobox(char_frame, values=ShadowrunCharacter.METATYPES, state="readonly", width=15)
        self.metatype_combo.grid(row=0, column=3, padx=5, pady=2, sticky=tk.W)
        self.metatype_combo.bind("<<ComboboxSelected>>", self.update_derived_stats)
        
        # Role
        ttk.Label(char_frame, text="Role:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.role_combo = ttk.Combobox(char_frame, values=list(ShadowrunCharacter.ROLES.keys()), state="readonly", width=15)
        self.role_combo.grid(row=1, column=1, padx=5, pady=2, sticky=tk.W)
        self.role_combo.bind("<<ComboboxSelected>>", self.update_derived_stats)
        
        # Magic Type
        ttk.Label(char_frame, text="Magic/Resonance:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=2)
        self.magic_combo = ttk.Combobox(char_frame, values=ShadowrunCharacter.MAGIC_TYPES, state="readonly", width=15)
        self.magic_combo.grid(row=1, column=3, padx=5, pady=2, sticky=tk.W)
        self.magic_combo.bind("<<ComboboxSelected>>", self.update_derived_stats)
        
        # Tradition/Mentor
        ttk.Label(char_frame, text="Tradition/Mentor:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.tradition_combo = ttk.Combobox(char_frame, values=ShadowrunCharacter.TRADITIONS, state="readonly", width=15)
        self.tradition_combo.grid(row=2, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Initiation Grade
        ttk.Label(char_frame, text="Initiation Grade:").grid(row=2, column=2, sticky=tk.W, padx=5, pady=2)
        self.init_grade_spin = ttk.Spinbox(char_frame, from_=0, to=10, width=5)
        self.init_grade_spin.grid(row=2, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Lifestyle
        ttk.Label(char_frame, text="Lifestyle:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.lifestyle_combo = ttk.Combobox(char_frame, values=ShadowrunCharacter.LIFESTYLES, state="readonly", width=15)
        self.lifestyle_combo.grid(row=3, column=1, padx=5, pady=2, sticky=tk.W)
        self.lifestyle_combo.bind("<<ComboboxSelected>>", self.update_lifestyle_nuyen)
        
        # Karma
        ttk.Label(char_frame, text="Karma:").grid(row=3, column=2, sticky=tk.W, padx=5, pady=2)
        self.karma_spin = ttk.Spinbox(char_frame, from_=0, to=100, width=5)
        self.karma_spin.grid(row=3, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Nuyen
        ttk.Label(char_frame, text="Nuyen:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.nuyen_entry = ttk.Entry(char_frame, width=15)
        self.nuyen_entry.grid(row=4, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Attributes frame
        attr_frame = ttk.Frame(notebook)
        notebook.add(attr_frame, text="Attributes")
        
        self.attribute_vars = {}
        self.attribute_entries = {}
        
        # Use a grid layout with 4 columns per row
        for i, attr in enumerate(ShadowrunCharacter.ATTRIBUTES):
            row = i // 4
            col = (i % 4) * 2
            
            ttk.Label(attr_frame, text=f"{attr}:").grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)
            
            var = tk.IntVar()
            entry = ttk.Spinbox(attr_frame, from_=1, to=10, width=3, textvariable=var)
            entry.grid(row=row, column=col+1, padx=(0, 15), pady=2)  # Add right padding
            entry.bind("<FocusOut>", self.update_derived_stats)
            
            self.attribute_vars[attr] = var
            self.attribute_entries[attr] = entry
            
            # Add label for metatype bonus - place in next column with spacing
            bonus_label = ttk.Label(attr_frame, text="", foreground="#4F9BFF")
            bonus_label.grid(row=row, column=col+2, padx=(0, 10), pady=2)
            setattr(self, f"{attr.lower()}_bonus_label", bonus_label)
        
        # Auto Roll button
        ttk.Button(attr_frame, text="Auto Roll Attributes", command=self.autoroll_attributes).grid(
            row=row+1, column=0, columnspan=8, pady=10
        )
    
    def autoroll_attributes(self):
        """Auto-roll attributes with metatype considerations"""
        metatype = self.character.metatype
        
        # Roll base attributes
        base_attrs = {}
        for attr in ShadowrunCharacter.ATTRIBUTES:
            # Skip Essence and Magic/Resonance for auto-roll
            if attr in ["Essence", "Magic", "Resonance"]:
                continue
            base_attrs[attr] = random.randint(1, 6)
        
        # Apply metatype minimums
        if metatype == "Dwarf":
            base_attrs["Body"] = max(3, base_attrs["Body"])
            base_attrs["Willpower"] = max(3, base_attrs["Willpower"])
        elif metatype == "Elf":
            base_attrs["Agility"] = max(2, base_attrs["Agility"])
            base_attrs["Charisma"] = max(3, base_attrs["Charisma"])
        elif metatype == "Ork":
            base_attrs["Body"] = max(3, base_attrs["Body"])
            base_attrs["Strength"] = max(3, base_attrs["Strength"])
        elif metatype == "Troll":
            base_attrs["Body"] = max(5, base_attrs["Body"])
            base_attrs["Strength"] = max(5, base_attrs["Strength"])
            base_attrs["Logic"] = min(5, base_attrs["Logic"])
        
        # Set the attributes
        self.character.base_attributes.update(base_attrs)
        self.update_all_fields()
    
    def update_lifestyle_nuyen(self, event=None):
        lifestyle = self.lifestyle_combo.get()
        if lifestyle:
            nuyen = ShadowrunCharacter.LIFESTYLE_NUYEN.get(lifestyle, 5000)
            self.nuyen_entry.delete(0, tk.END)
            self.nuyen_entry.insert(0, str(nuyen))
            self.update_derived_stats()
    
    def setup_skills_tab(self):
        tab = self.tabs["Skills"]
        
        # Left frame for skill selection
        left_frame = ttk.Frame(tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Skill list
        skill_frame = ttk.LabelFrame(left_frame, text="Skills")
        skill_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.skill_tree = ttk.Treeview(skill_frame, columns=("Rank", "Spec"), show="headings", height=15)
        self.skill_tree.heading("#0", text="Skill")
        self.skill_tree.heading("Rank", text="Rank")
        self.skill_tree.heading("Spec", text="Specialization")
        self.skill_tree.column("#0", width=150)
        self.skill_tree.column("Rank", width=50)
        self.skill_tree.column("Spec", width=150)
        
        for skill in ShadowrunCharacter.SKILLS:
            self.skill_tree.insert("", "end", text=skill, values=(0, ""))
        
        self.skill_tree.pack(fill=tk.BOTH, expand=True)
        self.skill_tree.bind("<<TreeviewSelect>>", self.update_specialization_list)
        
        # Controls for skill
        ctrl_frame = ttk.Frame(skill_frame)
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ctrl_frame, text="Rank:").pack(side=tk.LEFT, padx=2)
        self.skill_rank_spin = ttk.Spinbox(ctrl_frame, from_=0, to=12, width=3)
        self.skill_rank_spin.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(ctrl_frame, text="Specialization:").pack(side=tk.LEFT, padx=2)
        self.skill_spec_combo = ttk.Combobox(ctrl_frame, width=20, state="readonly")
        self.skill_spec_combo.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(ctrl_frame, text="Update Skill", command=self.update_skill).pack(side=tk.LEFT, padx=5)
        
        # Skill description
        desc_frame = ttk.LabelFrame(left_frame, text="Skill Description")
        desc_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.skill_desc_text = scrolledtext.ScrolledText(desc_frame, height=5, wrap=tk.WORD,
                                                        bg="#333", fg="#e0e0e0")
        self.skill_desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.skill_desc_text.config(state=tk.DISABLED)
    
    def update_specialization_list(self, event=None):
        selected = self.skill_tree.selection()
        if not selected:
            return
            
        skill = self.skill_tree.item(selected[0], "text")
        specializations = ShadowrunCharacter.SKILL_SPECIALIZATIONS.get(skill, [])
        
        # Add "None" option and set as default
        options = ["None"] + specializations
        self.skill_spec_combo["values"] = options
        self.skill_spec_combo.set("None")
        
        # Set current specialization if exists
        current_spec = self.character.specializations.get(skill, "")
        if current_spec:
            self.skill_spec_combo.set(current_spec)
        
        # Also update the rank spinbox to current skill value
        self.skill_rank_spin.delete(0, tk.END)
        self.skill_rank_spin.insert(0, str(self.character.skills[skill]))
        
        # Update skill description
        self.skill_desc_text.config(state=tk.NORMAL)
        self.skill_desc_text.delete(1.0, tk.END)
        self.skill_desc_text.insert(tk.END, f"Skill: {skill}\n")
        self.skill_desc_text.insert(tk.END, f"Rank: {self.character.skills[skill]}\n")
        self.skill_desc_text.insert(tk.END, f"Specialization: {current_spec or 'None'}\n")
        self.skill_desc_text.config(state=tk.DISABLED)
    
    def update_skill(self):
        selected = self.skill_tree.selection()
        if selected:
            skill = self.skill_tree.item(selected[0], "text")
            rank = int(self.skill_rank_spin.get())
            spec = self.skill_spec_combo.get()
            
            self.character.skills[skill] = rank
            if spec and spec != "None":
                self.character.specializations[skill] = spec
            elif skill in self.character.specializations:
                del self.character.specializations[skill]
            
            self.skill_tree.item(selected[0], values=(rank, spec))
            self.update_specialization_list()
    
    def setup_qualities_tab(self):
        tab = self.tabs["Qualities"]
        
        # Positive qualities
        pos_frame = ttk.LabelFrame(tab, text="Positive Qualities")
        pos_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.pos_quality_list = tk.Listbox(pos_frame, selectmode=tk.MULTIPLE, height=15, bg="#333", fg="#e0e0e0")
        for quality in ShadowrunCharacter.QUALITIES["Positive"]:
            self.pos_quality_list.insert(tk.END, quality)
        self.pos_quality_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Button(pos_frame, text="Add Selected", command=self.add_pos_quality).pack(pady=5)
        
        # Negative qualities
        neg_frame = ttk.LabelFrame(tab, text="Negative Qualities")
        neg_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.neg_quality_list = tk.Listbox(neg_frame, selectmode=tk.MULTIPLE, height=15, bg="#333", fg="#e0e0e0")
        for quality in ShadowrunCharacter.QUALITIES["Negative"]:
            self.neg_quality_list.insert(tk.END, quality)
        self.neg_quality_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Button(neg_frame, text="Add Selected", command=self.add_neg_quality).pack(pady=5)
        
        # Current qualities
        cur_frame = ttk.LabelFrame(tab, text="Current Qualities")
        cur_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.cur_quality_list = tk.Listbox(cur_frame, height=8, bg="#333", fg="#e0e0e0")
        self.cur_quality_list.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(cur_frame, text="Remove Selected", command=self.remove_quality).pack(pady=5)
    
    def add_pos_quality(self):
        selected = self.pos_quality_list.curselection()
        for index in selected:
            quality = self.pos_quality_list.get(index)
            if quality not in self.character.qualities:
                self.character.qualities.append(quality)
                self.cur_quality_list.insert(tk.END, f"[+] {quality}")
                self.update_derived_stats()
    
    def add_neg_quality(self):
        selected = self.neg_quality_list.curselection()
        for index in selected:
            quality = self.neg_quality_list.get(index)
            if quality not in self.character.qualities:
                self.character.qualities.append(quality)
                self.cur_quality_list.insert(tk.END, f"[-] {quality}")
                self.update_derived_stats()
    
    def remove_quality(self):
        selected = self.cur_quality_list.curselection()
        if selected:
            index = selected[0]
            quality_str = self.cur_quality_list.get(index)
            quality = quality_str[4:]  # Remove [+] or [-]
            if quality in self.character.qualities:
                self.character.qualities.remove(quality)
            self.cur_quality_list.delete(index)
            self.update_derived_stats()
    
    def setup_gear_tab(self):
        tab = self.tabs["Gear"]
        notebook = ttk.Notebook(tab)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create gear category tabs
        self.gear_frames = {}
        for category in ShadowrunCharacter.GEAR_CATEGORIES:
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=category)
            self.gear_frames[category] = frame
            
            # Add/Edit/Remove buttons
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X, padx=5, pady=5)
            
            ttk.Button(btn_frame, text=f"Add {category[:-1]}", 
                      command=lambda c=category: self.add_gear_item(c)).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="Edit Selected", 
                      command=lambda c=category: self.edit_gear_item(c)).pack(side=tk.LEFT, padx=2)
            ttk.Button(btn_frame, text="Remove Selected", 
                      command=lambda c=category: self.remove_gear_item(c)).pack(side=tk.LEFT, padx=2)
            
            # Gear list
            list_frame = ttk.Frame(frame)
            list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            tree = ttk.Treeview(list_frame, columns=("Details"), show="tree", height=10)
            tree.heading("#0", text="Item")
            tree.column("#0", width=200)
            tree.heading("Details", text="Details")
            tree.pack(fill=tk.BOTH, expand=True)
            
            # Bind double-click to edit and view
            tree.bind("<Double-1>", lambda e, c=category: self.view_gear_item(c))
            tree.bind("<<TreeviewSelect>>", lambda e, c=category: self.show_gear_description(c))
            
            setattr(self, f"{category.lower()}_tree", tree)
    
    def show_gear_description(self, category):
        tree = getattr(self, f"{category.lower()}_tree")
        selected = tree.selection()
        if selected:
            index = tree.index(selected[0])
            item = self.character.gear[category][index]
            content = f"Name: {item.get('name', '')}\n\n"
            content += f"Description: {item.get('description', '')}\n\n"
            content += "Attributes:\n"
            for key, value in item.items():
                if key not in ["name", "description"]:
                    content += f"  {key}: {value}\n"
            DescriptionViewer(self.root, "Gear Description", content)
    
    def view_gear_item(self, category):
        tree = getattr(self, f"{category.lower()}_tree")
        selected = tree.selection()
        if selected:
            self.edit_gear_item(category)
    
    def add_gear_item(self, category):
        dialog = EditGearDialog(self.root, category)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.add_gear(category, dialog.result)
            tree = getattr(self, f"{category.lower()}_tree")
            
            # Format details for display - show attributes only
            attrs = []
            for key, value in dialog.result.items():
                if key not in ["name", "description"]:
                    attrs.append(f"{key}: {value}")
            details = "; ".join(attrs)
            tree.insert("", "end", text=dialog.result["name"], values=(details,))
    
    def edit_gear_item(self, category):
        tree = getattr(self, f"{category.lower()}_tree")
        selected = tree.selection()
        
        if not selected:
            return
            
        item_id = selected[0]
        item_index = tree.index(item_id)
        gear_item = self.character.gear[category][item_index]
        
        dialog = EditGearDialog(self.root, category, gear_item)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.update_gear(category, item_index, dialog.result)
            
            # Update tree view - show attributes only
            attrs = []
            for key, value in dialog.result.items():
                if key not in ["name", "description"]:
                    attrs.append(f"{key}: {value}")
            details = "; ".join(attrs)
            tree.item(item_id, text=dialog.result["name"], values=(details,))
    
    def remove_gear_item(self, category):
        tree = getattr(self, f"{category.lower()}_tree")
        selected = tree.selection()
        
        if not selected:
            return
            
        item_id = selected[0]
        item_index = tree.index(item_id)
        
        # Remove from character
        del self.character.gear[category][item_index]
        
        # Remove from tree view
        tree.delete(item_id)
    
    def setup_magic_tab(self):
        tab = self.tabs["Magic/Resonance"]
        notebook = ttk.Notebook(tab)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Spells
        spells_frame = ttk.Frame(notebook)
        notebook.add(spells_frame, text="Spells")
        
        # Spell list with description
        spell_list_frame = ttk.Frame(spells_frame)
        spell_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.spell_tree = ttk.Treeview(spell_list_frame, columns=("Type", "Drain"), show="headings", height=10)
        self.spell_tree.heading("#0", text="Spell")
        self.spell_tree.column("#0", width=150)
        self.spell_tree.heading("Type", text="Type")
        self.spell_tree.column("Type", width=100)
        self.spell_tree.heading("Drain", text="Drain")
        self.spell_tree.column("Drain", width=50)
        self.spell_tree.pack(fill=tk.BOTH, expand=True)
        self.spell_tree.bind("<Double-1>", self.view_spell)
        self.spell_tree.bind("<<TreeviewSelect>>", self.show_spell_description)
        
        ctrl_frame = ttk.Frame(spells_frame)
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(ctrl_frame, text="Add Spell", command=self.add_spell).pack(side=tk.LEFT)
        ttk.Button(ctrl_frame, text="Edit Spell", command=lambda: self.edit_spell(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="Remove Spell", command=self.remove_spell).pack(side=tk.LEFT, padx=5)
        
        # Powers
        powers_frame = ttk.Frame(notebook)
        notebook.add(powers_frame, text="Powers")
        
        # Powers list with description
        power_list_frame = ttk.Frame(powers_frame)
        power_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.power_tree = ttk.Treeview(power_list_frame, columns=("Activation", "Effect"), show="headings", height=10)
        self.power_tree.heading("#0", text="Power")
        self.power_tree.column("#0", width=150)
        self.power_tree.heading("Activation", text="Activation")
        self.power_tree.column("Activation", width=100)
        self.power_tree.heading("Effect", text="Effect")
        self.power_tree.column("Effect", width=100)
        self.power_tree.pack(fill=tk.BOTH, expand=True)
        self.power_tree.bind("<Double-1>", self.view_power)
        self.power_tree.bind("<<TreeviewSelect>>", self.show_power_description)
        
        ctrl_frame = ttk.Frame(powers_frame)
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(ctrl_frame, text="Add Power", command=self.add_power).pack(side=tk.LEFT)
        ttk.Button(ctrl_frame, text="Edit Power", command=lambda: self.edit_power(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="Remove Power", command=self.remove_power).pack(side=tk.LEFT, padx=5)
        
        # Foci
        foci_frame = ttk.Frame(notebook)
        notebook.add(foci_frame, text="Foci")
        
        # Foci list with description
        foci_list_frame = ttk.Frame(foci_frame)
        foci_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.foci_tree = ttk.Treeview(foci_list_frame, columns=("Type", "Force"), show="headings", height=10)
        self.foci_tree.heading("#0", text="Focus")
        self.foci_tree.column("#0", width=150)
        self.foci_tree.heading("Type", text="Type")
        self.foci_tree.column("Type", width=100)
        self.foci_tree.heading("Force", text="Force")
        self.foci_tree.column("Force", width=50)
        self.foci_tree.pack(fill=tk.BOTH, expand=True)
        self.foci_tree.bind("<Double-1>", self.view_focus)
        self.foci_tree.bind("<<TreeviewSelect>>", self.show_focus_description)
        
        ctrl_frame = ttk.Frame(foci_frame)
        ctrl_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(ctrl_frame, text="Add Focus", command=self.add_focus).pack(side=tk.LEFT)
        ttk.Button(ctrl_frame, text="Edit Focus", command=lambda: self.edit_focus(None)).pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="Remove Focus", command=self.remove_focus).pack(side=tk.LEFT, padx=5)
    
    def show_spell_description(self, event=None):
        selected = self.spell_tree.selection()
        if selected:
            index = self.spell_tree.index(selected[0])
            spell = self.character.spells[index]
            content = f"Name: {spell.get('name', '')}\n\n"
            content += f"Type: {spell.get('type', '')}\n"
            content += f"Drain: {spell.get('drain', '')}\n\n"
            content += f"Description: {spell.get('description', '')}"
            DescriptionViewer(self.root, "Spell Description", content)
    
    def view_spell(self, event):
        selected = self.spell_tree.selection()
        if selected:
            self.edit_spell(None)
    
    def add_spell(self):
        dialog = EditGearDialog(self.root, "Spell")
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.spells.append(dialog.result)
            self.spell_tree.insert("", "end", text=dialog.result["name"], 
                                  values=(dialog.result.get("type", ""), dialog.result.get("drain", "")))
    
    def edit_spell(self, event):
        selected = self.spell_tree.selection()
        if not selected:
            return
            
        item_id = selected[0]
        index = self.spell_tree.index(item_id)
        spell = self.character.spells[index]
        
        dialog = EditGearDialog(self.root, "Spell", spell)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.spells[index] = dialog.result
            self.spell_tree.item(item_id, text=dialog.result["name"], 
                               values=(dialog.result.get("type", ""), dialog.result.get("drain", "")))
    
    def remove_spell(self):
        selected = self.spell_tree.selection()
        if selected:
            item_id = selected[0]
            index = self.spell_tree.index(item_id)
            self.character.spells.pop(index)
            self.spell_tree.delete(item_id)
    
    def show_power_description(self, event=None):
        selected = self.power_tree.selection()
        if selected:
            index = self.power_tree.index(selected[0])
            power = self.character.powers[index]
            content = f"Name: {power.get('name', '')}\n\n"
            content += f"Activation: {power.get('activation', '')}\n"
            content += f"Effect: {power.get('effect', '')}\n\n"
            content += f"Description: {power.get('description', '')}"
            DescriptionViewer(self.root, "Power Description", content)
    
    def view_power(self, event):
        selected = self.power_tree.selection()
        if selected:
            self.edit_power(None)
    
    def add_power(self):
        dialog = EditGearDialog(self.root, "Power")
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.powers.append(dialog.result)
            self.power_tree.insert("", "end", text=dialog.result["name"], 
                                  values=(dialog.result.get("activation", ""), dialog.result.get("effect", "")))
    
    def edit_power(self, event):
        selected = self.power_tree.selection()
        if not selected:
            return
            
        item_id = selected[0]
        index = self.power_tree.index(item_id)
        power = self.character.powers[index]
        
        dialog = EditGearDialog(self.root, "Power", power)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.powers[index] = dialog.result
            self.power_tree.item(item_id, text=dialog.result["name"], 
                               values=(dialog.result.get("activation", ""), dialog.result.get("effect", "")))
    
    def remove_power(self):
        selected = self.power_tree.selection()
        if selected:
            item_id = selected[0]
            index = self.power_tree.index(item_id)
            self.character.powers.pop(index)
            self.power_tree.delete(item_id)
    
    def show_focus_description(self, event=None):
        selected = self.foci_tree.selection()
        if selected:
            index = self.foci_tree.index(selected[0])
            focus = self.character.foci[index]
            content = f"Name: {focus.get('name', '')}\n\n"
            content += f"Type: {focus.get('type', '')}\n"
            content += f"Force: {focus.get('force', '')}\n\n"
            content += f"Description: {focus.get('description', '')}"
            DescriptionViewer(self.root, "Focus Description", content)
    
    def view_focus(self, event):
        selected = self.foci_tree.selection()
        if selected:
            self.edit_focus(None)
    
    def add_focus(self):
        dialog = EditGearDialog(self.root, "Focus")
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.foci.append(dialog.result)
            self.foci_tree.insert("", "end", text=dialog.result["name"], 
                                 values=(dialog.result.get("type", ""), dialog.result.get("force", "")))
    
    def edit_focus(self, event):
        selected = self.foci_tree.selection()
        if not selected:
            return
            
        item_id = selected[0]
        index = self.foci_tree.index(item_id)
        focus = self.character.foci[index]
        
        dialog = EditGearDialog(self.root, "Focus", focus)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.foci[index] = dialog.result
            self.foci_tree.item(item_id, text=dialog.result["name"], 
                              values=(dialog.result.get("type", ""), dialog.result.get("force", "")))
    
    def remove_focus(self):
        selected = self.foci_tree.selection()
        if selected:
            item_id = selected[0]
            index = self.foci_tree.index(item_id)
            self.character.foci.pop(index)
            self.foci_tree.delete(item_id)
    
    def setup_contacts_tab(self):
        tab = self.tabs["Contacts"]
        
        # Contact list
        list_frame = ttk.LabelFrame(tab, text="Contacts")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Name", "Type", "Loyalty", "Connection")
        self.contact_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.contact_tree.heading(col, text=col)
            self.contact_tree.column(col, width=100)
        
        self.contact_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.contact_tree.bind("<Double-1>", self.edit_contact)
        self.contact_tree.bind("<<TreeviewSelect>>", self.show_contact_description)
        
        # Contact controls
        ctrl_frame = ttk.Frame(tab)
        ctrl_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(ctrl_frame, text="Add Contact", command=self.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="Edit Contact", command=self.edit_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(ctrl_frame, text="Remove Contact", command=self.remove_contact).pack(side=tk.LEFT, padx=5)
    
    def show_contact_description(self, event=None):
        selected = self.contact_tree.selection()
        if selected:
            item = self.contact_tree.item(selected[0])
            name = item["values"][0]
            
            # Find contact
            contact = None
            for c in self.character.contacts:
                if c["name"] == name:
                    contact = c
                    break
                    
            if contact:
                content = f"Name: {contact.get('name', '')}\n"
                content += f"Type: {contact.get('type', '')}\n"
                content += f"Loyalty: {contact.get('loyalty', '')}\n"
                content += f"Connection: {contact.get('connection', '')}\n\n"
                content += f"Notes:\n{contact.get('notes', '')}"
                DescriptionViewer(self.root, "Contact Details", content)
    
    def add_contact(self):
        dialog = EditContactDialog(self.root)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.character.contacts.append(dialog.result)
            self.contact_tree.insert("", "end", values=(
                dialog.result["name"],
                dialog.result.get("type", ""),
                dialog.result.get("loyalty", ""),
                dialog.result.get("connection", "")
            ))
    
    def edit_contact(self, event=None):
        selected = self.contact_tree.selection()
        if not selected:
            return
            
        item = self.contact_tree.item(selected[0])
        name = item["values"][0]
        
        # Find contact
        contact = None
        for c in self.character.contacts:
            if c["name"] == name:
                contact = c
                break
                
        if not contact:
            return
            
        dialog = EditContactDialog(self.root, contact)
        self.root.wait_window(dialog)
        
        if dialog.result:
            # Update contact data
            contact.update(dialog.result)
            
            # Update tree view
            self.contact_tree.item(selected[0], values=(
                dialog.result["name"],
                dialog.result.get("type", ""),
                dialog.result.get("loyalty", ""),
                dialog.result.get("connection", "")
            ))
    
    def remove_contact(self):
        selected = self.contact_tree.selection()
        if selected:
            item = self.contact_tree.item(selected[0])
            name = item["values"][0]
            for contact in self.character.contacts:
                if contact["name"] == name:
                    self.character.contacts.remove(contact)
                    break
            self.contact_tree.delete(selected[0])
    
    def setup_background_tab(self):
        tab = self.tabs["Background"]
        
        frame = ttk.LabelFrame(tab, text="Character Background")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.background_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=20,
                                                        bg="#333", fg="#e0e0e0", insertbackground="white")
        self.background_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.background_text.bind("<FocusOut>", self.update_derived_stats)
    
    def setup_combat_stats_tab(self):
        tab = self.tabs["Combat Stats"]
        notebook = ttk.Notebook(tab)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Condition monitors
        cond_frame = ttk.Frame(notebook)
        notebook.add(cond_frame, text="Condition Monitors")
        
        # Physical monitor
        phys_frame = ttk.LabelFrame(cond_frame, text="Physical Condition")
        phys_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(phys_frame, text="Damage:").pack(anchor=tk.W, padx=5, pady=2)
        self.phys_damage_label = tk.Label(
            phys_frame, text="0", 
            font=("Arial", 10, "bold"),
            bg="#1c1c1c", fg="white"
        )
        self.phys_damage_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.phys_monitor = tk.Canvas(phys_frame, bg="#1c1c1c", height=200)
        self.phys_monitor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.phys_monitor.bind("<Button-1>", self.toggle_physical_damage)
        
        # Stun monitor
        stun_frame = ttk.LabelFrame(cond_frame, text="Stun Condition")
        stun_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(stun_frame, text="Damage:").pack(anchor=tk.W, padx=5, pady=2)
        self.stun_damage_label = tk.Label(
            stun_frame, text="0", 
            font=("Arial", 10, "bold"),
            bg="#1c1c1c", fg="white"
        )
        self.stun_damage_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.stun_monitor = tk.Canvas(stun_frame, bg="#1c1c1c", height=200)
        self.stun_monitor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.stun_monitor.bind("<Button-1>", self.toggle_stun_damage)
        
        # Combat actions frame
        actions_frame = ttk.Frame(notebook)
        notebook.add(actions_frame, text="Combat Actions")
        
        # Initiative
        init_frame = ttk.LabelFrame(actions_frame, text="Initiative")
        init_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(init_frame, text="Roll Initiative", command=self.roll_initiative).pack(side=tk.LEFT, padx=5, pady=5)
        self.init_result_label = ttk.Label(init_frame, text="Result: -")
        self.init_result_label.pack(side=tk.LEFT, padx=5)
        
        # Healing
        heal_frame = ttk.LabelFrame(actions_frame, text="Healing")
        heal_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(heal_frame, text="Use Medkit", command=self.use_medkit).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(heal_frame, text="Rest", command=self.rest).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Dice roller
        dice_frame = ttk.Frame(notebook)
        notebook.add(dice_frame, text="Dice Roller")
        
        # Roll selection
        roll_frame = ttk.Frame(dice_frame)
        roll_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(roll_frame, text="Roll Type:").pack(side=tk.LEFT, padx=5)
        self.roll_combo = ttk.Combobox(roll_frame, values=ShadowrunCharacter.DICE_ROLL_OPTIONS, width=25)
        self.roll_combo.pack(side=tk.LEFT, padx=5)
        self.roll_combo.set(ShadowrunCharacter.DICE_ROLL_OPTIONS[0])
        
        ttk.Label(roll_frame, text="Dice Pool:").pack(side=tk.LEFT, padx=5)
        self.dice_pool_combo = ttk.Combobox(roll_frame, width=25)
        self.dice_pool_combo.pack(side=tk.LEFT, padx=5)
        
        # Edge use
        edge_frame = ttk.Frame(dice_frame)
        edge_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(edge_frame, text="Use Edge:").pack(side=tk.LEFT, padx=5)
        self.edge_spin = ttk.Spinbox(edge_frame, from_=0, to=3, width=2)
        self.edge_spin.pack(side=tk.LEFT, padx=5)
        self.edge_spin.set("0")
        
        # Roll button
        btn_frame = ttk.Frame(dice_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Roll Dice", command=self.roll_dice).pack()
        
        # Results display
        result_frame = ttk.LabelFrame(dice_frame, text="Results")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, height=10, 
                                                   bg="#333", fg="#e0e0e0", wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.result_text.config(state=tk.DISABLED)
        
        # Combat stats
        stats_frame = ttk.Frame(notebook)
        notebook.add(stats_frame, text="Combat Stats")
        
        stats = [
            ("Initiative Score", "initiative_score"),
            ("Initiative Dice", "initiative_dice"),
            ("Physical Boxes", "physical_boxes"),
            ("Stun Boxes", "stun_boxes"),
            ("Armor Rating", "Armor"),
            ("Weapon Accuracy", "Weapon Accuracy")
        ]
        
        for i, (label, attr) in enumerate(stats):
            ttk.Label(stats_frame, text=label+":").grid(row=i, column=0, sticky=tk.W, padx=5, pady=2)
            value_label = ttk.Label(stats_frame, text="0", font=("Arial", 10, "bold"))
            value_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=2)
            setattr(self, f"{attr.replace(' ', '_').lower()}_label", value_label)
    
    def get_damage_status(self, damage, total_boxes):
        """Return status and color based on damage level"""
        if damage == 0:
            return "Healthy", "#4CAF50"  # Green
        elif damage <= total_boxes // 3:
            return "Light", "#FFEB3B"    # Yellow
        elif damage <= 2 * total_boxes // 3:
            return "Moderate", "#FF9800" # Orange
        else:
            return "Serious", "#F44336"  # Red
    
    def draw_condition_monitors(self):
        # Update damage labels with status indicators
        phys_status, phys_color = self.get_damage_status(
            self.character.physical_damage, 
            self.character.physical_boxes
        )
        stun_status, stun_color = self.get_damage_status(
            self.character.stun_damage, 
            self.character.stun_boxes
        )
        
        self.phys_damage_label.config(
            text=f"{self.character.physical_damage}/{self.character.physical_boxes} ({phys_status})",
            fg=phys_color
        )
        self.stun_damage_label.config(
            text=f"{self.character.stun_damage}/{self.character.stun_boxes} ({stun_status})",
            fg=stun_color
        )
        
        # Draw physical monitor
        self.draw_single_monitor(
            self.phys_monitor, 
            self.character.physical_boxes,
            self.character.physical_damage,
            "#FF5252",  # Light red
            "Physical Condition"
        )
        
        # Draw stun monitor
        self.draw_single_monitor(
            self.stun_monitor, 
            self.character.stun_boxes,
            self.character.stun_damage,
            "#FFC107",  # Amber color
            "Stun Condition"
        )
    
    def draw_single_monitor(self, canvas, total_boxes, damage, damage_color, title):
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # Calculate box size based on available space
        boxes_per_row = min(5, max(3, width // 35))
        box_size = min(30, (width - 20) // boxes_per_row)
        spacing = 5
        
        # Calculate rows needed
        rows = (total_boxes + boxes_per_row - 1) // boxes_per_row
        
        # Draw title
        canvas.create_text(
            10, 10, 
            text=title, 
            anchor=tk.W, 
            fill="#e0e0e0",
            font=("Arial", 10, "bold")
        )
        
        # Draw boxes
        for i in range(total_boxes):
            row = i // boxes_per_row
            col = i % boxes_per_row
            
            x1 = 10 + col * (box_size + spacing)
            y1 = 40 + row * (box_size + spacing)
            x2 = x1 + box_size
            y2 = y1 + box_size
            
            # Determine box color
            if i < damage:
                fill_color = damage_color
            else:
                fill_color = "#444"  # Undamaged
                
            # Draw box
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="#666")
            
            # Add number if space allows
            if box_size > 15:
                canvas.create_text(
                    (x1+x2)/2, (y1+y2)/2,
                    text=str(i+1),
                    fill="white" if i < damage else "#aaa"
                )
        
        # Draw thresholds
        thresholds = [
            (total_boxes // 3, "Light", "#FFEB3B"),
            (2 * total_boxes // 3, "Moderate", "#FF9800"),
            (total_boxes, "Serious", "#F44336")
        ]
        
        for threshold, label, color in thresholds:
            if threshold < total_boxes:
                row = threshold // boxes_per_row
                y_pos = 40 + row * (box_size + spacing) - 2
                
                canvas.create_line(
                    5, y_pos, width-5, y_pos, 
                    fill=color, dash=(4, 2), width=2
                )
                canvas.create_text(
                    width-5, y_pos-10, 
                    text=f"{label} ({threshold})", 
                    anchor=tk.E, 
                    fill=color,
                    font=("Arial", 8)
                )
    
    def toggle_physical_damage(self, event):
        box_size = 30
        spacing = 5
        boxes_per_row = min(5, max(3, self.phys_monitor.winfo_width() // 35))
        
        x = event.x
        y = event.y
        
        # Calculate which box was clicked
        row = (y - 40) // (box_size + spacing)
        col = (x - 10) // (box_size + spacing)
        box_index = row * boxes_per_row + col
        
        if box_index >= 0 and box_index < self.character.physical_boxes:
            if box_index < self.character.physical_damage:
                # Remove damage
                self.character.physical_damage -= 1
            else:
                # Add damage
                self.character.physical_damage += 1
                
            self.draw_condition_monitors()
    
    def toggle_stun_damage(self, event):
        box_size = 30
        spacing = 5
        boxes_per_row = min(5, max(3, self.stun_monitor.winfo_width() // 35))
        
        x = event.x
        y = event.y
        
        # Calculate which box was clicked
        row = (y - 40) // (box_size + spacing)
        col = (x - 10) // (box_size + spacing)
        box_index = row * boxes_per_row + col
        
        if box_index >= 0 and box_index < self.character.stun_boxes:
            if box_index < self.character.stun_damage:
                # Remove damage
                self.character.stun_damage -= 1
            else:
                # Add damage
                self.character.stun_damage += 1
                
            self.draw_condition_monitors()
    
    def update_dice_pool_options(self):
        """Update dice pool options based on character skills and attributes"""
        options = []
        
        # Add attributes
        for attr in ["Body", "Agility", "Reaction", "Strength", "Willpower", 
                    "Logic", "Intuition", "Charisma", "Edge"]:
            value = self.character.attributes[attr]
            if value > 0:
                options.append(f"{attr} ({value})")
        
        # Add skills
        for skill, rank in self.character.skills.items():
            if rank > 0:
                options.append(f"{skill} ({rank})")
        
        # Add spells
        for spell in self.character.spells:
            options.append(f"Spell: {spell.get('name', '')}")
        
        # Add powers
        for power in self.character.powers:
            options.append(f"Power: {power.get('name', '')}")
        
        # Add foci
        for focus in self.character.foci:
            options.append(f"Focus: {focus.get('name', '')}")
        
        self.dice_pool_combo["values"] = options
        if options:
            self.dice_pool_combo.set(options[0])
    
    def roll_dice(self):
        # Update edge max value
        self.edge_spin.config(to=self.character.attributes["Edge"])
        
        try:
            # Parse dice pool from combo selection
            dice_pool_text = self.dice_pool_combo.get()
            if "(" in dice_pool_text and ")" in dice_pool_text:
                pool_size = int(dice_pool_text.split("(")[1].split(")")[0])
            else:
                # Try to match gear, spells, or other special items
                pool_size = self.get_special_dice_pool(dice_pool_text)
        except (ValueError, IndexError):
            pool_size = 0
            
        edge_use = int(self.edge_spin.get() or "0")
        
        # Validate edge usage
        if edge_use > 0 and self.character.attributes["Edge"] <= 0:
            messagebox.showwarning("No Edge", "Character has no Edge points available!")
            return
        
        result = self.character.roll_dice(pool_size, edge_use)
        
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        roll_type = self.roll_combo.get()
        self.result_text.insert(tk.END, f"Rolling {roll_type} ({pool_size} dice, Edge {edge_use}):\n")
        self.result_text.insert(tk.END, f"Dice: {', '.join(map(str, result['dice']))}\n")
        
        if result['critical_glitch']:
            self.result_text.insert(tk.END, "CRITICAL GLITCH! ", "critical")
            self.result_text.insert(tk.END, "No successes and more than half are 1s\n")
        elif result['glitch']:
            self.result_text.insert(tk.END, "GLITCH! ", "glitch")
            self.result_text.insert(tk.END, "More than half of dice are 1s\n")
        
        self.result_text.insert(tk.END, f"Successes: {result['hits']}\n")
        
        # Color the results
        self.result_text.tag_config("success", foreground="#4CAF50")
        self.result_text.tag_config("glitch", foreground="#FF9800")
        self.result_text.tag_config("critical", foreground="#F44336")
        
        if result['hits'] > 0:
            self.result_text.insert(tk.END, "SUCCESS!", "success")
        else:
            self.result_text.insert(tk.END, "FAILURE", "critical")
        
        self.result_text.config(state=tk.DISABLED)
    
    def get_special_dice_pool(self, dice_pool_text):
        """Get dice pool for spells, powers, or gear"""
        pool_size = 0
        
        # Check for spell
        if dice_pool_text.startswith("Spell: "):
            spell_name = dice_pool_text[7:]
            for spell in self.character.spells:
                if spell["name"] == spell_name:
                    # Base pool is Magic + Spellcasting
                    pool_size = self.character.attributes["Magic"]
                    if "Sorcery" in self.character.skills:
                        pool_size += self.character.skills["Sorcery"]
                    break
        
        # Check for power
        elif dice_pool_text.startswith("Power: "):
            power_name = dice_pool_text[7:]
            for power in self.character.powers:
                if power["name"] == power_name:
                    # Base pool is Magic + relevant skill
                    pool_size = self.character.attributes["Magic"]
                    if "Sorcery" in self.character.skills:
                        pool_size += self.character.skills["Sorcery"]
                    break
        
        # Check for focus
        elif dice_pool_text.startswith("Focus: "):
            focus_name = dice_pool_text[7:]
            for focus in self.character.foci:
                if focus["name"] == focus_name:
                    # Base pool is Magic + relevant skill
                    pool_size = self.character.attributes["Magic"]
                    if "Sorcery" in self.character.skills:
                        pool_size += self.character.skills["Sorcery"]
                    break
        
        # Check for weapon
        elif dice_pool_text.startswith("Weapon: "):
            weapon_name = dice_pool_text[8:]
            for weapon in self.character.gear["Weapons"]:
                if weapon["name"] == weapon_name:
                    # Base pool is Agility + Firearms
                    pool_size = self.character.attributes["Agility"]
                    if "Firearms" in self.character.skills:
                        pool_size += self.character.skills["Firearms"]
                    break
        
        return pool_size
    
    def roll_initiative(self):
        result, dice_rolls = self.character.roll_initiative()
        self.init_result_label.config(text=f"Result: {result} (Dice: {dice_rolls})")
    
    def use_medkit(self):
        if self.character.use_medkit():
            self.draw_condition_monitors()
            messagebox.showinfo("Medkit Used", "Medkit applied! Physical and stun damage reduced.")
        else:
            messagebox.showwarning("No Medkit", "No medkit found in your gear!")
    
    def rest(self):
        self.character.rest()
        self.draw_condition_monitors()
        messagebox.showinfo("Rest", "Character rested. Stun damage reduced by 1.")
    
    def update_all_fields(self):
        # Basic Info
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, self.character.name)
        
        self.metatype_combo.set(self.character.metatype)
        self.role_combo.set(self.character.role)
        self.magic_combo.set(self.character.magic_type)
        self.tradition_combo.set(self.character.tradition)
        self.init_grade_spin.delete(0, tk.END)
        self.init_grade_spin.insert(0, str(self.character.initiation_grade))
        self.lifestyle_combo.set(self.character.lifestyle)
        self.karma_spin.delete(0, tk.END)
        self.karma_spin.insert(0, str(self.character.karma))
        self.nuyen_entry.delete(0, tk.END)
        self.nuyen_entry.insert(0, str(self.character.nuyen))
        
        # Attributes
        for attr in ShadowrunCharacter.ATTRIBUTES:
            self.attribute_vars[attr].set(self.character.base_attributes[attr])
            
            # Show metatype bonus with color coding
            bonus = self.character.attributes[attr] - self.character.base_attributes[attr]
            bonus_label = getattr(self, f"{attr.lower()}_bonus_label")
            if bonus != 0:
                bonus_text = f"+{bonus}" if bonus > 0 else str(bonus)
                bonus_label.config(text=bonus_text)
                # Set color to red if negative
                if bonus < 0:
                    bonus_label.config(foreground="#FF5252")  # Red for negative
                else:
                    bonus_label.config(foreground="#4F9BFF")  # Blue for positive
            else:
                bonus_label.config(text="")
        
        # Skills
        for skill in self.skill_tree.get_children():
            self.skill_tree.delete(skill)
        
        for skill, rank in self.character.skills.items():
            spec = self.character.specializations.get(skill, "")
            self.skill_tree.insert("", "end", text=skill, values=(rank, spec))
        
        # Qualities
        self.cur_quality_list.delete(0, tk.END)
        for quality in self.character.qualities:
            prefix = "[+]" if quality in ShadowrunCharacter.QUALITIES["Positive"] else "[-]"
            self.cur_quality_list.insert(tk.END, f"{prefix} {quality}")
        
        # Gear
        for category in ShadowrunCharacter.GEAR_CATEGORIES:
            tree = getattr(self, f"{category.lower()}_tree")
            for item in tree.get_children():
                tree.delete(item)
            
            for item in self.character.gear[category]:
                # Format attributes for display
                attrs = []
                for key, value in item.items():
                    if key not in ["name", "description"]:
                        attrs.append(f"{key}: {value}")
                details = "; ".join(attrs)
                tree.insert("", "end", text=item.get("name", "Unknown"), values=(details,))
        
        # Magic
        self.spell_tree.delete(*self.spell_tree.get_children())
        for spell in self.character.spells:
            self.spell_tree.insert("", "end", text=spell.get("name", ""), 
                                  values=(spell.get("type", ""), spell.get("drain", "")))
        
        self.power_tree.delete(*self.power_tree.get_children())
        for power in self.character.powers:
            self.power_tree.insert("", "end", text=power.get("name", ""), 
                                  values=(power.get("activation", ""), power.get("effect", "")))
        
        self.foci_tree.delete(*self.foci_tree.get_children())
        for focus in self.character.foci:
            self.foci_tree.insert("", "end", text=focus.get("name", ""), 
                                 values=(focus.get("type", ""), focus.get("force", "")))
        
        # Contacts
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)
        
        for contact in self.character.contacts:
            self.contact_tree.insert("", "end", values=(
                contact.get("name", "Unknown"),
                contact.get("type", ""),
                contact.get("loyalty", 0),
                contact.get("connection", 0)
            ))
        
        # Background
        self.background_text.delete(1.0, tk.END)
        self.background_text.insert(tk.END, self.character.background)
        
        # Update derived stats display
        self.update_derived_stats()
        
        # Update dice pool options
        self.update_dice_pool_options()
    
    def update_derived_stats(self, event=None):
        # Save current values to character object
        self.character.name = self.name_entry.get()
        self.character.metatype = self.metatype_combo.get()
        self.character.role = self.role_combo.get()
        self.character.magic_type = self.magic_combo.get()
        self.character.tradition = self.tradition_combo.get()
        self.character.initiation_grade = int(self.init_grade_spin.get() or "0")
        self.character.lifestyle = self.lifestyle_combo.get()
        self.character.karma = int(self.karma_spin.get() or "0")
        self.character.nuyen = int(self.nuyen_entry.get() or "0")
        self.character.background = self.background_text.get(1.0, tk.END).strip()
        
        for attr in ShadowrunCharacter.ATTRIBUTES:
            try:
                self.character.base_attributes[attr] = int(self.attribute_vars[attr].get())
            except tk.TclError:
                pass
        
        # Recalculate derived stats
        self.character.calculate_derived_stats()
        
        # Update combat stats display
        self.initiative_score_label.config(text=str(self.character.initiative_score))
        self.initiative_dice_label.config(text=str(self.character.initiative_dice))
        self.physical_boxes_label.config(text=str(self.character.physical_boxes))
        self.stun_boxes_label.config(text=str(self.character.stun_boxes))
        self.armor_label.config(text=str(self.character.attributes.get("Armor", 0)))
        self.weapon_accuracy_label.config(text=str(self.character.attributes.get("Weapon Accuracy", 0)))
        
        # Redraw condition monitors
        self.draw_condition_monitors()
        
        # Update dice pool options
        self.update_dice_pool_options()
    
    def new_character(self):
        self.character.reset_character()
        self.update_all_fields()
        messagebox.showinfo("New Character", "New character created successfully!")
    
    def save_character(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".sr6",
            filetypes=[("Shadowrun 6E Characters", "*.sr6"), ("All Files", "*.*")]
        )
        if file_path:
            data = self.character.to_dict()
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Save Character", "Character saved successfully!")
    
    def load_character(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Shadowrun 6E Characters", "*.sr6"), ("All Files", "*.*")]
        )
        if file_path and os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
            self.character.from_dict(data)
            self.update_all_fields()
            messagebox.showinfo("Load Character", "Character loaded successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CharacterSheetApp(root)
    
    # Schedule the first drawing of condition monitors
    root.after(100, app.draw_condition_monitors)
    
    # Bind window resize to redraw monitors
    root.bind("<Configure>", lambda e: app.draw_condition_monitors())
    
    root.mainloop()
