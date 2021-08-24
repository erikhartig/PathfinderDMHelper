import math

from PyQt5.QtCore import Qt, QStringListModel
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFormLayout, QGridLayout, QTabWidget, QWidget, QCompleter, QLineEdit

from Core.player import Item, get_all_items
from Core.scrape import get_item_names, request_item_data
from CustomObjects.lines import VLine
from Layouts.edit_grid_layout import stat_layout_style, EditGridLayout
from Layouts.popup import Popup, get_field_names, create_qlines


class ItemLayout(EditGridLayout):
    def __init__(self):
        super().__init__()
        self.items = get_all_items()
        self.tabwidget = self.create_item_tabs()
        self.setRowStretch(1, 10)
        menu_buttons = {
            "Create New Item": self.open_item_creation,
            "Import Item": self.import_item,
            "Edit Item": self.edit_item,
            "Delete Item": self.delete_item,
        }
        self._create_menu_buttons(menu_buttons)

    def create_item_tabs(self):
        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("""QTabBar::tab:selected{ background: DarkCyan }""")
        for item in self.items:
            tabwidget.addTab(self.item_tab(item), item.name)
        tabwidget.setMaximumHeight(700)
        self.addWidget(tabwidget, 1, 1, 5, 1, alignment=Qt.AlignTop)
        return tabwidget

    @staticmethod
    def item_tab(item):
        item_tab = QWidget()
        layout = QGridLayout()
        layout.setVerticalSpacing(10)
        layout.setColumnStretch(2, 4)
        fields = [field for field in vars(item) if getattr(item, field) and field not in ["name", "_player"]]
        layout.addWidget(VLine(color=QColor("White")), 0, 1, len(fields), 1)
        grid_num = 0
        for item_field in fields:
            stat_value = getattr(item, item_field)
            stat_label = stat_layout_style(clean_field_name(item_field))
            layout.addWidget(stat_label, grid_num, 0)

            value_label = stat_layout_style(stat_value)
            layout.addWidget(value_label, grid_num, 2)
            layout.setRowStretch(grid_num, 2 + math.ceil(math.log(len(str(stat_value)))))
            grid_num += 1

        item_tab.setLayout(layout)
        return item_tab

    def delete_item(self):
        del self.items[self.tabwidget.currentIndex()]
        self._update_item_tabs()

    def import_item(self):
        popup = ItemImportPopup(self)
        popup.show()
        popup.exec()

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
        self._update_item_tabs()

    def _update_item_tabs(self):
        self.tabwidget.close()
        self.tabwidget = self.create_item_tabs()


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


class ItemImportPopup(Popup):
    def __init__(self, parent):
        """
        Args:
            parent (itemLayout):
        """
        self.item_line_edit = None
        self.item_names = get_item_names()
        super().__init__("Import Item", parent)

    def get_info(self):
        if self.item_line_edit.text() in self.item_names:
            item_id = self.item_names[self.item_line_edit.text()]
            if len([item for item in self.item_names.values() if item == item_id]) > 1:
                response = request_item_data(int(item_id), self.item_line_edit.text())
            else:
                response = request_item_data(int(item_id))
            item = Item(**response)
            self.parent.add_item(item)
        self.close()

    def _get_item_values(self):
        return [item.text() for item in self.item_line_edits.values()]

    def create_form(self):
        model = QStringListModel()
        model.setStringList(self.item_names)

        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.item_line_edit = QLineEdit()
        self.item_line_edit.setCompleter(completer)
        self.item_line_edit.show()
        layout = QFormLayout()
        layout.addRow(self.item_line_edit)
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


def clean_field_name(value):
    value = value.replace("_", " ")
    return value.title()
