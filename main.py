import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTabWidget, \
    QGridLayout

from Layouts.dice_layout import DiceLayout


class ApplicationWindow(QtWidgets.QWidget):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.layout = QGridLayout()

        self.dice_layout = DiceLayout()
        tabwidget = QTabWidget()
        label2 = QLabel("Widget in Tab 2.")
        tabwidget.addTab(self.dice_tab(), "Dice")
        tabwidget.addTab(label2, "Manage Players")
        self.layout.addWidget(tabwidget, 0, 0)
        self.setLayout(self.layout)

    def dice_tab(self):
        """Create the General page UI."""
        dice_tab = QWidget()
        layout = DiceLayout()
        self.dice_layout = layout
        dice_tab.setLayout(layout)
        return dice_tab

    def manage_players_tab(self):
        pass


def main():
    app = QApplication([])
    window = ApplicationWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    sys.exit(main())
