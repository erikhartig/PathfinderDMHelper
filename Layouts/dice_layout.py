from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout

from Core import roll_dice


class DiceLayout(QVBoxLayout):
    def __init__(self):
        super(DiceLayout, self).__init__()
        title = QLabel("Dice")
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignCenter)
        self.addWidget(title)
        self._add_buttons()
        self.dice_result = None

    def _add_buttons(self):
        buttons = []
        buttons.append(button_dice_style(QPushButton('d100')))
        buttons[-1].clicked.connect(self._roll_d100)

        buttons.append(button_dice_style(QPushButton('d20')))
        buttons[-1].clicked.connect(self._roll_d20)

        buttons.append(button_dice_style(QPushButton('d10')))
        buttons[-1].clicked.connect(self._roll_d10)

        buttons.append(button_dice_style(QPushButton('d8')))
        buttons[-1].clicked.connect(self._roll_d8)

        buttons.append(button_dice_style(QPushButton('d6')))
        buttons[-1].clicked.connect(self._roll_d6)

        buttons.append(button_dice_style(QPushButton('d4')))
        buttons[-1].clicked.connect(self._roll_d4)

        for button in buttons:
            button.show()
            self.addWidget(button, alignment=Qt.AlignCenter)

    def _roll_d100(self):
        self._update_dice_result(roll_dice.roll_d100())

    def _roll_d20(self):
        self._update_dice_result(roll_dice.roll_d20())

    def _roll_d10(self):
        self._update_dice_result(roll_dice.roll_d10())

    def _roll_d8(self):
        self._update_dice_result(roll_dice.roll_d8())

    def _roll_d6(self):
        self._update_dice_result(roll_dice.roll_d6())

    def _roll_d4(self):
        self._update_dice_result(roll_dice.roll_d4())

    def _update_dice_result(self, value):
        new_result = QLabel(str(value))
        new_result.setAlignment(Qt.AlignCenter)
        new_result.setFont(QFont('Arial', 15))
        if not self.dice_result:
            self.dice_result = new_result
            self.dice_result.show()
            self.addWidget(self.dice_result)
        else:
            self.replaceWidget(self.dice_result, new_result)
            self.dice_result.close()
            self.update()
            self.dice_result = new_result


def button_dice_style(button):
    button.setMinimumWidth(80)
    return button
