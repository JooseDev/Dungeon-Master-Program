from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QComboBox, QMessageBox

class PlayerManager(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.players = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Player list
        self.player_list = QListWidget()

        # Player details
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Player Name')
        self.campaign_dropdown = QComboBox()

        # Buttons
        self.add_player_button = QPushButton('Add Player')
        self.edit_player_button = QPushButton('Edit Player')
        self.delete_player_button = QPushButton('Delete Player')

        self.add_player_button.clicked.connect(self.add_player)
        self.edit_player_button.clicked.connect(self.edit_player)
        self.delete_player_button.clicked.connect(self.delete_player)

        layout.addWidget(self.player_list)
        layout.addWidget(self.name_input)
        layout.addWidget(self.campaign_dropdown)
        layout.addWidget(self.add_player_button)
        layout.addWidget(self.edit_player_button)
        layout.addWidget(self.delete_player_button)

        self.setLayout(layout)
        self.update_campaign_dropdown()

    def load_data(self, players):
        self.players = players
        self.update_player_list()

    def update_campaign_dropdown(self):
        self.campaign_dropdown.clear()
        for campaign in self.main_window.campaign_manager.campaigns.keys():
            self.campaign_dropdown.addItem(campaign)

    def update_player_list(self):
        self.player_list.clear()
        for player in self.players:
            self.player_list.addItem(f"{player['name']} - {player['campaign']}")

    def add_player(self):
        name = self.name_input.text()
        campaign = self.campaign_dropdown.currentText()

        if name:
            self.players.append({'name': name, 'campaign': campaign})
            self.update_player_list()
            self.save_players()
        else:
            QMessageBox.warning(self, 'Error', 'Player name cannot be empty.')

    def edit_player(self):
        selected_items = self.player_list.selectedItems()
        if selected_items:
            index = self.player_list.row(selected_items[0])
            self.players[index]['name'] = self.name_input.text()
            self.players[index]['campaign'] = self.campaign_dropdown.currentText()
            self.update_player_list()
            self.save_players()
        else:
            QMessageBox.warning(self, 'Error', 'No player selected to edit.')

    def delete_player(self):
        selected_items = self.player_list.selectedItems()
        if selected_items:
            index = self.player_list.row(selected_items[0])
            del self.players[index]
            self.update_player_list()
            self.save_players()
        else:
            QMessageBox.warning(self, 'Error', 'No player selected to delete.')

    def save_players(self):
        current_item = self.main_window.campaign_manager.campaign_list.currentItem()
        
        if current_item is None:
            QMessageBox.warning(self, 'Error', 'No campaign selected. Please select a campaign to add players.')
            return

        campaign_name = current_item.text()
        self.main_window.campaign_manager.campaigns[campaign_name]['players'] = self.players
        self.main_window.campaign_manager.save_campaigns()