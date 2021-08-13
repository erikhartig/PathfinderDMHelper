import atexit

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QFormLayout, QLineEdit, \
    QGridLayout, QTabWidget, QWidget, QListWidget

from Core.manage_data import save_players, load_players
from Core.player import Player, AbilityScores, AbilityScore, Skills, SkillScore
from Layouts.popup import Popup, get_field_names, create_qlines


class PlayerLayout(QGridLayout):
    def __init__(self, data_store):
        super().__init__()
        self.data_store = data_store
        self.data_store.players = load_players()
        self.tabwidget = self.create_player_tabs()

        self._add_create_player()
        self._add_edit_player()
        self._add_delete_player()
        self._add_item()
        atexit.register(self.save_players)

    def create_player_tabs(self):
        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("""QTabBar::tab:selected{ background: DarkCyan }""")
        for player in self.data_store.players:
            tabwidget.addTab(self.player_tab(player), player.name)
        self.addWidget(tabwidget, 1, 1, 5, 4)
        return tabwidget

    @staticmethod
    def player_tab(player):
        player_tab = QWidget()
        layout = QGridLayout()

        stat_label = stat_header_style("Ability Scores")
        layout.addWidget(stat_label, 0, 0)
        grid_num = 1
        for ability in vars(player.ability_scores):
            stat_value = getattr(player.ability_scores, ability)()
            stat_label = stat_layout_style(ability.capitalize())
            layout.addWidget(stat_label, grid_num, 0)
            value_label = stat_layout_style(stat_value)
            layout.addWidget(value_label, grid_num, 1)
            grid_num += 1

        stat_label = stat_header_style("Skills")
        layout.addWidget(stat_label, 0, 3)
        grid_num = 1
        for skill in vars(player.skills):
            value_label = stat_layout_style("|")
            layout.addWidget(value_label, grid_num, 2)
            stat_value = getattr(player.skills, skill)()
            stat_label = stat_layout_style(skill.capitalize())
            layout.addWidget(stat_label, grid_num, 3)
            value_label = stat_layout_style(stat_value)
            layout.addWidget(value_label, grid_num, 4)
            grid_num += 1

        player_tab.setLayout(layout)
        return player_tab

    def _add_create_player(self):
        button = button_manage_player_style(QPushButton('Create New Player'))
        button.clicked.connect(self.open_player_creation)
        button.show()
        self.addWidget(button, 1, 0, 1, 1)

    def _add_edit_player(self):
        button = button_manage_player_style(QPushButton('Edit Player'))
        button.clicked.connect(self.edit_player)
        button.show()
        self.addWidget(button, 2, 0, 1, 1)

    def _add_delete_player(self):
        button = button_manage_player_style(QPushButton('Delete Player'))
        button.clicked.connect(self.delete_player)
        button.show()
        self.addWidget(button, 3, 0, 1, 1)

    def _add_item(self):
        button = button_manage_player_style(QPushButton('Add Item'))
        button.clicked.connect(self.add_item)
        button.show()
        self.addWidget(button, 4, 0, 1, 1)

    def add_item(self):
        index = self.tabwidget.currentIndex()
        player = self.data_store.players[index]
        popup = AddItemPopup(self, player, self.data_store.items)
        popup.show()
        popup.exec()

    def delete_player(self):
        del self.data_store.players[self.tabwidget.currentIndex()]
        self._update_player_tabs()

    def edit_player(self):
        index = self.tabwidget.currentIndex()
        player = self.data_store.players[index]
        popup = EditPlayerPopup(self, player, index)
        popup.show()
        popup.exec()
        self._update_player_tabs()

    def open_player_creation(self):
        popup = PlayerCreationPopup(self)
        popup.show()
        popup.exec()

    def add_player(self, player):
        self.data_store.players.append(player)
        print(self.data_store.players)
        self._update_player_tabs()

    def _update_player_tabs(self):
        self.tabwidget.close()
        self.tabwidget = self.create_player_tabs()

    def save_players(self):
        save_players(self.data_store.players)


class PlayerCreationPopup(Popup):
    def __init__(self, parent):
        """
        Args:
            parent (PlayerLayout):
        """
        self.name_line_edit = QLineEdit()
        self.abilities = get_field_names(AbilityScores)
        self.ability_line_edits = create_qlines(self.abilities)

        self.skills = get_field_names(Skills)
        self.skill_line_edits = create_qlines(self.skills)
        super().__init__("Create Player", parent)

    def get_info(self):
        player = Player(self.name_line_edit.text(), self._get_ability_scores(), self._get_skills())
        self.parent.add_player(player)
        self.close()

    def _get_ability_scores(self):
        values = [AbilityScore(int(ability.text())) for ability in self.ability_line_edits.values()]
        return AbilityScores(*values)

    def _get_skills(self):
        values = [SkillScore(int(ability.text())) for ability in self.skill_line_edits.values()]
        return Skills(*values)

    def create_form(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Name"), self.name_line_edit)
        for ability in self.abilities:
            layout.addRow(QLabel(ability.capitalize()), self.ability_line_edits[ability])
        for skill in self.skills:
            layout.addRow(QLabel(skill.capitalize()), self.skill_line_edits[skill])
        self.form_group_box.setLayout(layout)


class AddItemPopup(Popup):
    def __init__(self, parent, player, items):
        """
        Args:
            parent (PlayerLayout):
        """
        self.player = player
        self.items = items
        super().__init__("Add Item", parent)
        self.selected_item = None

    def get_info(self):
        if self.selected_item:
            self.player.assign_item(self.selected_item)
        self.close()

    def create_form(self):
        layout = QGridLayout()
        list_widget = QListWidget()
        list_widget.itemClicked.connect(self.add_item)
        for item in self.items:
            if not item.player:
                list_widget.addItem(item.name)
        layout.addWidget(list_widget, 0, 0)
        self.form_group_box.setLayout(layout)

    def add_item(self, item_selected):
        for item in self.items:
            if item.name == item_selected.text():
                self.selected_item = item
            return


class EditPlayerPopup(PlayerCreationPopup):
    def __init__(self, parent, player, index):
        super().__init__(parent)
        self.player = player
        self.index = index
        self.name_line_edit.setText(player.name)
        for name, line_edit in self.ability_line_edits.items():
            line_edit.setText(str(getattr(player.ability_scores, name)()))
        for name, line_edit in self.skill_line_edits.items():
            line_edit.setText(str(getattr(player.skills, name)()))

    def get_info(self):
        self.parent.players[self.index].ability_scores = self._get_ability_scores()
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


def button_manage_player_style(button):
    button.setMinimumWidth(150)
    return button
