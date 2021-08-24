from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton


class EditGridLayout(QGridLayout):
    def _create_menu_buttons(self, menu_buttons):
        button_index = 1
        for name, func in menu_buttons.items():
            button = button_manage_player_style(QPushButton(name))
            button.clicked.connect(func)
            button.show()
            self.addWidget(button, button_index, 0, 1, 1)
            button_index += 1


def stat_layout_style(value):
    label = QLabel(str(value))
    label.setFont(QFont('Arial', 13))
    label.setWordWrap(True)
    label.show()
    return label


def stat_header_style(value):
    label = QLabel(str(value))
    header_font = QFont('Arial', 16)
    header_font.setBold(True)
    label.setFont(header_font)
    label.show()
    return label


def button_manage_player_style(button):
    button.setMinimumWidth(150)
    return button
