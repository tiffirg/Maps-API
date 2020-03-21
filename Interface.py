from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QLabel, QAction, QTextBrowser
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QComboBox, QGroupBox, QHBoxLayout, QRadioButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PlaceSearch import get_response_about_place, get_coordinates_place
import requests
from io import BytesIO
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"


class Interface_API(QWidget):
    def __init__(self):
        super().__init__()
        self.size_map = 650, 450
        self.address = None
        self.toponym_to_find = ''
        self.toponym_coordinates = None
        self.mode_address = True
        self.now_mode = 'Схема'
        self.modes = {'Схема': 'map', 'Спутник': 'sat', 'Гибрид': 'sat,skl'}
        self.layout = QHBoxLayout(self)
        self.map_image = QLabel(self)
        self.search_edit = QLineEdit(self)
        self.box_modes = QComboBox(self)
        self.box_interface = QGroupBox(self)
        self.search_btn = QPushButton("Найти", self)
        self.reset_btn = QPushButton("Сбросить", self)
        self.address_btn = QRadioButton("Отображение\nпочтового индекса", self)
        self.address_text = QTextBrowser(self)
        self.layout_interface = QGridLayout(self)
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
            self.search_toponym()
        elif event.button() == 2:  # правая
            pass

    def initUI(self):
        self.reset_address()
        self.box_modes.addItems(self.modes)
        self.map_image.setPixmap(QPixmap("map.png").scaled(1000, 1000, Qt.KeepAspectRatio))
        self.box_interface.setMaximumWidth(200)
        self.layout.addWidget(self.map_image)
        self.layout.addWidget(self.box_interface)
        self.box_interface.setLayout(self.layout_interface)
        self.layout_interface.addWidget(self.box_modes, 0, 0, 1, 1)
        self.layout_interface.addWidget(self.address_btn, 0, 1, 1, 2)
        self.layout_interface.addWidget(self.search_edit, 1, 0, 1, 2)
        self.layout_interface.addWidget(self.search_btn, 1, 2, 1, 1)
        self.layout_interface.addWidget(self.reset_btn, 2, 0, 1, 1)
        self.layout_interface.addWidget(self.address_text, 3, 0, 1, 3)

        self.box_modes.activated[str].connect(self.change_mode)
        self.search_btn.clicked.connect(self.search_toponym)

        self.address_btn.setChecked(True)
        self.address_btn.toggled.connect(self.set_mode_text_address)

        self.reset_btn.clicked.connect(self.reset_search)

    def reset_address(self):
        self.address = {"Страна": '', "Город": '', "Улица": '', "Дом": '', "Почтовый индекс": ''}

    def change_mode(self, mode):
        self.now_mode = mode
        if self.toponym_to_find == '':
            self.set_map(pt=None)
        else:
            self.set_map()

    def search_toponym(self):
        new_toponym = self.search_edit.text()
        if new_toponym == '' or new_toponym == self.toponym_to_find:
            return
        self.toponym_to_find = new_toponym
        json_response = get_response_about_place(self.toponym_to_find).json()
        string = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]
        try:
            postal_code = string["Address"]["postal_code"]
        except KeyError:
            postal_code = ''
        address = string["text"].split(", ") + [postal_code]
        for key, value in zip(self.address, address):
            self.address[key] = value
        self.toponym_coordinates = get_coordinates_place(json_response)
        self.set_map()

    def set_map(self, spn=(0.01, 0.01), pt='pm2dgl'):
        if self.toponym_coordinates is None:
            return
        toponym_longitude, toponym_lattitude = self.toponym_coordinates
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": '{},{}'.format(*spn),
            "l": self.modes[self.now_mode],
            "size": '{},{}'.format(*self.size_map)
        }
        if pt is not None:
            map_params["pt"] = ",".join([toponym_longitude, toponym_lattitude, 'pm2dgl'])
        response = requests.get(MAP_API_SERVER, params=map_params)
        pixmap = QPixmap()
        pixmap.loadFromData(BytesIO(response.content).getvalue())
        self.map_image.setPixmap(pixmap)
        self.set_text_address()

    def set_mode_text_address(self, value):
        self.mode_address = value
        self.set_text_address()

    def set_text_address(self):
        keys = list(self.address.keys())
        if not self.mode_address:
            keys = keys[:-1]
        self.address_text.setText('\n\n'.join('{} - {}'.format(key, self.address[key]) for key in keys if self.address[key] != ''))

    def reset_search(self):
        self.set_map(pt=None)
        self.search_edit.setText('')
        self.address_text.setText('')
        self.toponym_to_find = ''
        self.reset_address()





