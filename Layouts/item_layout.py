import atexit
import math

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QLabel, QPushButton, QFormLayout, QGridLayout, QTabWidget, QWidget

from Core.item import Item
from Core.manage_data import load_items, save_items
from CustomObjects.lines import VLine
from Layouts.popup import Popup, get_field_names, create_qlines


class ItemLayout(QGridLayout):
    def __init__(self, data_store):
        super().__init__()
        self.data_store = data_store
        self.data_store.items = load_items()
        self.tabwidget = self.create_item_tabs()
        self.setRowStretch(1, 10)
        self._add_create_item()
        self._add_edit_item()
        self._add_delete_item()
        atexit.register(self.save_items)

    def create_item_tabs(self):
        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("""QTabBar::tab:selected{ background: DarkCyan }""")
        for item in self.data_store.items:
            tabwidget.addTab(self.item_tab(item), item.name)
        tabwidget.setMaximumHeight(700)
        self.addWidget(tabwidget, 1, 1, 4, 1, alignment=Qt.AlignTop)
        return tabwidget

    @staticmethod
    def item_tab(item):
        item_tab = QWidget()
        layout = QGridLayout()
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(2, 4)
        layout.addWidget(VLine(color=QColor("White")), 0, 1, len(vars(item)) - 1, 1)
        grid_num = 0
        for item_field in vars(item):
            if item_field in ["name", "_player"]:
                continue
            stat_value = getattr(item, item_field)
            stat_label = stat_layout_style(clean_field_name(item_field))
            layout.addWidget(stat_label, grid_num, 0)

            value_label = stat_layout_style(stat_value)
            layout.addWidget(value_label, grid_num, 2)
            layout.setRowStretch(grid_num, 2 + math.ceil(math.log(len(stat_value))))
            grid_num += 1

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
        del self.data_store.items[self.tabwidget.currentIndex()]
        self._update_item_tabs()

    def edit_item(self):
        index = self.tabwidget.currentIndex()
        item = self.data_store.items[index]
        popup = EditItemPopup(self, item, index)
        popup.show()
        popup.exec()
        self._update_item_tabs()

    def open_item_creation(self):
        popup = ItemCreationPopup(self)
        popup.show()
        popup.exec()

    def add_item(self, item):
        self.data_store.items.append(item)
        self._update_item_tabs()

    def _update_item_tabs(self):
        self.tabwidget.close()
        self.tabwidget = self.create_item_tabs()

    def save_items(self):
        save_items(self.data_store.items)


class ItemCreationPopup(Popup):
    def __init__(self, parent):
        """
        Args:
            parent (itemLayout):
        """
        self.item_fields = get_field_names(Item)
        self.item_fields.remove("_player")
        self.item_line_edits = create_qlines(self.item_fields)
        super().__init__("Create Item", parent)

    def get_info(self):
        item = Item(*self._get_item_values())
        self.parent.add_item(item)
        self.close()

    def _get_item_values(self):
        return [item.text() for item in self.item_line_edits.values()]

    def create_form(self):
        layout = QFormLayout()
        for item_field in self.item_fields:
            layout.addRow(QLabel(clean_field_name(item_field)), self.item_line_edits[item_field])
        self.form_group_box.setLayout(layout)


class EditItemPopup(ItemCreationPopup):
    def __init__(self, parent, item, index):
        super().__init__(parent)
        self.item = item
        self.index = index
        for name, line_edit in self.item_line_edits.items():
            line_edit.setText(str(getattr(item, name)))

    def get_info(self):
        self.parent.items[self.index] = Item(*self._get_item_values())
        self.close()


def stat_layout_style(value):
    label = QLabel(str(value))
    label.setFont(QFont('Arial', 13))
    label.setAlignment(Qt.AlignTop)
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


def button_manage_item_style(button):
    button.setMinimumWidth(150)
    return button


def clean_field_name(value):
    value = value.replace("_", " ")
    return value.title()
