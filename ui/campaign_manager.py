from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QTextEdit, QLineEdit, QMessageBox
import json
import os

class CampaignManager(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.campaigns = {}
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.campaign_list = QListWidget()
        self.campaign_list.itemClicked.connect(self.load_campaign)

        self.new_campaign_input = QLineEdit('Enter new campaign name')
        self.create_campaign_button = QPushButton('Create Campaign')
        self.create_campaign_button.clicked.connect(self.create_campaign)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.campaign_list)
        left_layout.addWidget(self.new_campaign_input)
        left_layout.addWidget(self.create_campaign_button)

        self.campaign_details = QTextEdit()
        self.campaign_details.setReadOnly(True)

        layout.addLayout(left_layout)
        layout.addWidget(self.campaign_details)

        self.setLayout(layout)
        self.load_campaigns()

    def load_campaigns(self):
        save_file = 'saves/campaigns.json'
        if os.path.exists(save_file):
            with open(save_file, 'r') as file:
                self.campaigns = json.load(file)
                self.refresh_campaign_list()
        else:
            with open(save_file, 'w') as file:
                json.dump({}, file)

    def refresh_campaign_list(self):
        self.campaign_list.clear()
        for campaign_name in self.campaigns.keys():
            self.campaign_list.addItem(campaign_name)

    def create_campaign(self):
        campaign_name = self.new_campaign_input.text().strip()
        if campaign_name and campaign_name not in self.campaigns:
            campaign_data = {
                'name': campaign_name,
                'npcs': [],
                'encounters': [],
                'maps': [],
                'players': []
            }
            self.campaigns[campaign_name] = campaign_data
            self.save_campaigns()
            self.refresh_campaign_list()
        else:
            QMessageBox.warning(self, 'Error', 'Campaign already exists or name is invalid.')

    def save_campaigns(self):
        with open('saves/campaigns.json', 'w') as file:
            json.dump(self.campaigns, file, indent=4)
        self.refresh_campaign_list()

    def load_campaign(self, item):
        campaign_name = item.text()
        campaign_data = self.campaigns[campaign_name]

        if 'players' not in campaign_data:
            campaign_data['players'] = []

        self.campaign_details.setText(
            f"Campaign: {campaign_name}\n\nNPCs: {len(campaign_data['npcs'])}\nEncounters: {len(campaign_data['encounters'])}\nMaps: {len(campaign_data['maps'])}\nPlayers: {len(campaign_data['players'])}"
        )

        self.main_window.load_campaign_data(campaign_data)
