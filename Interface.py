from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QLabel, QAction, QTextBrowser
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QComboBox, QGroupBox, QHBoxLayout, QRadioButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class Interface_API(QWidget):
    def __init__(self):
        super().__init__()
        self.search = ''
        self.now_mode = 'Схема'
        self.modes = ['Схема', 'Спутник', 'Гибрид']
        self.layout = QHBoxLayout(self)
        self.map_image = QLabel(self)
        self.search_edit = QLineEdit(self)
        self.box_modes = QComboBox(self)
        self.box_interface = QGroupBox(self)
        self.box_map = QGroupBox(self)
        self.search_btn = QPushButton("Найти", self)
        self.reset_btn = QPushButton("Сбросить", self)
        self.address_btn = QRadioButton("Отображение\nпочтового индекса", self)
        self.address_text = QTextBrowser(self)
        self.layout_interface = QGridLayout(self)
        self.layout_map = QVBoxLayout(self)
        self.initUI()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            pass  # Увеличиваем масштаб
        elif event.key() == Qt.Key_PageDown:
            pass  # Уменьшаем масштаб
        elif event.key() == Qt.Key_Up:
            pass  # Двгаем вверх
        elif event.key() == Qt.Key_Down:
            pass  # Двигаем вниз
        elif event.key() == Qt.Key_Right:
            pass  # Двигаем вправо
        elif event.key() == Qt.Key_Left:
            pass  # Двигаем влево

    def mousePressEvent(self, event):
        if event.button() == 1:  # левая
            self.set_address()
        elif event.button() == 2:  # правая
            pass

    def initUI(self):
        self.layout_map.addWidget(self.map_image)
        self.box_map.setLayout(self.layout_map)
        self.box_modes.addItems(self.modes)
        self.map_image.setPixmap(QPixmap("map.png").scaled(1000, 1000, Qt.KeepAspectRatio))
        self.box_interface.setMaximumWidth(300)
        self.layout.addWidget(self.box_map)
        self.layout.addWidget(self.box_interface)
        self.box_interface.setLayout(self.layout_interface)
        self.layout_interface.addWidget(self.box_modes, 0, 0, 1, 1)
        self.layout_interface.addWidget(self.address_btn, 0, 1, 1, 2)
        self.layout_interface.addWidget(self.search_edit, 1, 0, 1, 2)
        self.layout_interface.addWidget(self.search_btn, 1, 2, 1, 1)
        self.layout_interface.addWidget(self.reset_btn, 2, 0, 1, 1)
        self.layout_interface.addWidget(self.address_text, 3, 0, 1, 3)

        self.box_modes.activated[str].connect(self.change_mode)
        self.search_btn.clicked.connect(self.set_address)

    def change_mode(self, mode):
        self.now_mode = mode

    def set_address(self):
        self.search = self.search_edit.text()
        if self.search == '':
            return
        pass  # Запрос к API