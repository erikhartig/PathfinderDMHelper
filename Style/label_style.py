from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel


def stat_layout_style(value):
    label = QLabel(str(value))
    label.setFont(QFont('Arial', 13))
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
