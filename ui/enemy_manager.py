from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QLineEdit, QSpinBox, QTextEdit
import json
import os

class EnemyManager(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.enemies = {}
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.enemy_list = QListWidget()
        self.enemy_list.itemClicked.connect(self.load_enemy)

        self.new_enemy_input = QLineEdit('Enter new enemy name')
        self.create_enemy_button = QPushButton('Create Enemy')
        self.create_enemy_button.clicked.connect(self.create_enemy)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.enemy_list)
        left_layout.addWidget(self.new_enemy_input)
        left_layout.addWidget(self.create_enemy_button)

        self.stats_inputs = {}
        stats_layout = QVBoxLayout()
        for stat in ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']:
            label = QLabel(stat)
            spinbox = QSpinBox()
            spinbox.setRange(1, 30)
            self.stats_inputs[stat] = spinbox
            stats_layout.addWidget(label)
            stats_layout.addWidget(spinbox)
        
        self.actions_text = QTextEdit()
        self.spells_text = QTextEdit()
        
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_enemy_changes)
        
        right_layout = QVBoxLayout()
        right_layout.addLayout(stats_layout)
        right_layout.addWidget(QLabel("Actions"))
        right_layout.addWidget(self.actions_text)
        right_layout.addWidget(QLabel("Spells"))
        right_layout.addWidget(self.spells_text)
        right_layout.addWidget(self.save_button)
        
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)
        self.setLayout(layout)
        self.load_enemies()

    def load_enemies(self):
        save_file = 'saves/enemies.json'
        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                self.enemies = json.load(file)
                for enemy_name in self.enemies.keys():
                    self.enemy_list.addItem(enemy_name)
        else:
            with open(save_file, 'w') as file:
                json.dump({}, file)

    def save_enemies(self):
        with open('saves/enemies.json', 'w') as file:
            json.dump(self.enemies, file, indent=4)

    def create_enemy(self):
        enemy_name = self.new_enemy_input.text().strip()
        if enemy_name and enemy_name not in self.enemies:
            enemy_data = {
                'name': enemy_name,
                'stats': { stat: 10 for stat in self.stats_inputs.keys() },
                'actions': [],
                'spells': []
            }
            self.enemies[enemy_name] = enemy_data
            self.enemy_list.addItem(enemy_name)
            self.save_enemies()

    def load_enemy(self, item):
        enemy_name = item.text()
        if enemy_name in self.enemies:
            enemy_data = self.enemies[enemy_name]
            for stat, spinbox in self.stats_inputs.items():
                spinbox.setValue(enemy_data['stats'].get(stat, 10))
            self.actions_text.setPlainText("\n".join(enemy_data['actions']))
            self.spells_text.setPlainText("\n".join(enemy_data['spells']))

    def save_enemy_changes(self):
        selected_item = self.enemy_list.currentItem()
        if selected_item:
            enemy_name = selected_item.text()
            self.enemies[enemy_name]['stats'] = { stat: spinbox.value() for stat, spinbox in self.stats_inputs.items() }
            self.enemies[enemy_name]['actions'] = self.actions_text.toPlainText().split("\n")
            self.enemies[enemy_name]['spells'] = self.spells_text.toPlainText().split("\n")
            self.save_enemies()