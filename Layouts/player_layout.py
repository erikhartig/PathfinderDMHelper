from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, \
    QGridLayout, QTabWidget, QWidget, QListWidget

from Core.player import Player, SkillScore, get_all_players, get_all_items, get_ability_fields, get_skill_fields
from CustomObjects.lines import VLine
from Layouts.edit_grid_layout import stat_header_style, stat_layout_style, EditGridLayout
from Layouts.popup import Popup, create_qlines


class PlayerLayout(EditGridLayout):
    def __init__(self):
        super().__init__()
        self.players = get_all_players()
        menu_buttons = {
            "Create New Player": self.open_player_creation,
            "Edit Player": self.edit_player,
            "Delete Player": self.delete_player,
            "Add Item": self.add_item,
            "Remove Item": self.remove_item
        }
        self._create_menu_buttons(menu_buttons)
        self.player_tab_height = len(menu_buttons) + 1
        self.tabwidget = self.create_player_tabs()

    def create_player_tabs(self):
        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("""QTabBar::tab:selected{ background: DarkCyan }""")
        for player in self.players:
            tabwidget.addTab(self.player_tab(player), player.name)
        self.addWidget(tabwidget, 1, 1, self.player_tab_height, 4)
        return tabwidget

    def player_tab(self, player):
        player_tabs = QTabWidget()
        player_tabs.addTab(self._ability_and_skills_tab(player), "Abilities and Skills")
        player_tabs.addTab(self._item_tab(player), "Items")
        player_tabs.setTabPosition(QTabWidget.West)

        return player_tabs

    @staticmethod
    def _ability_and_skills_tab(player):
        stats_tab = QWidget()
        layout = QGridLayout()

        list_player_data(layout, player.get_ability_scores(), "Ability Scores", 0)
        layout.addWidget(VLine(color=QColor("White")), 1, 2, len(player.get_skill_scores().keys()), 1)
        list_player_data(layout, player.get_skill_scores(), "Skills", 3)

        stats_tab.setLayout(layout)
        return stats_tab

    @staticmethod
    def _item_tab(player):
        item_tab = QWidget()
        layout = QGridLayout()
        layout.setVerticalSpacing(10)
        layout.addWidget(stat_header_style("Name"), 0, 0, alignment=Qt.AlignTop)
        layout.addWidget(VLine(color=QColor("White")), 1, 1, len(player.items), 1)
        layout.addWidget(stat_header_style("Item Level"), 0, 2, alignment=Qt.AlignTop)
        layout.addWidget(VLine(color=QColor("White")), 1, 3, len(player.items), 1)
        layout.addWidget(stat_header_style("Gp Cost"), 0, 4, alignment=Qt.AlignTop)
        grid_index = 1
        for item in player.items:
            layout.addWidget(stat_layout_style(item.name), grid_index, 0, 10, 1, alignment=Qt.AlignTop)
            layout.addWidget(stat_layout_style(item.item_level), grid_index, 2, 10, 1, alignment=Qt.AlignTop)
            layout.addWidget(stat_layout_style(item.gp_cost), grid_index, 4, 10, 1, alignment=Qt.AlignTop)
            grid_index += 1
        item_tab.setLayout(layout)
        return item_tab

    def add_item(self):
        index = self.tabwidget.currentIndex()
        player = self.players[index]
        popup = AddItemPopup(player)
        popup.show()
        popup.exec()
        self._update_player_tabs()

    def remove_item(self):
        index = self.tabwidget.currentIndex()
        player = self.players[index]
        popup = RemoveItemPopup(player, player.items)
        popup.show()
        popup.exec()
        self._update_player_tabs()

    def delete_player(self):
        player = self.players[self.tabwidget.currentIndex()]
        player.delete()
        del self.players[self.tabwidget.currentIndex()]
        self._update_player_tabs()

    def edit_player(self):
        index = self.tabwidget.currentIndex()
        player = self.players[index]
        popup = EditPlayerPopup(player, index)
        popup.show()
        popup.exec()
        self._update_player_tabs()

    def open_player_creation(self):
        popup = PlayerCreationPopup()
        popup.show()
        popup.exec()
        self._update_player_tabs()

    def add_player(self, player):
        self.players.append(player)
        print(self.players)
        self._update_player_tabs()

    def _update_player_tabs(self):
        self.tabwidget.close()
        self.tabwidget = self.create_player_tabs()


class PlayerCreationPopup(Popup):
    def __init__(self):
        """
        """
        self.name_line_edit = QLineEdit()
        self.abilities = get_ability_fields()
        self.ability_line_edits = create_qlines(self.abilities)

        self.skills = get_skill_fields()
        self.skill_line_edits = create_qlines(self.skills)
        super().__init__("Create Player")

    def get_info(self):
        Player(self.name_line_edit.text(), *self._get_skills(), *self._get_ability_scores())
        self.close()

    def _get_ability_scores(self):
        values = [int(ability.text()) for ability in self.ability_line_edits.values() if ability.text()]
        return values

    def _get_skills(self):
        values = [SkillScore(int(ability.text())) for ability in self.skill_line_edits.values() if ability.text()]
        return values

    def create_form(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Name"), self.name_line_edit)
        for field in self.abilities:
            layout.addRow(QLabel(field.capitalize()), self.ability_line_edits[field])
        for field in self.skills:
            layout.addRow(QLabel(field.capitalize()), self.skill_line_edits[field])
        self.form_group_box.setLayout(layout)


class EditPlayerPopup(PlayerCreationPopup):
    def __init__(self, player, index):
        super().__init__()
        self.player = player
        self.index = index
        self.name_line_edit.setText(player.name)
        for name, line_edit in self.ability_line_edits.items():
            line_edit.setText(str(getattr(player, name)))
        for name, line_edit in self.skill_line_edits.items():
            line_edit.setText(str(getattr(player, name)))

    def get_info(self):
        self.player.name = self.name_line_edit.text()
        for name, line_edit in self.ability_line_edits.items():
            setattr(self.player, name, line_edit.text())
        for name, line_edit in self.skill_line_edits.items():
            setattr(self.player, name, line_edit.text())
        self.player.save()
        self.close()


class AddItemPopup(Popup):
    def __init__(self, player):
        """
        """
        self.player = player
        super().__init__("Add Item")
        self.selected_item = None

    def get_info(self):
        if self.selected_item:
            self.player.add_item(self.selected_item)
        self.close()

    def create_form(self):
        layout = QGridLayout()
        list_widget = QListWidget()
        list_widget.itemClicked.connect(self.add_item)
        for item in get_all_items():
            if not item.player:
                list_widget.addItem(item.name)
        layout.addWidget(list_widget, 0, 0)
        self.form_group_box.setLayout(layout)

    def add_item(self, item_selected):
        for item in get_all_items():
            if item.name == item_selected.text():
                self.selected_item = item
                return


class RemoveItemPopup(Popup):
    def __init__(self, player, items):
        """
        """
        self.player = player
        self.items = items
        super().__init__("Remove Item")
        self.selected_item = None

    def get_info(self):
        if self.selected_item:
            self.player.remove_item(self.selected_item)
        self.close()

    def create_form(self):
        layout = QGridLayout()
        list_widget = QListWidget()
        list_widget.itemClicked.connect(self.add_item)
        for item in self.items:
            list_widget.addItem(item.name)
        layout.addWidget(list_widget, 0, 0)
        self.form_group_box.setLayout(layout)

    def add_item(self, item_selected):
        for item in self.items:
            if item.name == item_selected.text():
                self.selected_item = item
                return


def list_player_data(layout, data, name, start_position):
    data_title = stat_header_style(name)
    layout.addWidget(data_title, 0, start_position)
    grid_num = 1
    for data_name, data_value in data.items():
        data_label = stat_layout_style(data_name.capitalize())
        layout.addWidget(data_label, grid_num, start_position)
        value_label = stat_layout_style(data_value)
        layout.addWidget(value_label, grid_num, start_position + 1)
        grid_num += 1
