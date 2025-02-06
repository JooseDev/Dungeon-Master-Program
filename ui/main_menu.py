from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QWidget, QStackedWidget
from ui.campaign_manager import CampaignManager
from ui.npc_generator import NPCGenerator
from ui.encounter_tracker import EncounterTracker
from ui.map_viewer import MapViewer
from ui.player_manager import PlayerManager
from ui.enemy_manager import EnemyManager
from ui.dice_roller import DiceRoller

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('D&D DM Manager')
        self.setGeometry(100, 100, 800, 600)

        self.stacked_widget = QStackedWidget()

        self.campaign_manager = CampaignManager(self)
        self.npc_generator = NPCGenerator(self)
        self.player_manager = PlayerManager(self)
        self.encounter_tracker = EncounterTracker(self)
        self.map_viewer = MapViewer(self)
        self.enemy_manager = EnemyManager(self)
        self.dice_roller = DiceRoller()

        self.stacked_widget.addWidget(self.campaign_manager)
        self.stacked_widget.addWidget(self.npc_generator)
        self.stacked_widget.addWidget(self.player_manager)
        self.stacked_widget.addWidget(self.encounter_tracker)
        self.stacked_widget.addWidget(self.map_viewer)
        self.stacked_widget.addWidget(self.enemy_manager)

        button_layout = QHBoxLayout()
        self.start_campaign_button = QPushButton('Start Campaign')
        self.manage_npcs_button = QPushButton('Manage NPCs')
        self.manage_players_button = QPushButton('Manage Players')
        self.track_encounters_button = QPushButton('Track Encounters')
        self.view_maps_button = QPushButton('View Maps')
        self.manage_enemies_button = QPushButton('Manage Enemies')
        self.roll_dice_button = QPushButton('Roll Dice')

        self.start_campaign_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.campaign_manager))
        self.manage_npcs_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.npc_generator))
        self.manage_players_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.player_manager))
        self.track_encounters_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.encounter_tracker))
        self.view_maps_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.map_viewer))
        self.manage_enemies_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.enemy_manager))
        self.roll_dice_button.clicked.connect(self.open_dice_roller)

        button_layout.addWidget(self.start_campaign_button)
        button_layout.addWidget(self.manage_npcs_button)
        button_layout.addWidget(self.manage_players_button)
        button_layout.addWidget(self.track_encounters_button)
        button_layout.addWidget(self.view_maps_button)
        button_layout.addWidget(self.manage_enemies_button)
        button_layout.addWidget(self.roll_dice_button)

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.addLayout(button_layout)
        container_layout.addWidget(self.stacked_widget)
        container.setLayout(container_layout)

        self.setCentralWidget(container)

    def open_dice_roller(self):
        self.dice_roller.show()

    def load_campaign_data(self, campaign_data):
        self.npc_generator.load_data(campaign_data['npcs'])
        self.player_manager.load_data(campaign_data['players'])
        self.encounter_tracker.load_data(campaign_data['encounters'])
        self.map_viewer.load_data(campaign_data['maps'])