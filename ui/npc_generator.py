from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QTextEdit, QLabel, QFormLayout, QSpinBox, QMessageBox
import json

class NPCGenerator(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.npcs = []
        self.selected_npc_index = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Left side - NPC list and action buttons
        self.npc_list = QListWidget()
        self.npc_list.itemClicked.connect(self.load_npc)

        self.add_npc_button = QPushButton('Add NPC')
        self.edit_npc_button = QPushButton('Save NPC')
        self.delete_npc_button = QPushButton('Delete NPC')

        self.add_npc_button.clicked.connect(self.add_npc)
        self.edit_npc_button.clicked.connect(self.edit_npc)
        self.delete_npc_button.clicked.connect(self.delete_npc)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.npc_list)
        left_layout.addWidget(self.add_npc_button)
        left_layout.addWidget(self.edit_npc_button)
        left_layout.addWidget(self.delete_npc_button)

        # Right side - NPC details
        self.name_input = QLineEdit()
        self.backstory_input = QTextEdit()

        self.stats_layout = QFormLayout()
        self.strength_input = QSpinBox()
        self.dexterity_input = QSpinBox()
        self.intelligence_input = QSpinBox()
        self.charisma_input = QSpinBox()

        self.stats_layout.addRow('Strength:', self.strength_input)
        self.stats_layout.addRow('Dexterity:', self.dexterity_input)
        self.stats_layout.addRow('Intelligence:', self.intelligence_input)
        self.stats_layout.addRow('Charisma:', self.charisma_input)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel('Name:'))
        right_layout.addWidget(self.name_input)
        right_layout.addWidget(QLabel('Backstory:'))
        right_layout.addWidget(self.backstory_input)
        right_layout.addLayout(self.stats_layout)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)

    def load_data(self, npcs):
        self.npcs = npcs
        self.npc_list.clear()
        for npc in self.npcs:
            self.npc_list.addItem(npc['name'])

    def add_npc(self):
        npc = {
            'name': self.name_input.text(),
            'backstory': self.backstory_input.toPlainText(),
            'stats': {
                'strength': self.strength_input.value(),
                'dexterity': self.dexterity_input.value(),
                'intelligence': self.intelligence_input.value(),
                'charisma': self.charisma_input.value()
            }
        }
        self.npcs.append(npc)
        self.npc_list.addItem(npc['name'])
        self.save_npcs()

    def edit_npc(self):
        if self.selected_npc_index is not None:
            npc = self.npcs[self.selected_npc_index]
            npc['name'] = self.name_input.text()
            npc['backstory'] = self.backstory_input.toPlainText()
            npc['stats'] = {
                'strength': self.strength_input.value(),
                'dexterity': self.dexterity_input.value(),
                'intelligence': self.intelligence_input.value(),
                'charisma': self.charisma_input.value()
            }
            self.npc_list.item(self.selected_npc_index).setText(npc['name'])
            self.save_npcs()
        else:
            QMessageBox.warning(self, 'Error', 'No NPC selected for editing.')

    def delete_npc(self):
        if self.selected_npc_index is not None:
            del self.npcs[self.selected_npc_index]
            self.npc_list.takeItem(self.selected_npc_index)
            self.selected_npc_index = None
            self.save_npcs()
        else:
            QMessageBox.warning(self, 'Error', 'No NPC selected for deletion.')

    def load_npc(self, item):
        self.selected_npc_index = self.npc_list.row(item)
        npc = self.npcs[self.selected_npc_index]
        self.name_input.setText(npc['name'])
        self.backstory_input.setText(npc['backstory'])
        self.strength_input.setValue(npc['stats']['strength'])
        self.dexterity_input.setValue(npc['stats']['dexterity'])
        self.intelligence_input.setValue(npc['stats']['intelligence'])
        self.charisma_input.setValue(npc['stats']['charisma'])

    def save_npcs(self):
        self.main_window.campaign_manager.campaigns[self.main_window.campaign_manager.campaign_list.currentItem().text()]['npcs'] = self.npcs
        self.main_window.campaign_manager.save_campaigns()