from dataclasses import fields

from PyQt5.QtWidgets import QVBoxLayout, QDialogButtonBox, QLineEdit, QGroupBox, QDialog


class Popup(QDialog):
    def __init__(self, name, parent):
        """
        Args:
            parent (itemLayout):
        """
        super().__init__()
        self.setWindowTitle(name)
        self.setGeometry(100, 100, 300, 400)
        self.form_group_box = QGroupBox("")
        self.parent = parent

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

    def create_form(self):
        """
        placeholder function that implements the creation of the form for the popup
        """


def get_field_names(data_cls):
    return [field.name for field in fields(data_cls)]


def create_qlines(names):
    qlines = {}
    for name in names:
        qlines[name] = QLineEdit()
    return qlines
