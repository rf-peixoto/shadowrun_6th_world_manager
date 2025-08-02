#!/usr/bin/env python3
import os
import sys
import json
import random
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Core attributes only—EDG, MAG, RES handled separately via priorities
CORE_ATTRIBUTES = ["BOD", "AGI", "REA", "STR", "WIL", "LOG", "INT", "CHA"]

METATYPE_LIMITS = {
    "Human":    {attr: (1, 6) for attr in CORE_ATTRIBUTES},
    "Elf":      {**{attr: (1, 6) for attr in CORE_ATTRIBUTES}, **{"CHA": (1, 7)}},
    "Dwarf":    {**{attr: (1, 6) for attr in CORE_ATTRIBUTES}, **{"WIL": (1, 7)}},
    "Ork":      {**{attr: (1, 6) for attr in CORE_ATTRIBUTES}, **{"STR": (1, 7)}},
    "Troll":    {**{attr: (1, 6) for attr in CORE_ATTRIBUTES}, **{"BOD": (1, 8), "STR": (1, 8)}},
}

PRIORITY_TABLES = {
    "Metatype": {
        "A": {"type": "Human", "EDG": 1},
        "B": {"type": "Elf",     "EDG": 2},
        "C": {"type": "Dwarf",   "EDG": 2},
        "D": {"type": "Ork",     "EDG": 3},
        "E": {"type": "Troll",   "EDG": 4},
    },
    "Attributes": {
        "A": 24,
        "B": 20,
        "C": 16,
        "D": 14,
        "E": 12,
    },
    "Magic/Resonance": {
        "A": {"type": "Adept",    "rating": 6},
        "B": {"type": "Magician", "rating": 4},
        "C": {"type": "Technomancer", "rating": 4},
        "D": {"type": "None",     "rating": 0},
        "E": {"type": "None",     "rating": 0},
    },
    "Skills": {
        "A": {"points": 46, "skill_group": 5},
        "B": {"points": 36, "skill_group": 4},
        "C": {"points": 30, "skill_group": 3},
        "D": {"points": 24, "skill_group": 2},
        "E": {"points": 18, "skill_group": 1},
    },
    "Resources": {
        "A": 450000,
        "B": 270000,
        "C": 150000,
        "D": 50000,
        "E": 6000,
    }
}

PRIORITY_DESCRIPTIONS = {
    "Metatype": {
        "A": "Human: +0 Edge",
        "B": "Elf: +1 Edge",
        "C": "Dwarf: +1 Edge",
        "D": "Ork: +2 Edge",
        "E": "Troll: +3 Edge",
    },
    "Attributes": {
        "A": "24 points to distribute among BOD, AGI, REA, STR, WIL, LOG, INT, CHA",
        "B": "20 points to distribute",
        "C": "16 points to distribute",
        "D": "14 points to distribute",
        "E": "12 points to distribute",
    },
    "Magic/Resonance": {
        "A": "Adept: Rating 6",
        "B": "Magician (Hermetic/Shamanic): Rating 4",
        "C": "Technomancer (Machine/Digital): Rating 4",
        "D": "None",
        "E": "None",
    },
    "Skills": {
        "A": "46 skill points, 5 groups",
        "B": "36 points, 4 groups",
        "C": "30 points, 3 groups",
        "D": "24 points, 2 groups",
        "E": "18 points, 1 group",
    },
    "Resources": {
        "A": "450,000¥",
        "B": "270,000¥",
        "C": "150,000¥",
        "D": "50,000¥",
        "E": "6,000¥",
    }
}

TRADITIONS = {
    "Mundane": ["None"],
    "Magician": ["Hermetic", "Shamanic"],
    "Mystic Adept": ["Eastern", "Nature"],
    "Technomancer": ["Machine", "Digital"],
    "Adept": ["Warrior", "Healer"],
    "Aspected Magician": ["Sorcery", "Conjuring"]
}

MENTORS = {
    "None": ["None"],
    "Hermetic": ["Master of the Five Elements", "The Scholar"],
    "Shamanic": ["Raven", "Bear"],
    "Eastern": ["Dragon", "Tiger"],
    "Nature": ["Green Man", "Stormcaller"],
    "Machine": ["The System", "The Ghost"],
    "Digital": ["The Weaver", "The Pattern"],
    "Warrior": ["The Champion", "The Strategist"],
    "Healer": ["The Lifegiver", "The Mender"],
    "Sorcery": ["The Artisan", "The Destroyer"],
    "Conjuring": ["The Summoner", "The Binder"]
}

SKILLS = [
    "Athletics", "Biotech", "Close Combat", "Conjuring", "Cracking", "Electronics", "Enchanting",
    "Engineering", "Firearms", "Influence", "Outdoors", "Perception", "Piloting", "Sorcery",
    "Stealth", "Tasking", "Exotic Weapons", "Gunnery", "Intimidation", "Leadership", "Negotiation",
    "Animal Handling", "Arcana", "Armorer", "Artisan", "Disguise", "Diving", "Escape Artist",
    "First Aid", "Forgery", "Gambling", "Hacking", "Hardware", "Locksmith", "Medicine", "Navigation",
    "Performance", "Running", "Survival", "Swimming", "Tracking", "Vehicle"
]

QUALITIES = {
    "Positive": {
        "Adept": {"karma": 12, "attribute": "MAG", "effect": "+1"},
        "Ambidextrous": {"karma": 8},
        "Analytical Mind": {"karma": 8},
        "Astral Chameleon": {"karma": 10},
        "Blandness": {"karma": 8},
        "Catlike": {"karma": 10, "attribute": "AGI", "effect": "+1"},
        "Double-Jointed": {"karma": 8},
        "Exceptional Attribute": {"karma": 14, "attribute": None, "effect": "+1"},
        "First Impression": {"karma": 12},
        "Guts": {"karma": 10},
        "High Pain Tolerance": {"karma": 10},
        "Home Ground": {"karma": 12},
        "Human Looking": {"karma": 8},
        "Juryrigger": {"karma": 10},
        "Lucky": {"karma": 12, "attribute": "EDG", "effect": "+1"},
        "Magician": {"karma": 15, "attribute": "MAG", "effect": "+1"},
        "Mentor Spirit": {"karma": 5},
        "Natural Athlete": {"karma": 8, "attribute": "STR", "effect": "+1"},
        "Natural Hardening": {"karma": 10},
        "Photographic Memory": {"karma": 6, "attribute": "LOG", "effect": "+1"},
        "Quick Healer": {"karma": 6},
        "Resistance to Pathogens": {"karma": 8},
        "Resistance to Toxins": {"karma": 8},
        "School of Hard Knocks": {"karma": 8},
        "Sharpshooter": {"karma": 12},
        "Technomancer": {"karma": 5, "attribute": "RES", "effect": "+1"},
        "Toughness": {"karma": 10, "attribute": "BOD", "effect": "+1"},
        "Will to Live": {"karma": 8}
    },
    "Negative": {
        "Addiction": {"karma": -5},
        "Allergy": {"karma": -10},
        "Astral Beacon": {"karma": -12},
        "Bad Luck": {"karma": -12, "attribute": "EDG", "effect": "-1"},
        "Bad Rep": {"karma": -6},
        "Code of Honor": {"karma": -10},
        "Dependents": {"karma": -8},
        "Distinctive Style": {"karma": -5},
        "Elf Poser": {"karma": -8},
        "Gremlins": {"karma": -8},
        "Low Pain Tolerance": {"karma": -10},
        "Ork Poser": {"karma": -8},
        "Pacifist": {"karma": -10},
        "Phobia": {"karma": -8},
        "Reckless Spending": {"karma": -5},
        "Social Stigma": {"karma": -8},
        "Spirit Bane": {"karma": -10},
        "Simsense Vertigo": {"karma": -10},
        "Weak Immune System": {"karma": -10}
    }
}

LIFESTYLES = {
    "Street":  {"cost": 0,      "description": "Survive by any means necessary"},
    "Squatter":{"cost": 300,    "description": "Abandoned buildings, minimal services"},
    "Low":     {"cost": 800,    "description": "Basic comforts, shared spaces"},
    "Middle":  {"cost": 2500,   "description": "Decent apartment, modest amenities"},
    "High":    {"cost": 9000,   "description": "Luxury condo, good security"},
    "Luxury":  {"cost": 100000, "description": "Penthouse with top-tier security"}
}

MEDKITS = {
    "Rating 1": {"cost": 200,  "dice": 4},
    "Rating 3": {"cost": 600,  "dice": 8},
    "Rating 6": {"cost": 1200, "dice": 12}
}


class ShadowrunCharacter:
    def __init__(self):
        self.name = ""
        self.metatype = ""
        self.role = ""
        self.tradition = None
        self.mentor = None
        self.lifestyle = ""
        self.nuyen = 0
        self.karma = 25
        # Edge will be set by Metatype priority
        self.edge = {"current": 1, "max": 1, "burnt": 0}
        # Initialize core + Edge/Magic/Resonance
        self.attributes = {
            "BOD": 1, "AGI": 1, "REA": 1, "STR": 1,
            "WIL": 1, "LOG": 1, "INT": 1, "CHA": 1,
            "EDG": 1, "MAG": 0, "RES": 0
        }
        self.skills = {}
        self.qualities = []
        self.condition = {"physical": 0, "stun": 0, "overflow": 0}
        self.magic_resonance = {"type": "Mundane", "rating": 0}
        self.medkits = []
        self.priorities = {
            "Metatype": "", "Attributes": "",
            "Magic/Resonance": "", "Skills": "", "Resources": ""
        }

    def calculate_condition_monitors(self):
        phys = 8 + (self.attributes["BOD"] + 1) // 2
        stun = 8 + (self.attributes["WIL"] + 1) // 2
        overflow = self.attributes["BOD"]
        return phys, stun, overflow

    def roll_dice(self, pool, spend_edge=False, wild_die=False):
        # Edge spending
        if spend_edge and self.edge["current"] > 0:
            pool += self.edge["current"]
            self.edge["current"] = 0

        rolls = [random.randint(1, 6) for _ in range(pool)]
        if wild_die:
            w = random.randint(1, 6)
            extended = []
            while w == 6:
                extended.append(6)
                w = random.randint(1, 6)
            rolls += extended + [w]

        successes = sum(1 for r in rolls if r >= 5)
        ones = rolls.count(1)
        glitch = ones > len(rolls) / 2
        critical = glitch and successes == 0
        return {
            "rolls": rolls,
            "successes": successes,
            "glitch": glitch,
            "critical": critical
        }

    def take_damage(self, damage_type, amount):
        if damage_type == "physical":
            self.condition["physical"] += amount
            phys_max, _, _ = self.calculate_condition_monitors()
            if self.condition["physical"] > phys_max:
                overflow = self.condition["physical"] - phys_max
                self.condition["overflow"] = min(overflow, self.attributes["BOD"])
        elif damage_type == "stun":
            self.condition["stun"] += amount

    def spend_edge(self):
        if self.edge["current"] > 0:
            self.edge["current"] -= 1
            return True
        return False

    def burn_edge(self):
        if self.edge["current"] > 0:
            self.edge["burnt"] += self.edge["current"]
            self.edge["current"] = 0
            return True
        return False

    def apply_quality_effects(self, quality_name):
        if quality_name in QUALITIES["Positive"]:
            qual = QUALITIES["Positive"][quality_name]
        else:
            qual = QUALITIES["Negative"][quality_name]
        attr = qual.get("attribute")
        eff = qual.get("effect")
        if attr and eff:
            change = int(eff)
            self.attributes[attr] += change

    def add_quality(self, quality_name, qtype):
        pool = QUALITIES[qtype]
        if quality_name not in pool:
            return False
        cost = pool[quality_name]["karma"]
        if qtype == "Positive" and self.karma < cost:
            return False
        self.qualities.append({"name": quality_name, "type": qtype})
        self.karma -= cost
        self.apply_quality_effects(quality_name)
        return True

    def remove_quality(self, quality_name):
        for q in self.qualities:
            if q["name"] == quality_name:
                data = QUALITIES[q["type"]][quality_name]
                self.karma += data["karma"] if q["type"] == "Positive" else -data["karma"]
                attr = data.get("attribute")
                eff = data.get("effect")
                if attr and eff:
                    self.attributes[attr] -= int(eff)
                self.qualities.remove(q)
                return True
        return False

    def buy_medkit(self, medkit_type):
        m = MEDKITS.get(medkit_type)
        if not m or self.nuyen < m["cost"]:
            return False
        self.nuyen -= m["cost"]
        self.medkits.append(medkit_type)
        return True

    def use_medkit(self, medkit_type):
        if medkit_type not in self.medkits:
            return 0
        dice = MEDKITS[medkit_type]["dice"]
        res = self.roll_dice(dice)
        healed = res["successes"]
        self.condition["physical"] = max(0, self.condition["physical"] - healed)
        self.medkits.remove(medkit_type)
        return healed

    def save_character(self, filename):
        data = self.__dict__.copy()
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def load_character(self, filename):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.__dict__.update(data)
            return True
        except:
            return False

    def roll_initiative(self):
        base = self.attributes["REA"] + self.attributes["INT"]
        res = self.roll_dice(1, wild_die=True)
        return base + res["successes"]  # wild die successes count


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(Fore.CYAN + Style.BRIGHT + "="*40)
    print(Fore.CYAN + Style.BRIGHT + "   Shadowrun 6E Character Manager   ")
    print(Fore.CYAN + Style.BRIGHT + "="*40)


def prompt(msg="> "):
    return input(Fore.YELLOW + msg)


def priority_selection(char):
    clear_screen()
    print_banner()
    print(Fore.MAGENTA + "\n=== PRIORITY SELECTION ===")
    available = ["A", "B", "C", "D", "E"]
    for category in char.priorities:
        while True:
            print(f"\n{category} (choose {', '.join(available)}):")
            for p in available:
                print(f"  {p}. {PRIORITY_DESCRIPTIONS[category][p]}")
            choice = prompt(f"{category} priority: ").upper()
            if choice in available:
                char.priorities[category] = choice
                available.remove(choice)
                break
            else:
                print(Fore.RED + "Invalid choice, try again.")


def create_character():
    char = ShadowrunCharacter()
    clear_screen(); print_banner()
    print(Fore.CYAN + "\nEnter your character's name: ")
    char.name = prompt()
    priority_selection(char)

    # Metatype & Edge
    m = PRIORITY_TABLES["Metatype"][char.priorities["Metatype"]]
    char.metatype = m["type"]
    char.edge["max"] = char.edge["current"] = m["EDG"]

    # Attributes
    clear_screen(); print_banner()
    pts = PRIORITY_TABLES["Attributes"][char.priorities["Attributes"]]
    print(Fore.CYAN + f"\nDistribute {pts} points among core attributes: ")
    for attr in CORE_ATTRIBUTES:
        while True:
            val = prompt(f"Remaining points: {pts} | {attr} (1–6): ").strip()
            if not val.isdigit(): 
                print(Fore.RED + "Enter a number.")
                continue
            v = int(val)
            if 1 <= v <= 6 and v <= pts:
                char.attributes[attr] = v
                pts -= v
                break
            else:
                print(Fore.RED + "Out of range or not enough points.")
    # Magic/Resonance
    mres = PRIORITY_TABLES["Magic/Resonance"][char.priorities["Magic/Resonance"]]
    char.magic_resonance = {"type": mres["type"], "rating": mres["rating"]}
    char.attributes["MAG"] = mres["rating"]
    char.attributes["RES"] = mres["rating"]

    # Skills
    clear_screen(); print_banner()
    sp = PRIORITY_TABLES["Skills"][char.priorities["Skills"]]["points"]
    print(Fore.CYAN + f"\nAllocate {sp} skill points:")
    while sp > 0:
        print(f"Remaining: {sp}")
        print("Available skills:", ", ".join(SKILLS))
        sk = prompt("Skill name (or 'done'): ").title()
        if sk == "Done":
            break
        if sk not in SKILLS:
            print(Fore.RED + "Invalid skill.")
            continue
        val = prompt(f"Rating for {sk}: ").strip()
        if not val.isdigit():
            print(Fore.RED + "Enter a number: ")
            continue
        r = int(val)
        if 1 <= r <= sp:
            char.skills[sk] = r
            sp -= r
        else:
            print(Fore.RED + "Too high or not enough points.")

    # Resources / Nuyen
    char.nuyen = PRIORITY_TABLES["Resources"][char.priorities["Resources"]]

    # Role & Lifestyle
    clear_screen(); print_banner()
    char.role = prompt("Character Role (Street Samurai, Decker, Rigger, Face, Mage, Shaman, Adept, Technomancer): ")
    print(Fore.CYAN + "\nSelect Lifestyle:")
    for name, info in LIFESTYLES.items():
        print(f"  {name}: {info['description']} ({info['cost']}¥)")
    while True:
        ls = prompt("Lifestyle: ").title()
        if ls in LIFESTYLES:
            char.lifestyle = ls
            char.nuyen -= LIFESTYLES[ls]["cost"]
            break
        else:
            print(Fore.RED + "Invalid choice.")

    return char


def display_character(char):
    clear_screen(); print_banner()
    phys_max, stun_max, ov = char.calculate_condition_monitors()
    print(Fore.YELLOW + f"Name: {char.name} | Metatype: {char.metatype} | Role: {char.role}")
    print(f"Tradition: {char.tradition or 'None'} | Mentor: {char.mentor or 'None'}")
    print(f"Lifestyle: {char.lifestyle} | Nuyen: {char.nuyen}¥ | Karma: {char.karma}")
    print(f"Edge: {char.edge['current']}/{char.edge['max']} | Burnt: {char.edge['burnt']}")
    print(Fore.CYAN + "\nAttributes:")
    for attr, val in char.attributes.items():
        mn, mx = METATYPE_LIMITS[char.metatype].get(attr, (None, None))
        print(f"  {attr}: {val}" + (f" (Min {mn}, Max {mx})" if mn else ""))

    print(Fore.CYAN + "\nCondition Monitors:")
    print(f"  Physical: [{'■'*char.condition['physical']}{'□'*(phys_max-char.condition['physical'])}] {char.condition['physical']}/{phys_max}")
    print(f"  Stun:     [{'■'*char.condition['stun']}{'□'*(stun_max-char.condition['stun'])}] {char.condition['stun']}/{stun_max}")
    print(f"  Overflow: {char.condition['overflow']}/{ov}")

    if char.magic_resonance["rating"] > 0:
        mr = char.magic_resonance
        print(Fore.CYAN + f"\nMagic/Resonance: {mr['type']} (Rating {mr['rating']})")

    print(Fore.CYAN + "\nSkills:")
    for sk, r in char.skills.items():
        print(f"  {sk}: {r}")

    print(Fore.CYAN + "\nQualities:")
    for q in char.qualities:
        print(f"  {q['name']} ({q['type']})")

    if char.medkits:
        print(Fore.CYAN + "\nMedkits:")
        for m in char.medkits:
            print(f"  {m}")


def manage_skills(char):
    while True:
        clear_screen(); print_banner()
        print(Fore.CYAN + "\n=== MANAGE SKILLS ===")
        print("1) Add / Increase Skill")
        print("2) Remove / Decrease Skill")
        print("0) Back")
        c = prompt("Choice: ")
        if c == "0": break
        if c == "1":
            sk = prompt("Skill name").title()
            if sk not in SKILLS:
                print(Fore.RED + "No such skill."); prompt("[Enter to continue]"); continue
            r = prompt("New rating").strip()
            if not r.isdigit():
                print(Fore.RED + "Invalid."); prompt("[Enter to continue]"); continue
            char.skills[sk] = int(r)
            print(Fore.GREEN + f"{sk} set to {r}."); prompt("[Enter to continue]")
        elif c == "2":
            sk = prompt("Skill to remove").title()
            if sk in char.skills:
                del char.skills[sk]
                print(Fore.GREEN + f"{sk} removed.")
            else:
                print(Fore.RED + "Not found.")
            prompt("[Enter to continue]")


def manage_qualities(char):
    while True:
        clear_screen(); print_banner()
        print(Fore.CYAN + "\n=== MANAGE QUALITIES ===")
        print("1) Add Positive")
        print("2) Add Negative")
        print("3) Remove Quality")
        print("0) Back")
        c = prompt("Choice: ")
        if c == "0": break
        if c in ("1", "2"):
            pt = "Positive" if c=="1" else "Negative"
            for name, dat in QUALITIES[pt].items():
                print(f"  {name} ({dat['karma']} Karma)")
            qn = prompt("Quality name: ").title()
            if char.add_quality(qn, pt):
                print(Fore.GREEN + f"Added {qn}")
            else:
                print(Fore.RED + "Failed.")
            prompt("[Enter to continue]")
        elif c == "3":
            for i,q in enumerate(char.qualities,1):
                print(f"  {i}. {q['name']} ({q['type']})")
            sel = prompt("Number").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(char.qualities):
                qn = char.qualities[int(sel)-1]["name"]
                if char.remove_quality(qn):
                    print(Fore.GREEN + f"Removed {qn}")
                else:
                    print(Fore.RED + "Failed.")
            else:
                print(Fore.RED + "Invalid selection.")
            prompt("[Enter to continue]")


def manage_edge(char):
    clear_screen(); print_banner()
    print(Fore.CYAN + "\n=== EDGE STATUS ===")
    print(f"Current Edge: {char.edge['current']} / {char.edge['max']}")
    print(f"Burnt Edge:   {char.edge['burnt']}")
    prompt("Enter to return")


def manage_medkits(char):
    while True:
        clear_screen(); print_banner()
        print(Fore.CYAN + "\n=== MEDKIT MENU ===")
        print("1) Buy Medkit")
        print("2) Use Medkit")
        print("0) Back")
        c = prompt("Choice: ")
        if c == "0": break
        if c == "1":
            for name, dat in MEDKITS.items():
                print(f"  {name}: {dat['dice']}d6 for {dat['cost']}¥")
            m = prompt("Which?").title()
            if char.buy_medkit(m):
                print(Fore.GREEN + f"Bought {m}")
            else:
                print(Fore.RED + "Can't buy.")
            prompt("[Enter to continue]")
        elif c == "2":
            if not char.medkits:
                print(Fore.YELLOW + "None available.")
                prompt("[Enter to continue]"); continue
            for i,m in enumerate(char.medkits,1):
                print(f"  {i}. {m}")
            sel = prompt("Number").strip()
            if sel.isdigit() and 1 <= int(sel) <= len(char.medkits):
                m = char.medkits[int(sel)-1]
                amt = char.use_medkit(m)
                print(Fore.GREEN + f"Healed {amt} physical damage.")
            else:
                print(Fore.RED + "Invalid.")
            prompt("[Enter to continue]")


def combat_actions(char):
    while True:
        clear_screen(); print_banner()
        print(Fore.CYAN + "\n=== COMBAT ACTIONS ===")
        print("1) Roll Initiative")
        print("2) Take Damage")
        print("3) Push the Limit (Spend Edge)")
        print("4) Blitz (Burn Edge + Wild Die)")
        print("0) Back")
        c = prompt("Choice: ")
        if c == "0": break
        if c == "1":
            initv = char.roll_initiative()
            print(Fore.GREEN + f"Initiative: {initv}")
            prompt("[Enter to continue]")
        elif c == "2":
            dt = prompt("Type (physical/stun)").lower()
            amt = prompt("Amount: ").strip()
            if not amt.isdigit():
                print(Fore.RED + "Invalid."); prompt("[Enter to continue]"); continue
            char.take_damage(dt, int(amt))
            phys, stun, ov = char.calculate_condition_monitors()
            print(Fore.YELLOW + f"Phys {char.condition['physical']}/{phys}, Stun {char.condition['stun']}/{stun}, Overflow {char.condition['overflow']}/{ov}")
            prompt("[Enter to continue]")
        elif c in ("3", "4"):
            pool = prompt("Base dice pool: ").strip()
            if not pool.isdigit():
                print(Fore.RED + "Invalid."); prompt("[Enter to continue]"); continue
            pool = int(pool)
            spend = (c == "3")
            burn = (c == "4")
            res = char.roll_dice(pool, spend_edge=spend, wild_die=burn)
            # visualize
            colored = []
            for d in res["rolls"]:
                if d in [5, 6]:
                    colored.append(Fore.GREEN + str(d))
                elif d in [2, 3, 4]:
                    colored.append(Fore.WHITE + str(d))
                else:
                    colored.append(Fore.RED + str(d))
            print("Rolls:", " ".join(colored))
            if res["critical"]:
                print(Back.RED + Fore.WHITE + "CRITICAL GLITCH!")
            elif res["glitch"]:
                print(Back.YELLOW + Fore.BLACK + "GLITCH!")
            print(Fore.CYAN + f"Successes: {res['successes']}")
            prompt("[Enter to continue]")


def character_menu(char):
    while True:
        clear_screen(); print_banner()
        print(Fore.CYAN + "\n=== MAIN MENU ===")
        print("1) View Character")
        print("2) Edit Attributes")
        print("3) Manage Skills")
        print("4) Manage Qualities")
        print("5) View Edge")
        print("6) Medkits")
        print("7) Dice Roller")
        print("8) Combat Actions")
        print("9) Save Character")
        print("0) Exit")
        c = prompt("Choice: ")
        if c == "0":
            break
        elif c == "1":
            display_character(char)
            prompt("[Enter to continue]")
        elif c == "2":
            # Editing raw attributes—be cautious!
            for a in CORE_ATTRIBUTES:
                mn, mx = METATYPE_LIMITS[char.metatype][a]
                v = prompt(f"{a} ({char.attributes[a]}) new: ").strip()
                if v.isdigit() and mn <= int(v) <= mx:
                    char.attributes[a] = int(v)
            print(Fore.GREEN + "Attributes updated.")
            prompt("[Enter to continue]")
        elif c == "3":
            manage_skills(char)
        elif c == "4":
            manage_qualities(char)
        elif c == "5":
            manage_edge(char)
        elif c == "6":
            manage_medkits(char)
        elif c == "7":
            # Quick roller
            pool = prompt("Dice pool: ").strip()
            if not pool.isdigit():
                print(Fore.RED + "Invalid."); prompt("[Enter to continue]"); continue
            res = char.roll_dice(int(pool))
            colored = [
                Fore.GREEN + str(d) if d >= 5
                else Fore.RED + str(d) if d == 1
                else Fore.WHITE + str(d)
                for d in res["rolls"]
            ]            
            print("Rolls:", " ".join(colored))
            if res["critical"]:
                print(Back.RED + Fore.WHITE + "CRITICAL GLITCH!")
            elif res["glitch"]:
                print(Back.YELLOW + Fore.BLACK + "GLITCH!")
            print(Fore.CYAN + f"Successes: {res['successes']}")
            prompt("[Enter to continue]")
        elif c == "8":
            combat_actions(char)
        elif c == "9":
            fn = prompt("Filename to save: ").strip()
            char.save_character(fn)
            print(Fore.GREEN + f"Saved to {fn}.")
            prompt("[Enter to continue]")


def main():
    char = None
    while True:
        clear_screen(); print_banner()
        print("1) New Character")
        print("2) Load Character")
        print("0) Quit")
        c = prompt("Choice: ")
        if c == "0":
            sys.exit(0)
        elif c == "1":
            char = create_character()
            character_menu(char)
        elif c == "2":
            fn = prompt("Filename to load: ").strip()
            ch = ShadowrunCharacter()
            if ch.load_character(fn):
                char = ch
                print(Fore.GREEN + "Loaded.")
                prompt("[Enter to continue]")
                character_menu(char)
            else:
                print(Fore.RED + "Load failed.")
                prompt("[Enter to continue]")


if __name__ == "__main__":
    main()
