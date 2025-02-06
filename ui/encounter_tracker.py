from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QComboBox, QSpinBox, QMessageBox
import json
import os

class EncounterTracker(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.enemies = []
        self.encounter_participants = []  # List to hold players and enemies in the encounter
        self.current_turn_index = 0
        self.init_ui()
        self.load_enemy_list()
        self.update_player_dropdown()

    def init_ui(self):
        layout = QVBoxLayout()

        # List of participants (players + enemies)
        self.participant_list = QListWidget()

        # Add enemy section
        add_enemy_layout = QHBoxLayout()
        self.enemy_dropdown = QComboBox()
        self.initiative_input = QSpinBox()
        self.initiative_input.setRange(1, 100)
        self.add_enemy_button = QPushButton('Add Enemy')
        self.add_enemy_button.clicked.connect(self.add_enemy)

        add_enemy_layout.addWidget(self.enemy_dropdown)
        add_enemy_layout.addWidget(self.initiative_input)
        add_enemy_layout.addWidget(self.add_enemy_button)

        # Add player to encounter
        add_player_layout = QHBoxLayout()
        self.player_dropdown = QComboBox()
        self.add_player_button = QPushButton('Add Player to Encounter')
        self.add_player_initiative = QSpinBox()
        self.add_player_initiative.setRange(1, 100)
        self.add_player_button.clicked.connect(self.add_player_to_encounter)
        add_player_layout.addWidget(self.player_dropdown)
        add_player_layout.addWidget(self.add_player_initiative)
        add_player_layout.addWidget(self.add_player_button)

        # Remove participant button
        self.remove_participant_button = QPushButton('Remove Selected Participant')
        self.remove_participant_button.clicked.connect(self.remove_participant)

        # Next turn button
        self.next_turn_button = QPushButton('Next Turn')
        self.next_turn_button.clicked.connect(self.next_turn)

        layout.addLayout(add_enemy_layout)
        layout.addLayout(add_player_layout)
        layout.addWidget(self.participant_list)
        layout.addWidget(self.remove_participant_button)
        layout.addWidget(self.next_turn_button)

        self.setLayout(layout)

    def load_enemy_list(self):
        save_file = 'saves/enemies.json'
        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                enemies = json.load(file)
                for enemy_name in enemies.keys():
                    self.enemy_dropdown.addItem(enemy_name)

    def load_players(self, players):
        self.players = players  # Keep a list of all available players
        self.update_player_dropdown()  # Only update the dropdown, don't add to the encounter

    def load_data(self, encounters):
        self.enemies = encounters
        self.players = []
        self.update_participant_list()
        self.update_player_dropdown()

    def update_player_dropdown(self):
        self.player_dropdown.clear()
        if hasattr(self.main_window, 'player_manager'):
            for player in self.main_window.player_manager.players:
                self.player_dropdown.addItem(player['name'])

    def add_enemy(self):
        enemy_name = self.enemy_dropdown.currentText()
        initiative = self.initiative_input.value()

        if enemy_name:
            enemy = {'name': enemy_name, 'initiative': initiative}
            self.encounter_participants.append(enemy)  # Add to encounter participants
            self.update_participant_list()
        else:
            QMessageBox.warning(self, 'Error', 'No enemy selected.')

    def add_player_to_encounter(self):
        player_name = self.player_dropdown.currentText()
        initiative = self.add_player_initiative.value()

        if player_name:
            player = {'name': player_name, 'initiative': initiative}
            self.encounter_participants.append(player)  # Add to encounter participants
            self.update_participant_list()
        else:
            QMessageBox.warning(self, 'Error', 'No player selected.')

    def remove_participant(self):
        selected_items = self.participant_list.selectedItems()
        if selected_items:
            index = self.participant_list.row(selected_items[0])
            del self.encounter_participants[index]
            self.update_participant_list()
        else:
            QMessageBox.warning(self, 'Error', 'No participant selected to remove.')

    def update_participant_list(self):
        self.participant_list.clear()
        self.encounter_participants.sort(key=lambda x: x['initiative'], reverse=True)
        for idx, participant in enumerate(self.encounter_participants):
            turn_indicator = ' (Current Turn)' if idx == self.current_turn_index else ''
            self.participant_list.addItem(f"{participant['name']} (Initiative: {participant['initiative']}){turn_indicator}")

    def next_turn(self):
        if self.encounter_participants:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.encounter_participants)
            self.update_participant_list()
        else:
            QMessageBox.warning(self, 'Error', 'No participants in the encounter.')