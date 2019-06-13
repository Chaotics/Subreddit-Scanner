from PyQt5.QtWidgets import QWidget, QSpinBox, QLineEdit, QTextEdit, QVBoxLayout, QFormLayout, QPushButton
from PyQt5 import QtCore

def make_create_menu(back_function):
    create_menu_widget = QWidget()
    main_layout = create_central_layout(back_function)
    form_layout = QFormLayout()

    name_line_edit = QLineEdit()
    subreddits_text_edit = QTextEdit()

    form_layout.addRow("Name (50 character limit): ", name_line_edit)
    form_layout.addRow("Subreddits (comma separated): ", subreddits_text_edit)
    main_layout.addLayout(form_layout)
    create_menu_widget.setLayout(main_layout)
    return create_menu_widget


def make_mimic_menu(back_function):
    mimic_menu_widget = QWidget()
    main_layout = create_central_layout(back_function)
    form_layout = QFormLayout()
    name_line_edit = QLineEdit()
    form_layout.addRow("Name of subreddit to mimic: ", name_line_edit)
    main_layout.addLayout(form_layout)
    mimic_menu_widget.setLayout(main_layout)
    return mimic_menu_widget


def make_save_menu(back_function):
    save_menu_widget = QWidget()
    main_layout = create_central_layout(back_function)
    form_layout = QFormLayout()

    name_line_edit = QLineEdit()
    quantity_spin_box = QSpinBox()
    quantity_spin_box.setValue(1)
    quantity_spin_box.setRange(1, 2147483647)
    form_layout.addRow("Name of subreddit: ", name_line_edit)
    form_layout.addRow("Number of items to save: ", quantity_spin_box)
    main_layout.addLayout(form_layout)
    save_menu_widget.setLayout(main_layout)
    return save_menu_widget


def create_central_layout(back_function):
    central_layout = QVBoxLayout()
    back_button = QPushButton("<--- Back to Main Menu")
    back_button.pressed.connect(back_function)
    central_layout.addWidget(back_button, alignment=QtCore.Qt.AlignLeft)
    central_layout.setSpacing(20)
    return central_layout


