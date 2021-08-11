import atexit
import pickle

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QFormLayout, QDialogButtonBox, QLineEdit, \
    QGroupBox, QDialog, QGridLayout, QTabWidget, QWidget

from Core.player import Player, AbilityScores, AbilityScore
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
        stats = {
            "Strength": player.ability_scores.strength(),
            "Dexterity": player.ability_scores.dexterity(),
            "Constitution": player.ability_scores.constitution(),
            "Intelligence": player.ability_scores.intelligence(),
            "Wisdom": player.ability_scores.wisdom(),
            "Charisma": player.ability_scores.charisma()
        }
        grid_num = 0
        for stat, value in stats.items():
            stat_label = stat_layout_style(stat)
            layout.addWidget(stat_label, grid_num, 0)
            value_label = stat_layout_style(value)
            layout.addWidget(value_label, grid_num, 1)
            grid_num += 1

        player_tab.setLayout(layout)
        return player_tab

    def _add_create_player(self):
        button = button_dice_style(QPushButton('Create New Player'))
        button.setMinimumWidth(150)
        button.clicked.connect(self.open_player_creation)
        button.show()
        self.addWidget(button, 1, 0, 1, 1)

    def _add_edit_player(self):
        button = button_dice_style(QPushButton('Edit Player'))
        button.setMinimumWidth(150)
        button.clicked.connect(self.edit_player)
        button.show()
        self.addWidget(button, 2, 0, 1, 1)

    def _add_delete_player(self):
        button = button_dice_style(QPushButton('Delete Player'))
        button.setMinimumWidth(150)
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
        self.strength_line_edit = QLineEdit()
        self.dexterity_line_edit = QLineEdit()
        self.constitution_line_edit = QLineEdit()
        self.intelligence_line_edit = QLineEdit()
        self.wisdom_line_edit = QLineEdit()
        self.charisma_line_edit = QLineEdit()

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
        player = Player(self.name_line_edit.text(), self._get_ability_scores())
        # closing the window
        self.parent.add_player(player)
        self.close()

    def _get_ability_scores(self):
        return AbilityScores(strength=AbilityScore(int(self.strength_line_edit.text())),
                             dexterity=AbilityScore(int(self.dexterity_line_edit.text())),
                             constitution=AbilityScore(int(self.constitution_line_edit.text())),
                             intelligence=AbilityScore(int(self.intelligence_line_edit.text())),
                             wisdom=AbilityScore(int(self.wisdom_line_edit.text())),
                             charisma=AbilityScore(int(self.charisma_line_edit.text())))

    def create_form(self):
        layout = QFormLayout()
        layout.addRow(QLabel("Name"), self.name_line_edit)
        layout.addRow(QLabel("Strength"), self.strength_line_edit)
        layout.addRow(QLabel("Dexterity"), self.dexterity_line_edit)
        layout.addRow(QLabel("Constitution"), self.constitution_line_edit)
        layout.addRow(QLabel("Intelligence"), self.intelligence_line_edit)
        layout.addRow(QLabel("Wisdom"), self.wisdom_line_edit)
        layout.addRow(QLabel("Charisma"), self.charisma_line_edit)
        self.form_group_box.setLayout(layout)


class EditPlayerPopup(PlayerCreationPopup):
    def __init__(self, parent, player, index):
        super().__init__(parent)
        self.player = player
        self.index = index
        self.name_line_edit.setText(player.name)
        self.strength_line_edit.setText(str(player.ability_scores.strength()))
        self.dexterity_line_edit.setText(str(player.ability_scores.dexterity()))
        self.constitution_line_edit.setText(str(player.ability_scores.constitution()))
        self.intelligence_line_edit.setText(str(player.ability_scores.intelligence()))
        self.wisdom_line_edit.setText(str(player.ability_scores.wisdom()))
        self.charisma_line_edit.setText(str(player.ability_scores.charisma()))

    def get_info(self):
        self.parent.players[self.index].ability_scores = self._get_ability_scores()
        self.close()


def stat_layout_style(value):
    label = QLabel(str(value))
    label.setFont(QFont('Arial', 13))
    label.show()
    return label


def button_dice_style(button):
    button.setMinimumWidth(80)
    return button
