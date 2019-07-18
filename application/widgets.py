from functools import partial
from typing import Tuple

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSpinBox, QLineEdit, QTextEdit, QVBoxLayout, QFormLayout, QPushButton, QSizePolicy
from praw import Reddit

from connectors.generic import create_feed, backup_tofeed, mimic_feed, save_hot
from connectors.gui import GuiInterface


# method responsible for creating the create sub-menu
def make_create_menu(reddit, back_function):
    create_menu_widget = QWidget()
    form_layout = QFormLayout()
    name_line_edit = QLineEdit()
    subreddits_text_edit = QTextEdit()
    subreddits_text_edit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
    subreddits_text_edit.setFixedHeight(100)
    submit_button = QPushButton("Submit")

    form_layout.addRow("Name (50 character limit): ", name_line_edit)
    form_layout.addRow("Subreddits (comma separated): ", subreddits_text_edit)
    main_layout, display_text_edit = create_central_layout(back_function, (name_line_edit, subreddits_text_edit))
    main_layout.insertLayout(1, form_layout)
    main_layout.addWidget(submit_button)
    submit_button.clicked.connect(
        partial(create_submitted, reddit, name_line_edit, subreddits_text_edit, display_text_edit))
    create_menu_widget.setLayout(main_layout)
    return create_menu_widget


# method responsible for creating the backup sub-menu
def make_backup_menu(reddit, back_function):
    backup_menu_widget = QWidget()
    form_layout = QFormLayout()
    name_line_edit = QLineEdit()
    submit_button = QPushButton("Submit")

    form_layout.addRow("Name of multifeed to backup to: ", name_line_edit)
    main_layout, display_text_edit = create_central_layout(back_function, (name_line_edit,))
    main_layout.insertLayout(1, form_layout)
    main_layout.addWidget(submit_button)
    submit_button.clicked.connect(partial(backup_submitted, reddit, name_line_edit, display_text_edit))
    backup_menu_widget.setLayout(main_layout)
    return backup_menu_widget


# method responsible for creating the mimic sub-menu
def make_mimic_menu(reddit, back_function):
    mimic_menu_widget = QWidget()
    form_layout = QFormLayout()
    name_line_edit = QLineEdit()
    submit_button = QPushButton("Submit")

    form_layout.addRow("Name of multifeed to mimic: ", name_line_edit)
    main_layout, display_text_edit = create_central_layout(back_function, (name_line_edit,))
    main_layout.insertLayout(1, form_layout)
    main_layout.addWidget(submit_button)
    submit_button.clicked.connect(partial(mimic_submitted, reddit, name_line_edit, display_text_edit))
    mimic_menu_widget.setLayout(main_layout)
    return mimic_menu_widget


# method responsible for creating the save sub-menu
def make_save_menu(reddit, back_function):
    save_menu_widget = QWidget()
    form_layout = QFormLayout()
    name_line_edit = QLineEdit()
    quantity_spin_box = QSpinBox()
    quantity_spin_box.setValue(1)
    quantity_spin_box.setRange(1, 2147483647)
    submit_button = QPushButton("Submit")

    form_layout.addRow("Name of multifeed: ", name_line_edit)
    form_layout.addRow("Number of items to save: ", quantity_spin_box)
    main_layout, display_text_edit = create_central_layout(back_function, (name_line_edit, quantity_spin_box))
    main_layout.insertLayout(1, form_layout)
    main_layout.addWidget(submit_button)
    submit_button.clicked.connect(partial(save_submitted, reddit, name_line_edit, quantity_spin_box, display_text_edit))
    save_menu_widget.setLayout(main_layout)
    return save_menu_widget


# method responsible for creating the generic layout for each sub-menu
def create_central_layout(parent_back_function, input_fields: Tuple):
    central_layout = QVBoxLayout()
    back_button = QPushButton("<--- Back to Main Menu")
    display_text_edit = QTextEdit()
    display_text_edit.setReadOnly(True)
    back_button.pressed.connect(partial(handle_back_pressed, parent_back_function, input_fields + (display_text_edit,)))
    central_layout.setSpacing(20)
    central_layout.addWidget(back_button, alignment=QtCore.Qt.AlignLeft)
    central_layout.addWidget(display_text_edit)
    return central_layout, display_text_edit


def handle_back_pressed(parent_back_function, reset_fields: Tuple):
    parent_back_function()
    for field in reset_fields:
        field.clear()


# TODO All of the following submit functions must be changed in order to error check BEFORE we send it to the gui class
# examples of the old error check methods have been put inside the gui class for reference and commented out

# method that gets executed when the submit button for create is pressed
def create_submitted(reddit: Reddit, name_line_edit: QLineEdit, subreddits_text_edit: QTextEdit,
                     display_text_edit: QTextEdit):
    multi_name = name_line_edit.text()
    subreddits = subreddits_text_edit.toPlainText()
    gui_connect = GuiInterface(display_text_edit)
    gui_connect.multi_name = multi_name
    gui_connect.subreddit_string = subreddits
    create_feed(reddit, gui_connect)
    name_line_edit.clear()
    subreddits_text_edit.clear()


# method that gets executed when the submit button for backup is pressed
def backup_submitted(reddit: Reddit, name_line_edit: QLineEdit, display_text_edit: QTextEdit):
    gui_connect = GuiInterface(display_text_edit)
    gui_connect.multi_name = name_line_edit.text()
    backup_tofeed(reddit, gui_connect)
    name_line_edit.clear()


# method that gets executed when the submit button for mimic is pressed
def mimic_submitted(reddit: Reddit, name_line_edit: QLineEdit, display_text_edit: QTextEdit):
    gui_connect = GuiInterface(display_text_edit)
    gui_connect.multi_name = name_line_edit.text()
    mimic_feed(reddit, gui_connect)

    name_line_edit.clear()


# method that gets executed when the submit button for save is pressed
def save_submitted(reddit: Reddit, name_line_edit: QLineEdit, quantity_spin_box: QSpinBox,
                   display_text_edit: QTextEdit):
    num_to_save = quantity_spin_box.text()
    gui_connect = GuiInterface(display_text_edit)
    gui_connect.multi_name = name_line_edit.text()
    gui_connect.number_of_items = int(num_to_save)
    save_hot(reddit, gui_connect)
    name_line_edit.clear()
    quantity_spin_box.setValue(quantity_spin_box.minimum())
