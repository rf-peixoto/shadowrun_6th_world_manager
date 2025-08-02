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
    
    # Qualities with attribute effects and karma costs
    QUALITY_EFFECTS = {
        "Analytical Mind": {"Logic": 1, "karma": 7},
        "Toughness": {"Body": 1, "karma": 9},
        "Indomitable": {"Willpower": 1, "karma": 8},
        "Ambidextrous": {"Agility": 1, "karma": 6},
        "Natural Athlete": {"Strength": 1, "Agility": 1, "karma": 10},
        "Uncouth": {"Charisma": -2, "karma": -12},
        "Uneducated": {"Logic": -2, "karma": -10},
        "Incompetent": {"Logic": -1, "Intuition": -1, "karma": -14},
        "High Pain Tolerance": {"karma": 7},
        "Lucky": {"karma": 12},
        "Guts": {"karma": 8},
        "Catlike": {"Agility": 1, "karma": 9},
        "Addiction": {"karma": -8},
        "Allergy": {"karma": -10},
        "Bad Luck": {"karma": -12},
        "Bad Rep": {"karma": -7},
        "Photographic Memory": {"Logic": 1, "karma": 6},
        "Quick Healer": {"Body": 1, "karma": 8},
        "Will to Live": {"karma": 6},
        "Sensitive System": {"karma": -12},
        "Simsense Vertigo": {"karma": -10},
        "Social Stress": {"karma": -8},
        "Spirit Bane": {"karma": -9}
    }
    
    GEAR_CATEGORIES = ["Weapons", "Armor", "Cyberware", "Bioware", "Magic Items", "Electronics", "Medkits", "Other"]
    WEAPON_TYPES = ["Blades", "Clubs", "Thrown", "Pistols", "Rifles", "Shotguns", "Machine Guns", "Special"]
    ARMOR_TYPES = ["Clothing", "Armor Jacket", "Full Body Armor", "Helmet", "Shield"]
    CYBERWARE_TYPES = ["Headware", "Eyeware", "Earware", "Bodyware", "Cyberlimbs", "Implants"]
    MEDKIT_TYPES = ["Rating 1", "Rating 3", "Rating 6", "Rating 10"]
    
    # Contact types and loyalty levels
    CONTACT_TYPES = ["Fixer", "Johnson", "Gang", "Corporate", "Police", "Media", "Talislegger", "Decker", "Street Doc"]
    LOYALTY_LEVELS = ["Unknown", "Known", "Transactional", "Regular", "Professional", "Respectful", "Reliable", "Supportive", "Loyal", "Devoted", "Family"]
    
    # Edge actions and costs
    EDGE_ACTIONS = {
        "Reroll Non-Hits (1 Edge)": 1,
        "Seal Fate (1 Edge)": 1,
        "Push the Limit (4 Edge)": 4,
        "Heroic Effort (3 Edge)": 3,
        "Battle Hardened (2 Edge)": 2
    }
    
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
    
    # Predefined spells, powers, and foci
    PREDEFINED_SPELLS = [
        {"name": "Power Bolt", "type": "Combat", "drain": "F", "description": "Direct combat spell that deals physical damage"},
        {"name": "Stun Bolt", "type": "Combat", "drain": "F", "description": "Direct combat spell that deals stun damage"},
        {"name": "Heal", "type": "Health", "drain": "F", "description": "Heals physical damage"},
        {"name": "Invisibility", "type": "Illusion", "drain": "F", "description": "Makes the target invisible"},
        {"name": "Levitate", "type": "Manipulation", "drain": "F", "description": "Allows the target to levitate"}
    ]
    
    PREDEFINED_POWERS = [
        {"name": "Improved Reflexes", "activation": "Passive", "effect": "+1d6 Initiative Dice", "description": "Improves reaction time"},
        {"name": "Combat Sense", "activation": "Passive", "effect": "+1 Defense Rating", "description": "Enhances combat awareness"},
        {"name": "Killing Hands", "activation": "Simple Action", "effect": "Unarmed attacks deal physical damage", "description": "Channels energy into unarmed strikes"},
        {"name": "Astral Perception", "activation": "Simple Action", "effect": "See into astral plane", "description": "Perceives astral space"},
        {"name": "Pain Resistance", "activation": "Passive", "effect": "+2 damage resistance", "description": "Reduces effects of pain"}
    ]
    
    PREDEFINED_FOCI = [
        {"name": "Power Focus", "type": "Sustaining", "force": 3, "description": "Increases Magic attribute"},
        {"name": "Weapon Focus", "type": "Weapon", "force": 2, "description": "Enhances a specific weapon"},
        {"name": "Spellcasting Focus", "type": "Spell", "force": 1, "description": "Improves spellcasting"},
        {"name": "Qi Focus", "type": "Adept", "force": 2, "description": "Enhances adept powers"},
        {"name": "Binding Focus", "type": "Binding", "force": 3, "description": "Aids in spirit binding"}
    ]
    
    # Predefined gear with attributes and Prices
    PREDEFINED_GEAR = {
        "Weapons": [
            {"name": "Ares Predator V", "Damage": "5P", "Accuracy": "5", "AP": "-1", "Mode": "SA", "RC": "0", "Ammo": "15", "Type": "Pistol", "Price": 800},
            {"name": "Remington Roomsweeper", "Damage": "4P", "Accuracy": "4", "AP": "-1", "Mode": "SS", "RC": "0", "Ammo": "5", "Type": "Shotgun", "Price": 450},
            {"name": "AK-97", "Damage": "6P", "Accuracy": "5", "AP": "-2", "Mode": "SA/BF/FA", "RC": "1", "Ammo": "38", "Type": "Rifle", "Price": 1200}
        ],
        "Armor": [
            {"name": "Armor Jacket", "Rating": "4", "Social": "0", "Capacity": "6", "Type": "Jacket", "Price": 1000},
            {"name": "Full Body Armor", "Rating": "6", "Social": "-4", "Capacity": "10", "Type": "Full Body", "Price": 2500},
            {"name": "Ballistic Mask", "Rating": "+2", "Social": "-2", "Capacity": "0", "Type": "Helmet", "Price": 300}
        ],
        "Cyberware": [
            {"name": "Datajack", "Essence Cost": "0.2", "Capacity": "-", "Rating": "-", "Type": "Headware", "Price": 500},
            {"name": "Cybereyes", "Essence Cost": "0.4", "Capacity": "6", "Rating": "3", "Type": "Eyeware", "Price": 2000},
            {"name": "Wired Reflexes", "Essence Cost": "1.0", "Capacity": "-", "Rating": "2", "Type": "Bodyware", "Price": 15000}
        ],
        "Bioware": [
            {"name": "Muscle Augmentation", "Essence Cost": "0.6", "Rating": "2", "Capacity": "-", "Type": "Muscle", "Price": 12000},
            {"name": "Synaptic Booster", "Essence Cost": "0.8", "Rating": "2", "Capacity": "-", "Type": "Nervous", "Price": 18000},
            {"name": "Tailored Pheromones", "Essence Cost": "0.4", "Rating": "3", "Capacity": "-", "Type": "Endocrine", "Price": 10000}
        ]
    }
    
    # Vehicle types
    VEHICLE_TYPES = [
        "Motorcycle", "Sedan", "Sports Car", "Truck", "Helicopter", 
        "Drone", "Boat", "VTOL", "Submarine", "Walker"
    ]
    
    # Minor and Major Actions
    MINOR_ACTIONS = [
        "Free Action", "Simple Action", "Interrupt Action", "Change Gun Mode",
        "Drop Prone", "Stand Up", "Reload Weapon", "Activate Device"
    ]
    
    MAJOR_ACTIONS = [
        "Complex Action", "Full Attack", "Cast Spell", "Summon Spirit",
        "Hack Device", "Pilot Vehicle", "Full Defense", "Overwatch"
    ]
    
    def __init__(self):
        self.reset_character()
        
    def reset_character(self):
        self.name = ""
        self.metatype = "Human"
        self.role = ""
        self.background = ""
        self.lifestyle = "Low"
        self.karma = 50  # Default karma set to 50
        self.nuyen = 5000
        self.magic_type = "Mundane"
        self.tradition = ""
        self.mentor_spirit = ""
        self.initiation_grade = 0
        self.age = 25
        self.reputation = 0  # New reputation field
        
        # Attributes
        self.attributes = {attr: 1 for attr in self.ATTRIBUTES}
        self.attributes["Edge"] = 1
        self.attributes["Essence"] = 6.0
        self.base_attributes = self.attributes.copy()  # Store base attributes without bonuses
        self.current_edge = self.attributes["Edge"]  # Track current Edge points
        
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
        self.physical_damage = 0
        self.stun_damage = 0
        self.initiative_passed = 0
        self.damage_penalty = 0  # Track damage penalty
        self.calculate_derived_stats()
    
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
                    if attr != "karma":  # Skip karma entry
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
        
        # Calculate damage penalty
        self.damage_penalty = -(self.physical_damage // 3 + self.stun_damage // 3)

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
    
    def roll_dice(self, pool_size, edge_action=None, use_wild_die=False):
        """Roll dice for Shadowrun system with edge options and wild die"""
        if pool_size <= 0:
            return {"dice": [], "hits": 0, "glitch": False, "critical_glitch": False}
        
        # Apply damage penalty
        pool_size += self.damage_penalty
        
        # Handle edge actions
        extra_hits = 0
        reroll_non_hits = False
        seal_fate = False
        battle_hardened = False
        
        if edge_action:
            if edge_action == "Reroll Non-Hits (1 Edge)":
                reroll_non_hits = True
            elif edge_action == "Seal Fate (1 Edge)":
                seal_fate = True
            elif edge_action == "Push the Limit (4 Edge)":
                # Add Edge attribute to dice pool
                pool_size += self.attributes["Edge"]
            elif edge_action == "Heroic Effort (3 Edge)":
                # Buy automatic hits
                extra_hits = min(3, self.current_edge)  # Max 3 automatic hits
            elif edge_action == "Battle Hardened (2 Edge)":
                battle_hardened = True
        
        dice = []
        wild_die_result = None
        wild_die_hits = 0
        
        if not edge_action or edge_action != "Heroic Effort (3 Edge)":
            # Roll initial dice
            dice = [random.randint(1, 6) for _ in range(pool_size)]
            
            # Handle wild die
            if use_wild_die and pool_size > 0:
                wild_die = dice.pop(0)
                wild_die_result = [wild_die]
                
                # Check for exploding wild die
                while wild_die == 6:
                    wild_die = random.randint(1, 6)
                    wild_die_result.append(wild_die)
                    wild_die_hits += 1
                
                # If wild die is 6, count as hit
                if 6 in wild_die_result:
                    wild_die_hits += 1
                
                # If wild die is 1, cancel one hit
                if 1 in wild_die_result:
                    wild_die_hits = -1
            
            # Reroll non-hits if selected
            if reroll_non_hits:
                non_hits = [r for r in dice if r < 5]
                rerolled = [random.randint(1, 6) for _ in non_hits]
                dice = [r for r in dice if r >= 5] + rerolled
            
            # Seal Fate - reroll any number of dice (here we reroll all non-hits and non-1s)
            if seal_fate:
                to_reroll = [r for r in dice if r < 5 and r != 1]
                rerolled = [random.randint(1, 6) for _ in to_reroll]
                dice = [r for r in dice if r >= 5 or r == 1] + rerolled
        
        hits = sum(1 for r in dice if r >= 5) + extra_hits + wild_die_hits
        ones = sum(1 for r in dice if r == 1)
        total_dice = len(dice)
        
        glitch = ones > total_dice / 2
        critical_glitch = glitch and hits == 0
        
        # Apply Battle Hardened effect
        if battle_hardened and "Defense" in self.roll_combo.get():
            hits += self.attributes["Edge"]
        
        return {
            "dice": dice,
            "hits": max(0, hits),
            "glitch": glitch,
            "critical_glitch": critical_glitch,
            "wild_die": wild_die_result
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
        self.calculate_derived_stats()
    
    def use_medkit(self):
        """Use a medkit to heal damage if available"""
        if not self.gear["Medkits"]:
            return False
            
        # Use the first medkit in the list
        medkit = self.gear["Medkits"][0]
        
        # Extract rating from medkit (stored as 'Rating' attribute)
        rating = 1
        if "Rating" in medkit:
            try:
                # Extract numeric value from string like "Rating 3"
                rating_str = medkit["Rating"]
                if " " in rating_str:
                    rating = int(rating_str.split()[1])
                else:
                    rating = int(rating_str)
            except (ValueError, IndexError):
                pass
        
        # Apply healing (p.220-221)
        self.heal_damage("physical", rating * 2)
        self.heal_damage("stun", rating)
        
        # Handle quantity
        quantity = 1
        if "Quantity" in medkit:
            try:
                quantity = int(medkit["Quantity"])
            except ValueError:
                pass
        
        # Decrement quantity
        quantity -= 1
        
        if quantity <= 0:
            # Remove medkit if no uses left
            self.gear["Medkits"].pop(0)
        else:
            # Update quantity
            medkit["Quantity"] = str(quantity)
            
        return True
    
    def rest(self):
        """Rest to recover stun damage"""
        self.heal_damage("stun", 1)
    
    def reset_edge(self):
        """Reset current Edge to maximum value"""
        self.current_edge = self.attributes["Edge"]
    
    def trade_karma_for_nuyen(self, amount):
        """Trade karma for nuyen (2000 nuyen per 1 karma)"""
        if self.karma >= amount:
            self.karma -= amount
            self.nuyen += amount * 2000
            return True
        return False
    
    def increase_attribute(self, attribute):
        """Increase attribute using karma"""
        current_rating = self.base_attributes[attribute]
        karma_cost = (current_rating + 1) * 5
        
        if self.karma >= karma_cost:
            self.karma -= karma_cost
            self.base_attributes[attribute] = current_rating + 1
            self.calculate_derived_stats()
            return True
        return False
    
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
            "age": self.age,
            "reputation": self.reputation,
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
            "stun_damage": self.stun_damage,
            "current_edge": self.current_edge,
            "damage_penalty": self.damage_penalty
        }
    
    def from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Set base attributes if not present in saved data
        if not hasattr(self, 'base_attributes'):
            self.base_attributes = self.attributes.copy()
            
        # Ensure current_edge exists
        if not hasattr(self, 'current_edge'):
            self.current_edge = self.attributes["Edge"]
            
        # Ensure reputation exists
        if not hasattr(self, 'reputation'):
            self.reputation = 0
            
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
        "Weapons": ["Damage", "Accuracy", "AP", "Mode", "RC", "Ammo", "Type", "Price"],
        "Armor": ["Rating", "Social", "Capacity", "Type", "Price"],
        "Cyberware": ["Essence Cost", "Capacity", "Rating", "Type", "Price"],
        "Bioware": ["Essence Cost", "Rating", "Capacity", "Type", "Price"],
        "Magic Items": ["Force", "Type", "Binding", "Price"],
        "Medkits": ["Rating", "Quantity", "Type", "Price"],
        "Electronics": ["Rating", "Capacity", "Function", "Price"],
        "Other": ["Effect", "Duration", "Potency", "Price"],
        "Spell": ["Type", "Drain", "Price"],
        "Power": ["Activation", "Effect", "Price"],
        "Focus": ["Type", "Force", "Price"]
    }
    
    GEAR_OPTIONS = {
        ("Weapons", "Type"): ShadowrunCharacter.WEAPON_TYPES,
        ("Armor", "Type"): ShadowrunCharacter.ARMOR_TYPES,
        ("Cyberware", "Type"): ShadowrunCharacter.CYBERWARE_TYPES,
        ("Medkits", "Type"): ShadowrunCharacter.MEDKIT_TYPES,
        ("Spell", "Type"): ["Combat", "Health", "Illusion", "Manipulation"],
        ("Power", "Activation"): ["Passive", "Simple Action", "Complex Action"],
        ("Focus", "Type"): ["Sustaining", "Weapon", "Spell", "Adept", "Binding"]
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
        
        # Predefined items button
        if self.category in ["Spell", "Power", "Focus", "Weapons", "Armor", "Cyberware", "Bioware"]:
            btn_frame = ttk.Frame(main_frame)
            btn_frame.grid(row=0, column=0, columnspan=2, pady=5)
            ttk.Button(btn_frame, text="Use Predefined", command=self.use_predefined).pack(side=tk.LEFT)
        
        # Name
        ttk.Label(main_frame, text="Name:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.name_entry.insert(0, self.item.get("name", ""))
        
        # Description
        ttk.Label(main_frame, text="Description:").grid(row=2, column=0, sticky=tk.NW, padx=5, pady=5)
        self.desc_text = scrolledtext.ScrolledText(main_frame, width=30, height=4, 
                                                  bg="#333", fg="#e0e0e0", insertbackground="white")
        self.desc_text.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.desc_text.insert(tk.END, self.item.get("description", ""))
        
        # Standard attributes for category
        row = 3
        self.attr_entries = {}
        for attr in self.GEAR_ATTRIBUTES.get(self.category, []):
            ttk.Label(main_frame, text=f"{attr}:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=2)
            
            # Check if this attribute should be a dropdown
            options = self.GEAR_OPTIONS.get((self.category, attr))
            if options:
                # Create combobox for attributes with predefined options
                entry = ttk.Combobox(main_frame, values=options, width=15)
                entry.set(self.item.get(attr, options[0] if options else ""))
            elif attr == "Quantity" or attr == "Rating" or attr == "Force":
                # Create spinbox for quantity and rating
                entry = ttk.Spinbox(main_frame, from_=1, to=100, width=15)
                entry.set(str(self.item.get(attr, "1")))
            elif attr == "Price":
                # Create entry with validation for Price
                entry = ttk.Entry(main_frame, width=15)
                entry.insert(0, str(self.item.get(attr, "0")))
            else:
                # Create regular entry field
                entry = ttk.Entry(main_frame, width=15)
                entry.insert(0, str(self.item.get(attr, "")))
                
            entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=2)
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
    
    def use_predefined(self):
        """Load predefined items based on category"""
        if self.category == "Spell":
            predefined = ShadowrunCharacter.PREDEFINED_SPELLS
            title = "Select Spell"
        elif self.category == "Power":
            predefined = ShadowrunCharacter.PREDEFINED_POWERS
            title = "Select Power"
        elif self.category == "Focus":
            predefined = ShadowrunCharacter.PREDEFINED_FOCI
            title = "Select Focus"
        elif self.category == "Weapons":
            predefined = ShadowrunCharacter.PREDEFINED_GEAR["Weapons"]
            title = "Select Weapon"
        elif self.category == "Armor":
            predefined = ShadowrunCharacter.PREDEFINED_GEAR["Armor"]
            title = "Select Armor"
        elif self.category == "Cyberware":
            predefined = ShadowrunCharacter.PREDEFINED_GEAR["Cyberware"]
            title = "Select Cyberware"
        elif self.category == "Bioware":
            predefined = ShadowrunCharacter.PREDEFINED_GEAR["Bioware"]
            title = "Select Bioware"
        else:
            return
        
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.configure(bg="#1c1c1c")
        
        # Create listbox
        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        listbox = tk.Listbox(list_frame, bg="#333", fg="#e0e0e0", font=("Arial", 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for item in predefined:
            listbox.insert(tk.END, item["name"])
        
        # Button to select
        def select_item():
            selected = listbox.curselection()
            if selected:
                item = predefined[selected[0]]
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, item.get("name", ""))
                self.desc_text.delete(1.0, tk.END)
                self.desc_text.insert(tk.END, item.get("description", ""))
                
                # Set attributes
                for attr, widget in self.attr_entries.items():
                    if attr in item:
                        if isinstance(widget, ttk.Combobox):
                            widget.set(item[attr])
                        else:
                            widget.delete(0, tk.END)
                            widget.insert(0, str(item[attr]))
                
                dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Select", command=select_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required")
            return
            
        # Get description
        description = self.desc_text.get("1.0", tk.END).strip()
        
        # Get standard attributes
        attributes = {}
        for attr, widget in self.attr_entries.items():
            value = widget.get().strip()
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
            ("Loyalty:", "loyalty", "loyalty_combo"),  # Changed to custom type
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
            elif field_type == "loyalty_combo":  # Custom field type for loyalty
                entry = ttk.Combobox(main_frame, width=27)
                entry["values"] = ShadowrunCharacter.LOYALTY_LEVELS
                entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                if self.contact.get(key):
                    entry.set(self.contact[key])
            elif field_type == "combo":
                entry = ttk.Combobox(main_frame, width=27)
                if key == "type":
                    entry["values"] = ShadowrunCharacter.CONTACT_TYPES
                entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)
                if self.contact.get(key):
                    entry.set(self.contact[key])
            elif field_type == "spin":
                entry = ttk.Spinbox(main_frame, from_=1, to=6, width=5)
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
            if isinstance(widget, (ttk.Entry, ttk.Combobox, ttk.Spinbox)):
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
        self.karma_spin.set(50)  # Default karma
        
        # Nuyen
        ttk.Label(char_frame, text="Nuyen:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.nuyen_entry = ttk.Entry(char_frame, width=15)
        self.nuyen_entry.grid(row=4, column=1, padx=5, pady=2, sticky=tk.W)
        
        # Trade Karma for Nuyen button
        ttk.Button(char_frame, text="Trade Karma for Nuyen", 
                  command=self.trade_karma_for_nuyen).grid(row=4, column=2, padx=5, pady=2, sticky=tk.W)
        ttk.Label(char_frame, text="1 Karma = 2000¥").grid(row=4, column=3, padx=5, pady=2, sticky=tk.W)
        
        # Attributes frame
        attr_frame = ttk.Frame(notebook)
        notebook.add(attr_frame, text="Attributes")
        
        self.attribute_vars = {}
        self.attribute_entries = {}
        
        # Use a grid layout with 3 columns per row for more space
        for i, attr in enumerate(ShadowrunCharacter.ATTRIBUTES):
            row = i // 3
            col = (i % 3) * 4  # Each attribute takes 4 columns
            
            ttk.Label(attr_frame, text=f"{attr}:").grid(row=row, column=col, sticky=tk.W, padx=15, pady=5)
            
            var = tk.IntVar()
            entry = ttk.Spinbox(attr_frame, from_=1, to=10, width=5, textvariable=var)
            entry.grid(row=row, column=col+1, padx=(0, 15), pady=5, sticky=tk.W)
            entry.bind("<FocusOut>", self.update_derived_stats)
            
            self.attribute_vars[attr] = var
            self.attribute_entries[attr] = entry
            
            # Add label for metatype bonus - place in next column with spacing
            bonus_label = ttk.Label(attr_frame, text="", foreground="#4F9BFF")
            bonus_label.grid(row=row, column=col+2, padx=(0, 10), pady=5, sticky=tk.W)
            setattr(self, f"{attr.lower()}_bonus_label", bonus_label)
            
            # Add button to increase attribute with karma
            if attr not in ["Edge", "Essence"]:
                btn = ttk.Button(attr_frame, text="+", width=2, 
                                command=lambda a=attr: self.increase_attribute(a))
                btn.grid(row=row, column=col+3, padx=5, pady=5, sticky=tk.W)
        
        # Auto Roll button
        ttk.Button(attr_frame, text="Auto Roll Attributes", command=self.autoroll_attributes).grid(
            row=row+1, column=0, columnspan=12, pady=15
        )
    
    def trade_karma_for_nuyen(self):
        try:
            amount = int(tk.simpledialog.askinteger("Trade Karma", "How much Karma to trade? (1 Karma = 2000¥)", 
                                                   parent=self.root, minvalue=1, maxvalue=self.character.karma))
            if amount:
                if self.character.trade_karma_for_nuyen(amount):
                    self.update_all_fields()
                    messagebox.showinfo("Trade Complete", f"Traded {amount} Karma for {amount*2000}¥")
                else:
                    messagebox.showerror("Error", "Not enough Karma!")
        except TypeError:
            pass  # User canceled
    
    def increase_attribute(self, attribute):
        current_rating = self.character.base_attributes[attribute]
        karma_cost = (current_rating + 1) * 5
        
        if self.character.karma >= karma_cost:
            if self.character.increase_attribute(attribute):
                self.update_all_fields()
                messagebox.showinfo("Attribute Increased", 
                                   f"Increased {attribute} to {current_rating+1} for {karma_cost} Karma")
            else:
                messagebox.showerror("Error", "Failed to increase attribute!")
        else:
            messagebox.showerror("Error", f"Not enough Karma! Cost: {karma_cost} Karma")
    
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
        
        # Updated treeview with three columns: Skill, Specialization, Rank
        self.skill_tree = ttk.Treeview(skill_frame, columns=("Skill", "Specialization", "Rank"), show="headings", height=15)
        self.skill_tree.heading("Skill", text="Skill")
        self.skill_tree.heading("Specialization", text="Specialization")
        self.skill_tree.heading("Rank", text="Rank")
        self.skill_tree.column("Skill", width=150)
        self.skill_tree.column("Specialization", width=150)
        self.skill_tree.column("Rank", width=50)
        
        for skill in ShadowrunCharacter.SKILLS:
            self.skill_tree.insert("", "end", values=(skill, "", 0))
        
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
            
        item = self.skill_tree.item(selected[0])
        values = item["values"]
        skill = values[0]
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
            item = self.skill_tree.item(selected[0])
            values = item["values"]
            skill = values[0]
            rank = int(self.skill_rank_spin.get())
            spec = self.skill_spec_combo.get()
            
            self.character.skills[skill] = rank
            if spec and spec != "None":
                self.character.specializations[skill] = spec
            elif skill in self.character.specializations:
                del self.character.specializations[skill]
            
            self.skill_tree.item(selected[0], values=(skill, spec, rank))
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
                # Add karma cost if defined
                karma_cost = ShadowrunCharacter.QUALITY_EFFECTS.get(quality, {}).get("karma", 0)
                if self.character.karma >= karma_cost:
                    self.character.qualities.append(quality)
                    self.character.karma -= karma_cost
                    self.cur_quality_list.insert(tk.END, f"[+] {quality}")
                    self.update_derived_stats()
                else:
                    messagebox.showerror("Error", f"Not enough karma for {quality}! Cost: {karma_cost}")
    
    def add_neg_quality(self):
        selected = self.neg_quality_list.curselection()
        for index in selected:
            quality = self.neg_quality_list.get(index)
            if quality not in self.character.qualities:
                # Add karma gain if defined (negative cost)
                karma_gain = -ShadowrunCharacter.QUALITY_EFFECTS.get(quality, {}).get("karma", 0)
                self.character.qualities.append(quality)
                self.character.karma += karma_gain
                self.cur_quality_list.insert(tk.END, f"[-] {quality}")
                self.update_derived_stats()
    
    def remove_quality(self):
        selected = self.cur_quality_list.curselection()
        if selected:
            index = selected[0]
            quality_str = self.cur_quality_list.get(index)
            quality = quality_str[4:]  # Remove [+] or [-]
            if quality in self.character.qualities:
                # Reverse karma effect
                if quality_str.startswith("[+]"):
                    karma_cost = ShadowrunCharacter.QUALITY_EFFECTS.get(quality, {}).get("karma", 0)
                    self.character.karma += karma_cost
                else:
                    karma_gain = -ShadowrunCharacter.QUALITY_EFFECTS.get(quality, {}).get("karma", 0)
                    self.character.karma -= karma_gain
                    
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
        self.spell_tree.column("Drain", width=80)  # Increased width for better visibility
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
        notebook.add(foci_frame, text="Focus")
        
        # Foci list with description
        foci_list_frame = ttk.Frame(foci_frame)
        foci_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.foci_tree = ttk.Treeview(foci_list_frame, columns=("Type", "Force"), show="headings", height=10)
        self.foci_tree.heading("#0", text="Focus")
        self.foci_tree.column("#0", width=150)
        self.foci_tree.heading("Type", text="Type")
        self.foci_tree.column("Type", width=100)
        self.foci_tree.heading("Force", text="Force")
        self.foci_tree.column("Force", width=80)  # Increased width for better visibility
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
        
        # Age and Reputation on the same row
        age_rep_frame = ttk.Frame(tab)
        age_rep_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(age_rep_frame, text="Age:").pack(side=tk.LEFT, padx=5)
        self.age_spin = ttk.Spinbox(age_rep_frame, from_=0, to=200, width=5)
        self.age_spin.pack(side=tk.LEFT, padx=5)
        self.age_spin.set(self.character.age)
        self.age_spin.bind("<FocusOut>", self.update_derived_stats)
        
        ttk.Label(age_rep_frame, text="Reputation:").pack(side=tk.LEFT, padx=5)
        self.reputation_spin = ttk.Spinbox(age_rep_frame, from_=0, to=20, width=5)
        self.reputation_spin.pack(side=tk.LEFT, padx=5)
        self.reputation_spin.set(self.character.reputation)
        self.reputation_spin.bind("<FocusOut>", self.update_derived_stats)
        
        # Background text
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
        
        # Edge tracker
        edge_frame = ttk.LabelFrame(actions_frame, text="Edge")
        edge_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(edge_frame, text="Current Edge:").pack(side=tk.LEFT, padx=5)
        self.edge_label = ttk.Label(edge_frame, text="1", font=("Arial", 10, "bold"))
        self.edge_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(edge_frame, text="Reset Edge", command=self.reset_edge).pack(side=tk.LEFT, padx=5)
        
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
        
        # Edge actions
        edge_action_frame = ttk.Frame(dice_frame)
        edge_action_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(edge_action_frame, text="Edge Action:").pack(side=tk.LEFT, padx=5)
        self.edge_action_combo = ttk.Combobox(edge_action_frame, values=["None"] + list(ShadowrunCharacter.EDGE_ACTIONS.keys()), width=30)
        self.edge_action_combo.pack(side=tk.LEFT, padx=5)
        self.edge_action_combo.set("None")
        
        # Wild Die checkbox
        self.wild_die_var = tk.BooleanVar()
        wild_die_check = ttk.Checkbutton(edge_action_frame, text="Use Wild Die", 
                                        variable=self.wild_die_var)
        wild_die_check.pack(side=tk.LEFT, padx=10)
        
        # Damage penalty info
        damage_frame = ttk.Frame(dice_frame)
        damage_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.damage_penalty_label = ttk.Label(
            damage_frame, 
            text="Damage Penalty: 0", 
            foreground="#FF5252",  # Red color
            font=("Arial", 10)
        )
        self.damage_penalty_label.pack(anchor=tk.W)
        
        # Roll button
        btn_frame = ttk.Frame(dice_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Roll Dice", command=self.roll_dice).pack()
        
        # Results display - more visual representation
        result_frame = ttk.LabelFrame(dice_frame, text="Results")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for dice visualization
        self.dice_canvas = tk.Canvas(result_frame, bg="#333", height=100)
        self.dice_canvas.pack(fill=tk.X, padx=5, pady=5)
        
        # Results labels
        self.result_frame = ttk.Frame(result_frame)
        self.result_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.hits_label = ttk.Label(self.result_frame, text="Hits: 0", font=("Arial", 12, "bold"))
        self.hits_label.pack(side=tk.LEFT, padx=10)
        
        self.glitch_label = ttk.Label(self.result_frame, text="", font=("Arial", 12))
        self.glitch_label.pack(side=tk.LEFT, padx=10)
        
        self.success_label = ttk.Label(self.result_frame, text="", font=("Arial", 14, "bold"))
        self.success_label.pack(side=tk.LEFT, padx=10)
        
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
        
        # Update damage penalty label
        self.damage_penalty_label.config(
            text=f"Damage Penalty: {self.character.damage_penalty}"
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
                
            self.character.calculate_derived_stats()
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
                
            self.character.calculate_derived_stats()
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
        
        # Add weapons
        for weapon in self.character.gear["Weapons"]:
            options.append(f"Weapon: {weapon.get('name', '')}")
        
        self.dice_pool_combo["values"] = options
        if options:
            self.dice_pool_combo.set(options[0])
    
    def roll_dice(self):
        # Get selected edge action
        edge_action_name = self.edge_action_combo.get()
        edge_action = edge_action_name if edge_action_name != "None" else None
        
        # Get edge cost
        edge_cost = 0
        if edge_action:
            edge_cost = ShadowrunCharacter.EDGE_ACTIONS.get(edge_action_name, 0)
            
            # Check if character has enough edge
            if self.character.current_edge < edge_cost:
                # Instead of blocking, fall back to no edge action
                edge_action = None
                messagebox.showwarning("Not Enough Edge", 
                                      f"Not enough Edge points for {edge_action_name}! Rolling without edge action.")
        
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
            
        # Get wild die setting
        use_wild_die = self.wild_die_var.get()
        
        result = self.character.roll_dice(pool_size, edge_action, use_wild_die)
        
        # Clear previous results
        self.dice_canvas.delete("all")
        self.hits_label.config(text=f"Hits: {result['hits']}")
        
        # Set status text
        if result['critical_glitch']:
            self.glitch_label.config(text="CRITICAL GLITCH!", foreground="#F44336")
            self.success_label.config(text="FAILURE", foreground="#F44336")
        elif result['glitch']:
            self.glitch_label.config(text="GLITCH!", foreground="#FF9800")
            self.success_label.config(text="FAILURE", foreground="#F44336")
        else:
            self.glitch_label.config(text="")
            if result['hits'] > 0:
                self.success_label.config(text="SUCCESS!", foreground="#4CAF50")
            else:
                self.success_label.config(text="FAILURE", foreground="#F44336")
        
        # Visual dice representation
        dice_width = 30
        spacing = 5
        canvas_width = self.dice_canvas.winfo_width()
        start_x = (canvas_width - (dice_width * len(result['dice']) + spacing * (len(result['dice'])-1))) // 2
        
        # Draw wild die separately if used
        if result.get('wild_die'):
            wild_dice = result['wild_die']
            wild_x = 10
            for die in wild_dice:
                y = 40
                self.draw_die(self.dice_canvas, wild_x, y, dice_width, die, True)
                wild_x += dice_width + spacing
        
        # Draw regular dice
        for i, die in enumerate(result['dice']):
            x = start_x + i * (dice_width + spacing)
            y = 40
            
            # Draw die
            self.draw_die(self.dice_canvas, x, y, dice_width, die)
    
    def draw_die(self, canvas, x, y, size, value, is_wild=False):
        """Draw a single die with visual indicators"""
        # Draw die background with special color for wild die
        fill_color = "#4F9BFF" if is_wild else "#444"
        canvas.create_rectangle(
            x, y, x+size, y+size,
            fill=fill_color, outline="#666"
        )
        
        # Draw die value
        canvas.create_text(
            x + size/2, y + size/2,
            text=str(value),
            fill="white",
            font=("Arial", 14, "bold")
        )
        
        # Draw hit indicator (5-6)
        if value >= 5:
            canvas.create_oval(
                x+5, y+5, x+10, y+10,
                fill="#4CAF50", outline=""
            )
        # Draw glitch indicator (1)
        elif value == 1:
            canvas.create_oval(
                x+size-10, y+5, x+size-5, y+10,
                fill="#F44336", outline=""
            )
    
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
            # Update gear display
            for item in self.medkits_tree.get_children():
                self.medkits_tree.delete(item)
            for item in self.character.gear["Medkits"]:
                attrs = []
                for key, value in item.items():
                    if key not in ["name", "description"]:
                        attrs.append(f"{key}: {value}")
                details = "; ".join(attrs)
                self.medkits_tree.insert("", "end", text=item.get("name", "Unknown"), values=(details,))
        else:
            messagebox.showwarning("No Medkit", "No medkit found in your gear!")
    
    def rest(self):
        self.character.rest()
        self.draw_condition_monitors()
        messagebox.showinfo("Rest", "Character rested. Stun damage reduced by 1.")
    
    def reset_edge(self):
        self.character.reset_edge()
        self.edge_label.config(text=str(self.character.current_edge))
        messagebox.showinfo("Edge Reset", "Edge points reset to maximum!")
    
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
        self.age_spin.delete(0, tk.END)
        self.age_spin.insert(0, str(self.character.age))
        self.reputation_spin.delete(0, tk.END)
        self.reputation_spin.insert(0, str(self.character.reputation))
        
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
            self.skill_tree.insert("", "end", values=(skill, spec, rank))
        
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
                # Format details for display - show attributes only
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
                contact.get("loyalty", ""),
                contact.get("connection", "")
            ))
        
        # Background
        self.background_text.delete(1.0, tk.END)
        self.background_text.insert(tk.END, self.character.background)
        
        # Update derived stats display
        self.update_derived_stats()
        
        # Update dice pool options
        self.update_dice_pool_options()
        
        # Update edge display
        self.edge_label.config(text=str(self.character.current_edge))
        
        # Update damage penalty display
        self.damage_penalty_label.config(text=f"Damage Penalty: {self.character.damage_penalty}")
    
    def update_derived_stats(self, event=None):
        # Save current values to character object
        self.character.name = self.name_entry.get()
        self.character.metatype = self.metatype_combo.get()
        self.character.role = self.role_combo.get()
        self.character.magic_type = self.magic_combo.get()
        self.character.tradition = self.tradition_combo.get()
        self.character.initiation_grade = int(self.init_grade_spin.get() or "0")
        self.character.lifestyle = self.lifestyle_combo.get()
        self.character.karma = int(self.karma_spin.get() or "50")
        self.character.nuyen = int(self.nuyen_entry.get() or "0")
        self.character.background = self.background_text.get(1.0, tk.END).strip()
        self.character.age = int(self.age_spin.get() or "25")
        self.character.reputation = int(self.reputation_spin.get() or "0")
        
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
        
        # Update edge display
        self.edge_label.config(text=str(self.character.current_edge))
    
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
