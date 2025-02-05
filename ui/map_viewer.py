from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap
import os

class MapViewer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.maps = []
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.map_list = QListWidget()
        self.map_list.itemClicked.connect(self.display_map)

        self.map_display = QLabel('Select a map to view')
        self.map_display.setFixedSize(600, 400)
        self.map_display.setStyleSheet("border: 1px solid black;")
        self.map_display.setScaledContents(True)

        self.add_map_button = QPushButton('Add Map')
        self.add_map_button.clicked.connect(self.add_map)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.map_list)
        left_layout.addWidget(self.add_map_button)

        layout.addLayout(left_layout)
        layout.addWidget(self.map_display)

        self.setLayout(layout)
        self.load_maps()

    def load_data(self, maps):
        self.maps = maps
        self.load_maps()

    def load_maps(self):
        self.map_list.clear()
        maps_folder = 'assets/maps'
        if os.path.exists(maps_folder):
            for map_file in os.listdir(maps_folder):
                if map_file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                    self.map_list.addItem(map_file)
        else:
            os.makedirs(maps_folder)

    def display_map(self, item):
        map_name = item.text()
        map_path = os.path.join('assets/maps', map_name)
        pixmap = QPixmap(map_path)
        if not pixmap.isNull():
            self.map_display.setPixmap(pixmap)
        else:
            self.map_display.setText('Failed to load map.')

    def add_map(self):
        file_dialog = QFileDialog()
        map_file, _ = file_dialog.getOpenFileName(self, 'Open Map', '', 'Image Files (*.png *.jpg *.jpeg *.bmp *.gif)')
        if map_file:
            maps_folder = 'assets/maps'
            if not os.path.exists(maps_folder):
                os.makedirs(maps_folder)
            
            new_map_path = os.path.join(maps_folder, os.path.basename(map_file))
            if not os.path.exists(new_map_path):
                with open(map_file, 'rb') as src_file:
                    with open(new_map_path, 'wb') as dest_file:
                        dest_file.write(src_file.read())
                self.load_maps()
