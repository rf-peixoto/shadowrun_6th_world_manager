import json
import os
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox,
    QPushButton, QGroupBox, QListWidget, QListWidgetItem, QAbstractItemView,
    QMessageBox, QStyledItemDelegate, QStyle
)
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt, Signal

# Define core data structures
METATYPES = ["Human", "Elf", "Dwarf", "Ork", "Troll"]
ATTRIBUTES = ["Body", "Agility", "Reaction", "Strength", "Willpower", "Logic", "Intuition", "Charisma"]
SKILLS = [
    "Athletics", "Biotech", "Close Combat", "Con", "Cracking", "Electronics", "Engineering",
    "Firearms", "Influence", "Outdoors", "Perception", "Piloting", "Stealth", "Sorcery", "Tasking"
]
QUALITIES = {
    "Positive": [
        "Aptitude", "Blandness", "Catlike", "Double Jointed", "Guts", "High Pain Tolerance",
        "Home Ground", "Lucky", "Magical Resistance", "Photographic Memory", "Quick Healer",
        "Spirit Affinity", "Toughness", "Will to Live"
    ],
    "Negative": [
        "Allergy", "Astral Beacon", "Bad Luck", "Code of Honor", "Dependents", "Glass Jaw",
        "Incompetent", "Low Pain Tolerance", "Magic Sense", "Prejudiced", "Scorched", "SINner",
        "Slow Healer", "Uncouth"
    ]
}
POWERS = [
    "Attribute Boost", "Combat Sense", "Critical Strike", "Elemental Strike", "Enhanced Accuracy",
    "Improved Ability", "Improved Physical Attribute", "Improved Reflexes", "Improved Sense",
    "Killing Hands", "Mystic Armor", "Pain Resistance", "Penetrating Strike", "Traceless Walk"
]
FOCI = ["Weapon", "Spellcasting", "Power", "Qi", "Alchemy"]
LIFESTYLES = ["Street", "Squatter", "Low", "Middle", "High", "Luxury"]
PRIORITY_LEVELS = ["A", "B", "C", "D", "E"]

# Dark theme palette
DARK_PALETTE = QPalette()
DARK_PALETTE.setColor(QPalette.Window, QColor(45, 45, 55))
DARK_PALETTE.setColor(QPalette.WindowText, QColor(220, 220, 220))
DARK_PALETTE.setColor(QPalette.Base, QColor(35, 35, 45))
DARK_PALETTE.setColor(QPalette.AlternateBase, QColor(45, 45, 55))
DARK_PALETTE.setColor(QPalette.ToolTipBase, QColor(60, 60, 80))
DARK_PALETTE.setColor(QPalette.ToolTipText, Qt.white)
DARK_PALETTE.setColor(QPalette.Text, QColor(220, 220, 220))
DARK_PALETTE.setColor(QPalette.Button, QColor(65, 65, 80))
DARK_PALETTE.setColor(QPalette.ButtonText, QColor(220, 220, 220))
DARK_PALETTE.setColor(QPalette.BrightText, Qt.red)
DARK_PALETTE.setColor(QPalette.Highlight, QColor(90, 100, 150))
DARK_PALETTE.setColor(QPalette.HighlightedText, Qt.white)
DARK_PALETTE.setColor(QPalette.Disabled, QPalette.Text, QColor(150, 150, 150))
DARK_PALETTE.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(150, 150, 150))

class Character:
    def __init__(self):
        self.reset_character()
        
    def reset_character(self):
        # Core identity
        self.name = ""
        self.metatype = "Human"
        self.role = ""
        
        # Attributes
        self.attributes = {attr: 1 for attr in ATTRIBUTES}
        self.attributes["Edge"] = 1
        self.attributes["Magic"] = 0
        self.attributes["Resonance"] = 0
        
        # Derived stats
        self.physical_limit = 1
        self.mental_limit = 1
        self.social_limit = 1
        self.essence = 6.0
        self.nuyen = 0
        self.karma = 0
        self.lifestyle = "Squatter"
        
        # Skills
        self.skills = {skill: {"rating": 0, "specialization": ""} for skill in SKILLS}
        
        # Magic/Resonance
        self.powers = []
        self.foci = []
        self.drain_resist = 0
        
        # Qualities
        self.qualities = {"Positive": [], "Negative": []}
        
        # Combat stats
        self.physical_condition = 0
        self.stun_condition = 0
        self.overflow = 0
        self.initiative = 0
        self.initiative_dice = 1
        self.edge_points = 0
        self.max_edge = 1
        
        # Add max condition monitors
        self.max_physical_condition = 0
        self.max_stun_condition = 0
        
        # Gear
        self.cyberware = []
        self.bioware = []
        self.armor = 0
        
        # Flags
        self.wild_die_enabled = False
        self.overflow_enabled = True
        
        # Priority selection
        self.priorities = {
            "Metatype": "",
            "Attributes": "",
            "Skills": "",
            "Magic": "",
            "Resources": ""
        }
        
        # Calculate derived stats to initialize max condition and other derived values
        self.calculate_derived_stats()
    
    def calculate_derived_stats(self):
        # Calculate limits
        self.physical_limit = max(1, (2 * self.attributes["Strength"] + self.attributes["Body"] + self.attributes["Reaction"]) // 3)
        self.mental_limit = max(1, (2 * self.attributes["Logic"] + self.attributes["Willpower"] + self.attributes["Intuition"]) // 3)
        self.social_limit = max(1, (2 * self.attributes["Charisma"] + self.attributes["Willpower"] + int(self.essence)) // 3)
        
        # Condition monitors
        self.max_physical_condition = 8 + (self.attributes["Body"] // 2)
        self.max_stun_condition = 8 + (self.attributes["Willpower"] // 2)
        
        # Initiative
        self.initiative = self.attributes["Intuition"] + self.attributes["Reaction"]
        
        # Edge points
        self.max_edge = self.attributes["Edge"]
        self.edge_points = min(self.edge_points, self.max_edge)
        
        # Magic limits
        if self.attributes["Magic"] > 0:
            self.attributes["Magic"] = min(self.attributes["Magic"], int(self.essence))
            self.drain_resist = self.attributes["Willpower"]
            
        if self.attributes["Resonance"] > 0:
            self.attributes["Resonance"] = min(self.attributes["Resonance"], int(self.essence))
            self.drain_resist = self.attributes["Willpower"]
            
    def update_combat_display(self):
        # Condition monitors
        self.physical_progress.setText(f"{self.character.physical_condition}/{self.character.max_physical_condition}")
        self.stun_progress.setText(f"{self.character.stun_condition}/{self.character.max_stun_condition}")
        self.overflow_label.setText(f"Overflow: {self.character.overflow}")
        
        # Initiative
        self.initiative_label.setText(f"Base Initiative: {self.character.initiative}")
        self.initiative_dice_label.setText(f"Initiative Dice: {self.character.initiative_dice}d6")
        
        # Edge
        self.edge_spin.setValue(self.character.edge_points)
        self.wild_die_check.setChecked(self.character.wild_die_enabled)
        self.overflow_check.setChecked(self.character.overflow_enabled)
    
    def apply_metatype_bonuses(self):
        if self.metatype == "Elf":
            self.attributes["Charisma"] += 1
            self.attributes["Agility"] += 1
        elif self.metatype == "Dwarf":
            self.attributes["Body"] += 1
            self.attributes["Willpower"] += 1
        elif self.metatype == "Ork":
            self.attributes["Body"] += 1
            self.attributes["Strength"] += 1
        elif self.metatype == "Troll":
            self.attributes["Body"] += 2
            self.attributes["Strength"] += 2
        self.calculate_derived_stats()
    
    def add_cyberware(self, name, essence_cost):
        self.cyberware.append(name)
        self.essence -= essence_cost
        self.calculate_derived_stats()
    
    def add_bioware(self, name, essence_cost):
        self.bioware.append(name)
        self.essence -= essence_cost
        self.calculate_derived_stats()
    
    def add_power(self, power):
        if power not in self.powers:
            self.powers.append(power)
    
    def add_focus(self, focus):
        if focus not in self.foci:
            self.foci.append(focus)
    
    def add_quality(self, quality_type, quality):
        if quality not in self.qualities[quality_type]:
            self.qualities[quality_type].append(quality)
    
    def remove_quality(self, quality_type, quality):
        if quality in self.qualities[quality_type]:
            self.qualities[quality_type].remove(quality)
    
    def take_damage(self, damage_type, amount):
        if damage_type == "Physical":
            self.physical_condition = min(self.max_physical_condition, self.physical_condition + amount)
            if self.physical_condition >= self.max_physical_condition and self.overflow_enabled:
                self.overflow = min(10, self.overflow + (amount - (self.max_physical_condition - self.physical_condition)))
        elif damage_type == "Stun":
            self.stun_condition = min(self.max_stun_condition, self.stun_condition + amount)
    
    def heal_damage(self, damage_type, amount):
        if damage_type == "Physical":
            self.physical_condition = max(0, self.physical_condition - amount)
        elif damage_type == "Stun":
            self.stun_condition = max(0, self.stun_condition - amount)
    
    def spend_edge(self, amount):
        if amount <= self.edge_points:
            self.edge_points -= amount
            return True
        return False
    
    def burn_edge(self):
        if self.attributes["Edge"] > 1:
            self.attributes["Edge"] -= 1
            self.max_edge -= 1
            self.edge_points = self.max_edge
            return True
        return False
    
    def recover_naturally(self):
        # Physical recovery (weekly)
        self.physical_condition = max(0, self.physical_condition - (self.attributes["Body"] // 3))
        # Stun recovery (hourly)
        self.stun_condition = max(0, self.stun_condition - (self.attributes["Willpower"] // 2))
    
    def roll_initiative(self):
        return self.initiative + sum(random.randint(1, 6) for _ in range(self.initiative_dice))
    
    def to_dict(self):
        return {
            "name": self.name,
            "metatype": self.metatype,
            "role": self.role,
            "attributes": self.attributes,
            "skills": self.skills,
            "qualities": self.qualities,
            "powers": self.powers,
            "foci": self.foci,
            "cyberware": self.cyberware,
            "bioware": self.bioware,
            "nuyen": self.nuyen,
            "karma": self.karma,
            "lifestyle": self.lifestyle,
            "physical_condition": self.physical_condition,
            "stun_condition": self.stun_condition,
            "overflow": self.overflow,
            "edge_points": self.edge_points,
            "essence": self.essence,
            "armor": self.armor,
            "wild_die_enabled": self.wild_die_enabled,
            "overflow_enabled": self.overflow_enabled,
            "priorities": self.priorities
        }
    
    def from_dict(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.calculate_derived_stats()

class AttributeEditor(QWidget):
    valueChanged = Signal()
    
    def __init__(self, attribute, min_val, max_val, parent=None):
        super().__init__(parent)
        self.attribute = attribute
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel(f"{attribute}:")
        self.spinbox = QSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.valueChanged.connect(self.on_value_changed)
        
        layout.addWidget(self.label)
        layout.addWidget(self.spinbox)
    
    def on_value_changed(self):
        self.valueChanged.emit()
    
    def value(self):
        return self.spinbox.value()
    
    def set_value(self, value):
        self.spinbox.setValue(value)

class PrioritySelector(QWidget):
    priorityChanged = Signal()
    
    def __init__(self, category, parent=None):
        super().__init__(parent)
        self.category = category
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        self.label = QLabel(f"{category}:")
        self.combobox = QComboBox()
        self.combobox.addItems(PRIORITY_LEVELS)
        self.combobox.currentIndexChanged.connect(self.on_priority_changed)
        
        layout.addWidget(self.label)
        layout.addWidget(self.combobox)
    
    def on_priority_changed(self):
        self.priorityChanged.emit()
    
    def current_priority(self):
        return self.combobox.currentText()
    
    def set_priority(self, priority):
        index = self.combobox.findText(priority)
        if index >= 0:
            self.combobox.setCurrentIndex(index)

class CharacterManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shadowrun 6E Character Manager")
        self.setGeometry(100, 100, 1344, 768)
        
        # Apply dark theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2d2d37;
                color: #dcdcdc;
                font-size: 12px;
            }
            QTabWidget::pane {
                border: 1px solid #444;
                background: #23232d;
            }
            QTabBar::tab {
                background: #414158;
                color: #dcdcdc;
                padding: 8px;
                border: 1px solid #555;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #5a5a96;
                border-color: #777;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 1ex;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #414158;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 5px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4d4d6e;
            }
            QListWidget {
                background-color: #1e1e28;
                border: 1px solid #444;
            }
            QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox {
                background-color: #1e1e28;
                border: 1px solid #555;
                color: #dcdcdc;
                padding: 3px;
            }
        """)
        
        self.character = Character()
        self.init_ui()
        self.update_all_displays()
    
    def init_ui(self):
        # Create tabs
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Create tab widgets
        self.overview_tab = self.create_overview_tab()
        self.attributes_tab = self.create_attributes_tab()
        self.skills_tab = self.create_skills_tab()
        self.magic_tab = self.create_magic_tab()
        self.qualities_tab = self.create_qualities_tab()
        self.gear_tab = self.create_gear_tab()
        self.combat_tab = self.create_combat_tab()
        
        # Add tabs
        self.tabs.addTab(self.overview_tab, "Overview")
        self.tabs.addTab(self.attributes_tab, "Attributes")
        self.tabs.addTab(self.skills_tab, "Skills")
        self.tabs.addTab(self.magic_tab, "Magic/Resonance")
        self.tabs.addTab(self.qualities_tab, "Qualities")
        self.tabs.addTab(self.gear_tab, "Gear")
        self.tabs.addTab(self.combat_tab, "Combat")
        
        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        
        new_action = file_menu.addAction("New Character")
        new_action.triggered.connect(self.new_character)
        
        load_action = file_menu.addAction("Load Character")
        load_action.triggered.connect(self.load_character)
        
        save_action = file_menu.addAction("Save Character")
        save_action.triggered.connect(self.save_character)
    
    def create_overview_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Character info
        info_group = QGroupBox("Character Information")
        info_layout = QVBoxLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Character Name")
        self.name_edit.textChanged.connect(self.update_character_name)
        
        self.metatype_combo = QComboBox()
        self.metatype_combo.addItems(METATYPES)
        self.metatype_combo.currentIndexChanged.connect(self.update_metatype)
        
        self.role_edit = QLineEdit()
        self.role_edit.setPlaceholderText("Character Role")
        self.role_edit.textChanged.connect(self.update_role)
        
        info_layout.addWidget(QLabel("Name:"))
        info_layout.addWidget(self.name_edit)
        info_layout.addWidget(QLabel("Metatype:"))
        info_layout.addWidget(self.metatype_combo)
        info_layout.addWidget(QLabel("Role:"))
        info_layout.addWidget(self.role_edit)
        info_group.setLayout(info_layout)
        
        # Priority selection
        priority_group = QGroupBox("Priority Selection")
        priority_layout = QVBoxLayout()
        
        self.priority_selectors = {}
        for category in ["Metatype", "Attributes", "Skills", "Magic", "Resources"]:
            selector = PrioritySelector(category)
            selector.priorityChanged.connect(self.update_priorities)
            priority_layout.addWidget(selector)
            self.priority_selectors[category] = selector
        
        priority_group.setLayout(priority_layout)
        
        # Resources
        resources_group = QGroupBox("Resources")
        resources_layout = QVBoxLayout()
        
        self.nuyen_spin = QSpinBox()
        self.nuyen_spin.setRange(0, 1000000)
        self.nuyen_spin.valueChanged.connect(self.update_nuyen)
        
        self.karma_spin = QSpinBox()
        self.karma_spin.setRange(0, 1000)
        self.karma_spin.valueChanged.connect(self.update_karma)
        
        self.lifestyle_combo = QComboBox()
        self.lifestyle_combo.addItems(LIFESTYLES)
        self.lifestyle_combo.currentIndexChanged.connect(self.update_lifestyle)
        
        resources_layout.addWidget(QLabel("Nuyen:"))
        resources_layout.addWidget(self.nuyen_spin)
        resources_layout.addWidget(QLabel("Karma:"))
        resources_layout.addWidget(self.karma_spin)
        resources_layout.addWidget(QLabel("Lifestyle:"))
        resources_layout.addWidget(self.lifestyle_combo)
        resources_group.setLayout(resources_layout)
        
        # Stats display
        stats_group = QGroupBox("Derived Stats")
        stats_layout = QVBoxLayout()
        
        self.physical_limit_label = QLabel("Physical Limit: 1")
        self.mental_limit_label = QLabel("Mental Limit: 1")
        self.social_limit_label = QLabel("Social Limit: 1")
        self.essence_label = QLabel("Essence: 6.0")
        self.edge_label = QLabel("Edge: 1/1")
        
        stats_layout.addWidget(self.physical_limit_label)
        stats_layout.addWidget(self.mental_limit_label)
        stats_layout.addWidget(self.social_limit_label)
        stats_layout.addWidget(self.essence_label)
        stats_layout.addWidget(self.edge_label)
        stats_group.setLayout(stats_layout)
        
        # Assemble layout
        layout.addWidget(info_group)
        layout.addWidget(priority_group)
        layout.addWidget(resources_group)
        layout.addWidget(stats_group)
        
        return tab
    
    def create_attributes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Attribute editors
        attributes_group = QGroupBox("Attributes")
        attributes_layout = QVBoxLayout()
        
        self.attribute_editors = {}
        for attribute in ATTRIBUTES + ["Edge", "Magic", "Resonance"]:
            min_val = 1
            max_val = 12
            if attribute in ["Magic", "Resonance"]:
                min_val = 0
            editor = AttributeEditor(attribute, min_val, max_val)
            editor.valueChanged.connect(self.update_attributes)
            attributes_layout.addWidget(editor)
            self.attribute_editors[attribute] = editor
        
        attributes_group.setLayout(attributes_layout)
        layout.addWidget(attributes_group)
        
        return tab
    
    def create_skills_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Skills editor
        skills_group = QGroupBox("Skills")
        skills_layout = QVBoxLayout()
        
        self.skill_editors = {}
        for skill in SKILLS:
            skill_widget = QWidget()
            skill_layout = QHBoxLayout(skill_widget)
            
            skill_label = QLabel(skill)
            rating_spin = QSpinBox()
            rating_spin.setRange(0, 12)
            rating_spin.valueChanged.connect(lambda val, s=skill: self.update_skill_rating(s, val))
            
            spec_edit = QLineEdit()
            spec_edit.setPlaceholderText("Specialization")
            spec_edit.textChanged.connect(lambda text, s=skill: self.update_skill_specialization(s, text))
            
            skill_layout.addWidget(skill_label)
            skill_layout.addWidget(QLabel("Rating:"))
            skill_layout.addWidget(rating_spin)
            skill_layout.addWidget(QLabel("Specialization:"))
            skill_layout.addWidget(spec_edit)
            
            skills_layout.addWidget(skill_widget)
            self.skill_editors[skill] = {"rating": rating_spin, "specialization": spec_edit}
        
        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)
        
        return tab
    
    def create_magic_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Powers
        powers_group = QGroupBox("Powers")
        powers_layout = QVBoxLayout()
        
        self.powers_list = QListWidget()
        self.powers_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
        add_power_button = QPushButton("Add Selected Powers")
        add_power_button.clicked.connect(self.add_selected_powers)
        
        for power in POWERS:
            item = QListWidgetItem(power)
            self.powers_list.addItem(item)
        
        powers_layout.addWidget(self.powers_list)
        powers_layout.addWidget(add_power_button)
        powers_group.setLayout(powers_layout)
        
        # Foci
        foci_group = QGroupBox("Foci")
        foci_layout = QVBoxLayout()
        
        self.foci_list = QListWidget()
        self.foci_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
        add_focus_button = QPushButton("Add Selected Foci")
        add_focus_button.clicked.connect(self.add_selected_foci)
        
        for focus in FOCI:
            item = QListWidgetItem(focus)
            self.foci_list.addItem(item)
        
        foci_layout.addWidget(self.foci_list)
        foci_layout.addWidget(add_focus_button)
        foci_group.setLayout(foci_layout)
        
        # Drain resist
        drain_group = QGroupBox("Drain Resistance")
        drain_layout = QVBoxLayout()
        self.drain_label = QLabel("Drain Resist: 0")
        drain_layout.addWidget(self.drain_label)
        drain_group.setLayout(drain_layout)
        
        # Current selections
        current_group = QGroupBox("Current Selections")
        current_layout = QVBoxLayout()
        
        self.current_powers_label = QLabel("Powers: None")
        self.current_foci_label = QLabel("Foci: None")
        
        current_layout.addWidget(self.current_powers_label)
        current_layout.addWidget(self.current_foci_label)
        current_group.setLayout(current_layout)
        
        # Assemble layout
        layout.addWidget(powers_group)
        layout.addWidget(foci_group)
        layout.addWidget(drain_group)
        layout.addWidget(current_group)
        
        return tab
    
    def create_qualities_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Qualities selection
        qualities_group = QGroupBox("Qualities")
        qualities_layout = QHBoxLayout()
        
        # Positive qualities
        positive_group = QGroupBox("Positive Qualities")
        positive_layout = QVBoxLayout()
        
        self.positive_list = QListWidget()
        self.positive_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
        for quality in QUALITIES["Positive"]:
            item = QListWidgetItem(quality)
            self.positive_list.addItem(item)
        
        positive_layout.addWidget(self.positive_list)
        positive_group.setLayout(positive_layout)
        
        # Negative qualities
        negative_group = QGroupBox("Negative Qualities")
        negative_layout = QVBoxLayout()
        
        self.negative_list = QListWidget()
        self.negative_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
        for quality in QUALITIES["Negative"]:
            item = QListWidgetItem(quality)
            self.negative_list.addItem(item)
        
        negative_layout.addWidget(self.negative_list)
        negative_group.setLayout(negative_layout)
        
        qualities_layout.addWidget(positive_group)
        qualities_layout.addWidget(negative_group)
        qualities_group.setLayout(qualities_layout)
        
        # Create a widget for the button layout
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        add_positive_button = QPushButton("Add Selected Positive")
        add_positive_button.clicked.connect(self.add_selected_positive_qualities)
        
        add_negative_button = QPushButton("Add Selected Negative")
        add_negative_button.clicked.connect(self.add_selected_negative_qualities)
        
        remove_qualities_button = QPushButton("Remove Selected Qualities")
        remove_qualities_button.clicked.connect(self.remove_selected_qualities)
        
        button_layout.addWidget(add_positive_button)
        button_layout.addWidget(add_negative_button)
        button_layout.addWidget(remove_qualities_button)
        
        # Current qualities
        current_group = QGroupBox("Current Qualities")
        current_layout = QVBoxLayout()
        
        self.current_qualities_list = QListWidget()
        self.current_qualities_list.setSelectionMode(QAbstractItemView.MultiSelection)
        
        current_layout.addWidget(self.current_qualities_list)
        current_group.setLayout(current_layout)
        
        # Assemble layout
        layout.addWidget(qualities_group)
        layout.addWidget(button_widget)  # Add the widget containing the button layout
        layout.addWidget(current_group)
        
        return tab
    
    def create_gear_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Cyberware
        cyberware_group = QGroupBox("Cyberware")
        cyberware_layout = QVBoxLayout()
        
        self.cyberware_list = QListWidget()
        self.cyberware_list.addItems([
            "Datajack (0.2 Essence)", 
            "Cybereyes (0.4 Essence)", 
            "Wired Reflexes (2.0 Essence)",
            "Cyberarm (0.8 Essence)",
            "Bone Lacing (0.6 Essence)"
        ])
        
        add_cyberware_button = QPushButton("Add Selected Cyberware")
        add_cyberware_button.clicked.connect(self.add_selected_cyberware)
        
        cyberware_layout.addWidget(self.cyberware_list)
        cyberware_layout.addWidget(add_cyberware_button)
        cyberware_group.setLayout(cyberware_layout)
        
        # Bioware
        bioware_group = QGroupBox("Bioware")
        bioware_layout = QVBoxLayout()
        
        self.bioware_list = QListWidget()
        self.bioware_list.addItems([
            "Muscle Toner (0.6 Essence)", 
            "Orthoskin (0.4 Essence)", 
            "Tailored Pheromones (0.8 Essence)",
            "Synaptic Booster (1.2 Essence)"
        ])
        
        add_bioware_button = QPushButton("Add Selected Bioware")
        add_bioware_button.clicked.connect(self.add_selected_bioware)
        
        bioware_layout.addWidget(self.bioware_list)
        bioware_layout.addWidget(add_bioware_button)
        bioware_group.setLayout(bioware_layout)
        
        # Current augmentations
        current_group = QGroupBox("Current Augmentations")
        current_layout = QVBoxLayout()
        
        self.current_cyberware_list = QListWidget()
        self.current_bioware_list = QListWidget()
        
        current_layout.addWidget(QLabel("Cyberware:"))
        current_layout.addWidget(self.current_cyberware_list)
        current_layout.addWidget(QLabel("Bioware:"))
        current_layout.addWidget(self.current_bioware_list)
        current_group.setLayout(current_layout)
        
        # Armor
        armor_group = QGroupBox("Armor")
        armor_layout = QVBoxLayout()
        
        self.armor_spin = QSpinBox()
        self.armor_spin.setRange(0, 20)
        self.armor_spin.valueChanged.connect(self.update_armor)
        
        armor_layout.addWidget(QLabel("Armor Rating:"))
        armor_layout.addWidget(self.armor_spin)
        armor_group.setLayout(armor_layout)
        
        # Assemble layout
        layout.addWidget(cyberware_group)
        layout.addWidget(bioware_group)
        layout.addWidget(current_group)
        layout.addWidget(armor_group)
        
        return tab
    
    def create_combat_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Condition monitors
        condition_group = QGroupBox("Condition Monitors")
        condition_layout = QHBoxLayout()
        
        # Physical condition
        physical_group = QGroupBox("Physical Condition")
        physical_layout = QVBoxLayout()
        
        self.physical_progress = QLabel("0/0")
        self.physical_progress.setFont(QFont("Arial", 14, QFont.Bold))
        self.physical_progress.setAlignment(Qt.AlignCenter)
        
        self.physical_increment = QSpinBox()
        self.physical_increment.setRange(1, 10)
        self.physical_increment.setValue(1)
        
        damage_physical_button = QPushButton("Take Damage")
        damage_physical_button.clicked.connect(lambda: self.take_damage("Physical"))
        
        heal_physical_button = QPushButton("Heal Damage")
        heal_physical_button.clicked.connect(lambda: self.heal_damage("Physical"))
        
        physical_layout.addWidget(self.physical_progress)
        physical_layout.addWidget(QLabel("Damage Amount:"))
        physical_layout.addWidget(self.physical_increment)
        physical_layout.addWidget(damage_physical_button)
        physical_layout.addWidget(heal_physical_button)
        physical_group.setLayout(physical_layout)
        
        # Stun condition
        stun_group = QGroupBox("Stun Condition")
        stun_layout = QVBoxLayout()
        
        self.stun_progress = QLabel("0/0")
        self.stun_progress.setFont(QFont("Arial", 14, QFont.Bold))
        self.stun_progress.setAlignment(Qt.AlignCenter)
        
        self.stun_increment = QSpinBox()
        self.stun_increment.setRange(1, 10)
        self.stun_increment.setValue(1)
        
        damage_stun_button = QPushButton("Take Damage")
        damage_stun_button.clicked.connect(lambda: self.take_damage("Stun"))
        
        heal_stun_button = QPushButton("Heal Damage")
        heal_stun_button.clicked.connect(lambda: self.heal_damage("Stun"))
        
        stun_layout.addWidget(self.stun_progress)
        stun_layout.addWidget(QLabel("Damage Amount:"))
        stun_layout.addWidget(self.stun_increment)
        stun_layout.addWidget(damage_stun_button)
        stun_layout.addWidget(heal_stun_button)
        stun_group.setLayout(stun_layout)
        
        # Overflow
        overflow_group = QGroupBox("Overflow")
        overflow_layout = QVBoxLayout()
        
        self.overflow_label = QLabel("Overflow: 0")
        self.overflow_label.setFont(QFont("Arial", 12))
        
        overflow_layout.addWidget(self.overflow_label)
        overflow_group.setLayout(overflow_layout)
        
        condition_layout.addWidget(physical_group)
        condition_layout.addWidget(stun_group)
        condition_layout.addWidget(overflow_group)
        condition_group.setLayout(condition_layout)
        
        # Initiative
        initiative_group = QGroupBox("Initiative")
        initiative_layout = QVBoxLayout()
        
        self.initiative_label = QLabel("Base Initiative: 0")
        self.initiative_dice_label = QLabel("Initiative Dice: 1d6")
        self.roll_initiative_button = QPushButton("Roll Initiative")
        self.roll_initiative_button.clicked.connect(self.roll_character_initiative)
        self.initiative_result = QLabel("")
        self.initiative_result.setFont(QFont("Arial", 16, QFont.Bold))
        
        initiative_layout.addWidget(self.initiative_label)
        initiative_layout.addWidget(self.initiative_dice_label)
        initiative_layout.addWidget(self.roll_initiative_button)
        initiative_layout.addWidget(self.initiative_result)
        initiative_group.setLayout(initiative_layout)
        
        # Edge management
        edge_group = QGroupBox("Edge Points")
        edge_layout = QVBoxLayout()
        
        self.edge_spin = QSpinBox()
        self.edge_spin.setRange(0, 7)
        self.edge_spin.valueChanged.connect(self.update_edge_points)
        
        self.burn_edge_button = QPushButton("Burn Edge")
        self.burn_edge_button.clicked.connect(self.burn_edge)
        
        self.recover_button = QPushButton("Natural Recovery")
        self.recover_button.clicked.connect(self.natural_recovery)
        
        self.wild_die_check = QCheckBox("Enable Wild Die")
        self.wild_die_check.stateChanged.connect(self.toggle_wild_die)
        
        self.overflow_check = QCheckBox("Enable Overflow Rules")
        self.overflow_check.stateChanged.connect(self.toggle_overflow)
        
        edge_layout.addWidget(QLabel("Current Edge Points:"))
        edge_layout.addWidget(self.edge_spin)
        edge_layout.addWidget(self.burn_edge_button)
        edge_layout.addWidget(self.recover_button)
        edge_layout.addWidget(self.wild_die_check)
        edge_layout.addWidget(self.overflow_check)
        edge_group.setLayout(edge_layout)
        
        # Assemble layout
        layout.addWidget(condition_group)
        layout.addWidget(initiative_group)
        layout.addWidget(edge_group)
        
        return tab
    
    def update_character_name(self):
        self.character.name = self.name_edit.text()
    
    def update_metatype(self):
        self.character.metatype = self.metatype_combo.currentText()
        self.character.apply_metatype_bonuses()
        self.update_all_displays()
    
    def update_role(self):
        self.character.role = self.role_edit.text()
    
    def update_priorities(self):
        for category, selector in self.priority_selectors.items():
            self.character.priorities[category] = selector.current_priority()
    
    def update_nuyen(self):
        self.character.nuyen = self.nuyen_spin.value()
    
    def update_karma(self):
        self.character.karma = self.karma_spin.value()
    
    def update_lifestyle(self):
        self.character.lifestyle = self.lifestyle_combo.currentText()
    
    def update_attributes(self):
        for attribute, editor in self.attribute_editors.items():
            self.character.attributes[attribute] = editor.value()
        self.character.calculate_derived_stats()
        self.update_all_displays()
    
    def update_skill_rating(self, skill, rating):
        self.character.skills[skill]["rating"] = rating
    
    def update_skill_specialization(self, skill, specialization):
        self.character.skills[skill]["specialization"] = specialization
    
    def add_selected_powers(self):
        selected_items = self.powers_list.selectedItems()
        for item in selected_items:
            power = item.text()
            self.character.add_power(power)
        self.update_magic_display()
    
    def add_selected_foci(self):
        selected_items = self.foci_list.selectedItems()
        for item in selected_items:
            focus = item.text()
            self.character.add_focus(focus)
        self.update_magic_display()
    
    def add_selected_positive_qualities(self):
        selected_items = self.positive_list.selectedItems()
        for item in selected_items:
            quality = item.text()
            self.character.add_quality("Positive", quality)
        self.update_qualities_display()
    
    def add_selected_negative_qualities(self):
        selected_items = self.negative_list.selectedItems()
        for item in selected_items:
            quality = item.text()
            self.character.add_quality("Negative", quality)
        self.update_qualities_display()
    
    def remove_selected_qualities(self):
        selected_items = self.current_qualities_list.selectedItems()
        for item in selected_items:
            quality = item.text()
            # Determine if it's positive or negative
            if quality in QUALITIES["Positive"]:
                self.character.remove_quality("Positive", quality)
            elif quality in QUALITIES["Negative"]:
                self.character.remove_quality("Negative", quality)
        self.update_qualities_display()
    
    def add_selected_cyberware(self):
        selected_items = self.cyberware_list.selectedItems()
        essence_costs = {
            "Datajack (0.2 Essence)": 0.2,
            "Cybereyes (0.4 Essence)": 0.4,
            "Wired Reflexes (2.0 Essence)": 2.0,
            "Cyberarm (0.8 Essence)": 0.8,
            "Bone Lacing (0.6 Essence)": 0.6
        }
        for item in selected_items:
            cyberware = item.text()
            if cyberware in essence_costs:
                self.character.add_cyberware(cyberware, essence_costs[cyberware])
        self.update_gear_display()
    
    def add_selected_bioware(self):
        selected_items = self.bioware_list.selectedItems()
        essence_costs = {
            "Muscle Toner (0.6 Essence)": 0.6,
            "Orthoskin (0.4 Essence)": 0.4,
            "Tailored Pheromones (0.8 Essence)": 0.8,
            "Synaptic Booster (1.2 Essence)": 1.2
        }
        for item in selected_items:
            bioware = item.text()
            if bioware in essence_costs:
                self.character.add_bioware(bioware, essence_costs[bioware])
        self.update_gear_display()
    
    def update_armor(self):
        self.character.armor = self.armor_spin.value()
    
    def take_damage(self, damage_type):
        amount = self.physical_increment.value() if damage_type == "Physical" else self.stun_increment.value()
        self.character.take_damage(damage_type, amount)
        self.update_combat_display()
    
    def heal_damage(self, damage_type):
        amount = self.physical_increment.value() if damage_type == "Physical" else self.stun_increment.value()
        self.character.heal_damage(damage_type, amount)
        self.update_combat_display()
    
    def update_edge_points(self):
        self.character.edge_points = self.edge_spin.value()
    
    def burn_edge(self):
        if self.character.burn_edge():
            QMessageBox.information(self, "Edge Burned", "Edge attribute permanently reduced by 1!")
            self.update_all_displays()
    
    def natural_recovery(self):
        self.character.recover_naturally()
        self.update_combat_display()
    
    def toggle_wild_die(self, state):
        self.character.wild_die_enabled = state == Qt.Checked
    
    def toggle_overflow(self, state):
        self.character.overflow_enabled = state == Qt.Checked
    
    def roll_character_initiative(self):
        result = self.character.roll_initiative()
        self.initiative_result.setText(f"Rolled: {result}")
    
    def update_all_displays(self):
        self.update_overview_display()
        self.update_attributes_display()
        self.update_skills_display()
        self.update_magic_display()
        self.update_qualities_display()
        self.update_gear_display()
        self.update_combat_display()
    
    def update_overview_display(self):
        self.name_edit.setText(self.character.name)
        self.metatype_combo.setCurrentText(self.character.metatype)
        self.role_edit.setText(self.character.role)
        
        for category, selector in self.priority_selectors.items():
            selector.set_priority(self.character.priorities.get(category, ""))
        
        self.nuyen_spin.setValue(self.character.nuyen)
        self.karma_spin.setValue(self.character.karma)
        self.lifestyle_combo.setCurrentText(self.character.lifestyle)
        
        self.physical_limit_label.setText(f"Physical Limit: {self.character.physical_limit}")
        self.mental_limit_label.setText(f"Mental Limit: {self.character.mental_limit}")
        self.social_limit_label.setText(f"Social Limit: {self.character.social_limit}")
        self.essence_label.setText(f"Essence: {self.character.essence:.1f}")
        self.edge_label.setText(f"Edge: {self.character.edge_points}/{self.character.max_edge}")
    
    def update_attributes_display(self):
        for attribute, value in self.character.attributes.items():
            if attribute in self.attribute_editors:
                self.attribute_editors[attribute].set_value(value)
    
    def update_skills_display(self):
        for skill, data in self.character.skills.items():
            if skill in self.skill_editors:
                self.skill_editors[skill]["rating"].setValue(data["rating"])
                self.skill_editors[skill]["specialization"].setText(data["specialization"])
    
    def update_magic_display(self):
        # Update powers display
        self.current_powers_label.setText(f"Powers: {', '.join(self.character.powers) if self.character.powers else 'None'}")
        
        # Update foci display
        self.current_foci_label.setText(f"Foci: {', '.join(self.character.foci) if self.character.foci else 'None'}")
        
        # Update drain resist
        self.drain_label.setText(f"Drain Resist: {self.character.drain_resist}")
    
    def update_qualities_display(self):
        self.current_qualities_list.clear()
        for q_type in ["Positive", "Negative"]:
            for quality in self.character.qualities[q_type]:
                item = QListWidgetItem(f"{quality} ({q_type})")
                self.current_qualities_list.addItem(item)
    
    def update_gear_display(self):
        # Update cyberware list
        self.current_cyberware_list.clear()
        for cyberware in self.character.cyberware:
            self.current_cyberware_list.addItem(cyberware)
        
        # Update bioware list
        self.current_bioware_list.clear()
        for bioware in self.character.bioware:
            self.current_bioware_list.addItem(bioware)
        
        # Update armor
        self.armor_spin.setValue(self.character.armor)
    
    def update_combat_display(self):
        # Condition monitors
        self.physical_progress.setText(f"{self.character.physical_condition}/{self.character.max_physical_condition}")
        self.stun_progress.setText(f"{self.character.stun_condition}/{self.character.max_stun_condition}")
        self.overflow_label.setText(f"Overflow: {self.character.overflow}")
        
        # Initiative
        self.initiative_label.setText(f"Base Initiative: {self.character.initiative}")
        self.initiative_dice_label.setText(f"Initiative Dice: {self.character.initiative_dice}d6")
        
        # Edge
        self.edge_spin.setValue(self.character.edge_points)
        self.wild_die_check.setChecked(self.character.wild_die_enabled)
        self.overflow_check.setChecked(self.character.overflow_enabled)
    
    def new_character(self):
        self.character.reset_character()
        self.update_all_displays()
        QMessageBox.information(self, "New Character", "New character created!")
    
    def save_character(self):
        file_name = f"{self.character.name.replace(' ', '_')}.json" if self.character.name else "character.json"
        try:
            with open(file_name, 'w') as f:
                json.dump(self.character.to_dict(), f, indent=2)
            QMessageBox.information(self, "Save Successful", f"Character saved to {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save character: {str(e)}")
    
    def load_character(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Character", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    data = json.load(f)
                self.character.from_dict(data)
                self.update_all_displays()
                QMessageBox.information(self, "Load Successful", f"Character loaded from {file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Load Error", f"Failed to load character: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    app.setPalette(DARK_PALETTE)
    manager = CharacterManager()
    manager.show()
    app.exec()
