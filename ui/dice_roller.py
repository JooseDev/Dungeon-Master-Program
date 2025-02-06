from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
import random

class DiceRoller(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        
        self.dice_dropdown = QComboBox()
        self.dice_dropdown.addItems(["d4", "d6", "d8", "d10", "d12", "d20", "d100"])
        
        self.roll_button = QPushButton("Roll Dice")
        self.roll_button.clicked.connect(self.roll_dice)
        
        self.result_label = QLabel("Select a dice and roll")
        
        top_layout.addWidget(self.dice_dropdown)
        top_layout.addWidget(self.roll_button)
        
        layout.addLayout(top_layout)
        layout.addWidget(self.result_label)
        
        self.setLayout(layout)

    def roll_dice(self):
        dice = self.dice_dropdown.currentText()
        sides = int(dice[1:])
        result = random.randint(1, sides)
        self.result_label.setText(f"Rolled a {dice}: {result}")