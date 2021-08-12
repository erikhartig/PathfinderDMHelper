import atexit
import pickle
from dataclasses import fields

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QFormLayout, QDialogButtonBox, QLineEdit, \
    QGroupBox, QDialog, QGridLayout, QTabWidget, QWidget

from Core.player import Player, AbilityScores, AbilityScore, Skills, SkillScore
from paths import PLAYERS


class PlayerLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.players = self.load_players()
        self.tabwidget = self.create_player_tabs()
        self.addWidget(self.tabwidget, 1, 1, 4, 4)

        title = QLabel("Players")
        title.setFont(QFont('Arial', 20))
        title.setAlignment(Qt.AlignCenter)
        self.addWidget(title, 0, 1)
        self._add_create_player()
        self._add_edit_player()
        self._add_delete_player()
        atexit.register(self.save_players)

    def create_player_tabs(self):
        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("""QTabBar::tab:selected{ background: DarkCyan }""")
        for player in self.players:
            tabwidget.addTab(self.player_tab(player), player.name)
        self.addWidget(tabwidget, 1, 1, 4, 4)
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

    def delete_player(self):
        del self.players[self.tabwidget.currentIndex()]
        self._update_player_tabs()

    def edit_player(self):
        index = self.tabwidget.currentIndex()
        player = self.players[index]
        popup = EditPlayerPopup(self, player, index)
        popup.show()
        popup.exec()
        self._update_player_tabs()

    def open_player_creation(self):
        popup = PlayerCreationPopup(self)
        popup.show()
        popup.exec()

    def add_player(self, player):
        self.players.append(player)
        print(self.players)
        self._update_player_tabs()

    def _update_player_tabs(self):
        self.tabwidget.close()
        self.tabwidget = self.create_player_tabs()
        self.addWidget(self.tabwidget, 1, 1, 4, 4)

    def save_players(self):
        with open(PLAYERS, 'wb') as player_file:
            pickle.dump(self.players, player_file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_players():
        if not PLAYERS.exists():
            return []
        with open(PLAYERS, 'rb') as player_file:
            players = pickle.load(player_file)
        return players


class PlayerCreationPopup(QDialog):
    def __init__(self, parent):
        """
        Args:
            parent (PlayerLayout):
        """
        super().__init__()
        self.setWindowTitle("Create Player")
        self.player = None
        self.setGeometry(100, 100, 300, 400)
        self.form_group_box = QGroupBox("")
        self.parent = parent
        # creating a line edit
        self.name_line_edit = QLineEdit()
        self.ability_line_edits = {}
        self.abilities = [field.name for field in fields(AbilityScores)]
        for attribute in self.abilities:
            self.ability_line_edits[attribute] = QLineEdit()
            print(attribute)

        self.skill_line_edits = {}
        self.skills = [field.name for field in fields(Skills)]
        for skill in self.skills:
            self.skill_line_edits[skill] = QLineEdit()
            print(skill)
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
        player = Player(self.name_line_edit.text(), self._get_ability_scores(), self._get_skills())
        # closing the window
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
