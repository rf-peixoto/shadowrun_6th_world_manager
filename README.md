![Shadowrun 6th World Logo](https://www.shadowrunsixthworld.com/wp-content/themes/shadowrun/dist/images/shadowrun-logo-totem_bc47c041.png)

# Shadowrun 6E Character Manager

A standalone Python/Tkinter application for creating, editing, and managing Shadowrun 6th World character sheets.

## Features

- **Basic Info**  
  - Name, Metatype, Role, Background, Lifestyle (auto‑sets starting Nuyen)  
  - Karma tracker  

- **Attributes**  
  - All 12 core attributes + Edge & Essence  
  - Metatype minimums & role bonuses enforced automatically  
  - “Auto Roll” to randomly generate base attributes within metatype limits  

- **Skills**  
  - Full skill list with ranks  
  - Drop‑down specializations per skill  
  - Live update of skill tree  

- **Qualities**  
  - Positive & Negative qualities selectable from book lists  
  - Automatic attribute adjustments & Karma cost/gain  

- **Gear**  
  - Categorized tabs (Weapons, Armor, Cyberware, Bioware, Magic Items, Electronics, Other)  
  - Add/Edit/Remove items with full name, description, and custom stats  
  - Persisted descriptions in the tree view  

- **Magic & Resonance**  
  - Spells, Powers, Foci each with name + detailed description  
  - Add/Edit/Remove via modal dialogs  

- **Contacts**  
  - Type & Loyalty drop‑downs based on book options  
  - Connection level and freeform notes  
  - View full contact details in a read‑only pop‑up  

- **Background**  
  - Freeform text area for history, notes, Karma logs, etc.  

- **Combat Statistics**  
  - Clickable Physical & Stun condition monitors  
  - Automatic box calculation (Body/Willpower → boxes + High Pain Tolerance bonus)  
  - Color‑coded damage status (Healthy, Light, Moderate, Serious)  

- **Dice Roller**  
  - Predefined roll types (physical attack, hacking, stealth, etc.)  
  - Dynamic dice‑pool selector from attributes/skills  
  - Edge re‑roll support  
  - Glitch & Critical Glitch detection  
  - Colorized result output  

- **Persistence**  
  - Save/Load character as JSON (`*.sr6`)  
  - All data—including gear descriptions, qualities, spells, contacts—fully preserved  

## Installation

1. Ensure you have **Python 3.7+** installed.
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python shadowrunv2.py
```

- Click New Character to start fresh.
- Use Save Character / Load Character to manage your .sr6 files.
- Navigate the tabs to fill in every section of your sheet.
- Double‑click items, spells, or contacts to view full descriptions.
- Click on the condition monitors to apply or heal damage.
- Use the Dice Roller tab for in‑game tests with glitch detection.
