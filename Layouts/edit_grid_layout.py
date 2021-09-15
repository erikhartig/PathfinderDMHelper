from PyQt5.QtWidgets import QGridLayout, QPushButton

from Style.button_styles import button_manage_player_style


class EditGridLayout(QGridLayout):
    def _create_menu_buttons(self, menu_buttons):
        button_index = 1
        for name, func in menu_buttons.items():
            button = button_manage_player_style(QPushButton(name))
            button.clicked.connect(func)
            button.show()
            self.addWidget(button, button_index, 0, 1, 1)
            button_index += 1
