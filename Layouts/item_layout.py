import atexit
import pickle

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QFormLayout, QDialogButtonBox, QLineEdit, \
    QGroupBox, QDialog, QGridLayout, QTabWidget, QWidget

from Core.item import Item
from paths import ITEMS


class ItemLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.items = self.load_items()
        self.tabwidget = self.create_item_tabs()
        self.addWidget(self.tabwidget, 1, 1, 4, 4)

        title = QLabel("Items")
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignCenter)
        self.addWidget(title, 0, 1)
        self._add_create_item()
        self._add_edit_item()
        self._add_delete_item()
        atexit.register(self.save_items)

    def create_item_tabs(self):
        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("""QTabBar::tab:selected{ background: DarkCyan }""")
        for item in self.items:
            tabwidget.addTab(self.item_tab(item), item.name)
        self.addWidget(tabwidget, 1, 1, 4, 4)
        return tabwidget

    @staticmethod
    def item_tab(item):
        item_tab = QWidget()
        layout = QGridLayout()

        stat_label = stat_header_style("Ability Scores")
        layout.addWidget(stat_label, 0, 0)
        grid_num = 1
        for ability in vars(item.ability_scores):
            pass

        item_tab.setLayout(layout)
        return item_tab

    def _add_create_item(self):
        button = button_manage_item_style(QPushButton('Create New item'))
        button.clicked.connect(self.open_item_creation)
        button.show()
        self.addWidget(button, 1, 0, 1, 1)

    def _add_edit_item(self):
        button = button_manage_item_style(QPushButton('Edit item'))
        button.clicked.connect(self.edit_item)
        button.show()
        self.addWidget(button, 2, 0, 1, 1)

    def _add_delete_item(self):
        button = button_manage_item_style(QPushButton('Delete item'))
        button.clicked.connect(self.delete_item)
        button.show()
        self.addWidget(button, 3, 0, 1, 1)

    def delete_item(self):
        del self.items[self.tabwidget.currentIndex()]
        self._update_item_tabs()

    def edit_item(self):
        index = self.tabwidget.currentIndex()
        item = self.items[index]
        popup = EditItemPopup(self, item, index)
        popup.show()
        popup.exec()
        self._update_item_tabs()

    def open_item_creation(self):
        popup = ItemCreationPopup(self)
        popup.show()
        popup.exec()

    def add_item(self, item):
        self.items.append(item)
        print(self.items)
        self._update_item_tabs()

    def _update_item_tabs(self):
        self.tabwidget.close()
        self.tabwidget = self.create_item_tabs()
        self.addWidget(self.tabwidget, 1, 1, 4, 4)

    def save_items(self):
        with open(ITEMS, 'wb') as item_file:
            pickle.dump(self.items, item_file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_items():
        if not ITEMS.exists():
            return []
        with open(ITEMS, 'rb') as item_file:
            items = pickle.load(item_file)
        return items


class ItemCreationPopup(QDialog):
    def __init__(self, parent):
        """
        Args:
            parent (itemLayout):
        """
        super().__init__()
        self.setWindowTitle("Create item")
        self.item = None
        self.setGeometry(100, 100, 300, 400)
        self.form_group_box = QGroupBox("")
        self.parent = parent
        # creating a line edit
        self.name_line_edit = QLineEdit()
        # calling the method that create the form
        self.create_form()

        # creating a dialog button for ok and cancel
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.get_info)
        self.button_box.rejected.connect(self.reject)

        # creating a vertical layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(self.button_box)

        # setting lay out
        self.setLayout(main_layout)

    def get_info(self):
        # printing the form information
        print("Person Name : {0}".format(self.name_line_edit.text()))
        item = Item(self.name_line_edit.text(), self._get_ability_scores(), self._get_skills())
        # closing the window
        self.parent.add_item(item)
        self.close()


    def create_form(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Name"), self.name_line_edit)
        for ability in self.abilities:
            layout.addRow(QLabel(ability.capitalize()), self.ability_line_edits[ability])
        for skill in self.skills:
            layout.addRow(QLabel(skill.capitalize()), self.skill_line_edits[skill])
        self.form_group_box.setLayout(layout)


class EditItemPopup(ItemCreationPopup):
    def __init__(self, parent, item, index):
        super().__init__(parent)
        self.item = item
        self.index = index
        self.name_line_edit.setText(item.name)
        for name, line_edit in self.ability_line_edits.items():
            line_edit.setText(str(getattr(item.ability_scores, name)()))
        for name, line_edit in self.skill_line_edits.items():
            line_edit.setText(str(getattr(item.skills, name)()))

    def get_info(self):
        self.parent.items[self.index].ability_scores = self._get_ability_scores()
        self.close()


def stat_layout_style(value):
    label = QLabel(str(value))
    label.setFont(QFont('Arial', 13))
    label.show()
    return label


def stat_header_style(value):
    label = QLabel(str(value))
    header_font = QFont('Arial', 16)
    header_font.setBold(True)
    label.setFont(header_font)
    label.show()
    return label


def button_manage_item_style(button):
    button.setMinimumWidth(150)
    return button
