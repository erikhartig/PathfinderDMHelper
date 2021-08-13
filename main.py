import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, \
    QGridLayout

from Core.manage_data import DataStore
from Layouts.dice_layout import DiceLayout
from Layouts.item_layout import ItemLayout
from Layouts.player_layout import PlayerLayout


class ApplicationWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.data_store = DataStore()

        tabwidget = QTabWidget()
        tabwidget.addTab(self.dice_tab(), "Dice")
        tabwidget.addTab(self.manage_players_tab(), "Manage Players")
        tabwidget.addTab(self.manage_items_tab(), "Manage Items")
        self.layout.addWidget(tabwidget, 0, 0)
        self.setLayout(self.layout)

    @staticmethod
    def dice_tab():
        """Create the General page UI."""
        dice_tab = QWidget()
        layout = DiceLayout()
        dice_tab.setLayout(layout)
        return dice_tab

    def manage_players_tab(self):
        manage_players_tab = QWidget()
        layout = PlayerLayout(self.data_store)
        manage_players_tab.setLayout(layout)
        return manage_players_tab

    def manage_items_tab(self):
        manage_items_tab = QWidget()
        layout = ItemLayout(self.data_store)
        manage_items_tab.setLayout(layout)
        return manage_items_tab


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
