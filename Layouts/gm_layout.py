from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGridLayout, QWidget, QTabWidget, QPushButton

from Core.player import get_all_players
from CustomObjects.lines import VLine, HLine
from Style.button_styles import button_manage_refresh_style
from Style.label_style import stat_layout_style, stat_header_style


class GMInfoLayout(QGridLayout):
    def __init__(self):
        super().__init__()
        self.tabwidget = self.create_item_overview_tabs()
        button = button_manage_refresh_style(QPushButton("refresh"))
        button.clicked.connect(self.update)
        button.show()
        self.addWidget(button, 0, 0, 1, 1)

    def create_item_overview_tabs(self):
        tabwidget = QTabWidget()
        tabwidget.setStyleSheet("""QTabBar::tab:selected{ background: DarkCyan }""")
        tabwidget.addTab(self.create_item_overview_tab(), "Item Overview")
        tabwidget.setMaximumHeight(700)
        self.addWidget(tabwidget, 1, 0, 4, 1, alignment=Qt.AlignTop)
        return tabwidget

    def create_item_overview_tab(self):
        item_overview = QWidget()
        layout = QGridLayout()
        layout.setVerticalSpacing(10)
        players = get_all_players()
        for i in range(1, 21):
            item_level_header = stat_header_style(str(i))
            layout.addWidget(item_level_header, 0, i * 2, alignment=Qt.AlignCenter)
            layout.addWidget(VLine(color=QColor("White")), 1, i*2-1, len(players) + 1, 1)
        layout.addWidget(HLine(color=QColor("White")), 1, 1, 1, 43)
        item_level_header = stat_header_style("GP")
        layout.addWidget(item_level_header, 0, 42, alignment=Qt.AlignCenter)
        grid_num = 2
        for player in players:
            stat_label = stat_layout_style(player.name)
            layout.addWidget(stat_label, grid_num, 0)
            items_by_level = [0] * 20
            total_gp = 0
            for item in player.items:
                items_by_level[int(item.item_level) - 1] += 1
                total_gp += int(item.gp_cost)
            side_grid = 2
            for item_count in items_by_level:
                stat_label = stat_layout_style(str(item_count))
                layout.addWidget(stat_label, grid_num, side_grid, alignment=Qt.AlignCenter)
                side_grid += 2
            gp_count = stat_layout_style(str(total_gp))
            layout.addWidget(gp_count, grid_num, side_grid, alignment=Qt.AlignCenter)
            grid_num += 1
        item_overview.setLayout(layout)
        return item_overview

    def update(self):
        self.tabwidget.close()
        self.tabwidget = self.create_item_overview_tabs()


def clean_field_name(value):
    value = value.replace("_", " ")
    return value.title()
