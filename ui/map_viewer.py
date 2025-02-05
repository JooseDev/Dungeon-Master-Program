from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QFileDialog, QSpinBox, QSizePolicy
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt
import os

class MapViewer(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.maps = []
        self.current_map = None
        self.grid_rows = 10
        self.grid_cols = 10
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.map_list = QListWidget()
        self.map_list.itemClicked.connect(self.display_map)

        self.map_display = QLabel('Select a map to view')
        self.map_display.setAlignment(Qt.AlignCenter)
        self.map_display.setStyleSheet("border: 1px solid black;")
        self.map_display.setScaledContents(True)
        self.map_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.add_map_button = QPushButton('Add Map')
        self.add_map_button.clicked.connect(self.add_map)

        self.grid_rows_input = QSpinBox()
        self.grid_rows_input.setRange(1, 50)
        self.grid_rows_input.setValue(self.grid_rows)
        self.grid_rows_input.setPrefix("Rows: ")

        self.grid_cols_input = QSpinBox()
        self.grid_cols_input.setRange(1, 50)
        self.grid_cols_input.setValue(self.grid_cols)
        self.grid_cols_input.setPrefix("Cols: ")

        self.update_grid_button = QPushButton('Update Grid')
        self.update_grid_button.clicked.connect(self.update_grid)

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.map_list)
        left_layout.addWidget(self.add_map_button)
        left_layout.addWidget(self.grid_rows_input)
        left_layout.addWidget(self.grid_cols_input)
        left_layout.addWidget(self.update_grid_button)

        layout.addLayout(left_layout)
        layout.addWidget(self.map_display, stretch=1)

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
        self.current_map = QPixmap(map_path)
        self.draw_grid()

    def draw_grid(self):
        if self.current_map is not None:
            display_size = self.map_display.size()
            grid_map = self.current_map.scaled(display_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Prevent scaling loop by checking if scaling exceeds display size
            if grid_map.size().width() > display_size.width() or grid_map.size().height() > display_size.height():
                grid_map = self.current_map.scaled(display_size.width(), display_size.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            painter = QPainter(grid_map)
            pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)
            painter.setPen(pen)

            width = grid_map.width()
            height = grid_map.height()

            cell_width = width / self.grid_cols
            cell_height = height / self.grid_rows

            for col in range(1, self.grid_cols):
                x = int(col * cell_width)
                painter.drawLine(x, 0, x, height)

            for row in range(1, self.grid_rows):
                y = int(row * cell_height)
                painter.drawLine(0, y, width, y)

            painter.end()
            self.map_display.setPixmap(grid_map)
        else:
            self.map_display.setText('No map selected.')

    def resizeEvent(self, event):
        self.draw_grid()
        super().resizeEvent(event)

    def update_grid(self):
        self.grid_rows = self.grid_rows_input.value()
        self.grid_cols = self.grid_cols_input.value()
        self.draw_grid()

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