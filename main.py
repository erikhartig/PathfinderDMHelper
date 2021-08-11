import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, \
    QGridLayout

from Layouts.dice_layout import DiceLayout
from Layouts.player_layout import PlayerLayout


class ApplicationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()

        tabwidget = QTabWidget()
        tabwidget.addTab(self.dice_tab(), "Dice")
        tabwidget.addTab(self.manage_players_tab(), "Manage Players")
        self.layout.addWidget(tabwidget, 0, 0)
        self.setLayout(self.layout)

    @staticmethod
    def dice_tab():
        """Create the General page UI."""
        dice_tab = QWidget()
        layout = DiceLayout()
        dice_tab.setLayout(layout)
        return dice_tab

    @staticmethod
    def manage_players_tab():
        dice_tab = QWidget()
        layout = PlayerLayout()
        dice_tab.setLayout(layout)
        return dice_tab


def main():
    app = QApplication([])
    window = ApplicationWindow()
    window.show()
    try:
        app.exec()
    except BaseException as error:
        print(error)
        raise error

if __name__ == "__main__":
    sys.exit(main())
