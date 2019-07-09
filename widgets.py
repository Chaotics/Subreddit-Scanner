from functools import partial

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QSpinBox, QLineEdit, QTextEdit, QVBoxLayout, QFormLayout, QPushButton
from praw import Reddit

from generic import create_feed, backup_tofeed, mimic_feed, save_hot
from gui import GuiInterface


def make_create_menu(reddit, back_function):
    create_menu_widget = QWidget()
    main_layout = create_central_layout(back_function)
    form_layout = QFormLayout()

    name_line_edit = QLineEdit()
    subreddits_text_edit = QTextEdit()
    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(partial(create_submitted, reddit, name_line_edit, subreddits_text_edit))

    form_layout.addRow("Name (50 character limit): ", name_line_edit)
    form_layout.addRow("Subreddits (comma separated): ", subreddits_text_edit)

    main_layout.addLayout(form_layout)
    main_layout.addWidget(submit_button)
    create_menu_widget.setLayout(main_layout)
    return create_menu_widget


def make_backup_menu(reddit, back_function):
    backup_menu_widget = QWidget()
    main_layout = create_central_layout(back_function)
    form_layout = QFormLayout()
    name_line_edit = QLineEdit()
    form_layout.addRow("Name of multifeed to backup to: ", name_line_edit)
    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(partial(backup_submitted, reddit, name_line_edit))
    main_layout.addLayout(form_layout)
    main_layout.addWidget(submit_button)
    backup_menu_widget.setLayout(main_layout)
    return backup_menu_widget


def make_mimic_menu(reddit, back_function):
    mimic_menu_widget = QWidget()
    main_layout = create_central_layout(back_function)
    form_layout = QFormLayout()
    name_line_edit = QLineEdit()
    form_layout.addRow("Name of multifeed to mimic: ", name_line_edit)
    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(partial(mimic_submitted, reddit, name_line_edit))
    main_layout.addLayout(form_layout)
    main_layout.addWidget(submit_button)
    mimic_menu_widget.setLayout(main_layout)
    return mimic_menu_widget


def make_save_menu(reddit, back_function):
    save_menu_widget = QWidget()
    main_layout = create_central_layout(back_function)
    form_layout = QFormLayout()

    name_line_edit = QLineEdit()
    quantity_spin_box = QSpinBox()
    quantity_spin_box.setValue(1)
    quantity_spin_box.setRange(1, 2147483647)
    form_layout.addRow("Name of multifeed: ", name_line_edit)
    form_layout.addRow("Number of items to save: ", quantity_spin_box)
    submit_button = QPushButton("Submit")
    submit_button.clicked.connect(partial(save_submitted, reddit, name_line_edit, quantity_spin_box))
    main_layout.addLayout(form_layout)
    main_layout.addWidget(submit_button)
    save_menu_widget.setLayout(main_layout)
    return save_menu_widget


def create_central_layout(back_function):
    central_layout = QVBoxLayout()
    back_button = QPushButton("<--- Back to Main Menu")
    back_button.pressed.connect(back_function)
    central_layout.addWidget(back_button, alignment=QtCore.Qt.AlignLeft)
    central_layout.setSpacing(20)
    return central_layout


# All of the following submit functions must be changed in order to error check BEFORE we send it to the gui class
# examples of the old error check methods have been put inside the gui class for reference and commented out

def create_submitted(reddit: Reddit, name_line_edit: QLineEdit, subreddits_text_edit: QTextEdit):
    multi_name = name_line_edit.text()
    subreddits = subreddits_text_edit.toPlainText()
    print("New multi name: " + multi_name)
    print("Subreddits to include: " + subreddits)

    # TODO
    # when we create the gui interface for the generic objects, we need to pass it a screen item it can write to
    gui_connect = GuiInterface()
    gui_connect.multi_name = name_line_edit.text()
    gui_connect.subreddit_string = subreddits_text_edit.toPlainText()
    create_feed(reddit, gui_connect)
    name_line_edit.clear()
    subreddits_text_edit.clear()


def backup_submitted(reddit: Reddit, name_line_edit: QLineEdit):
    backup_name = name_line_edit.text()
    print("Backup name " + backup_name)
    gui_connect = GuiInterface()
    gui_connect.multi_name = name_line_edit.text()
    backup_tofeed(reddit, gui_connect)
    name_line_edit.clear()


def mimic_submitted(reddit: Reddit, name_line_edit: QLineEdit):
    mimic_name = name_line_edit.text()
    print("Mimiced multi name: " + mimic_name)
    gui_connect = GuiInterface()
    gui_connect.multi_name = name_line_edit.text()
    mimic_feed(reddit, gui_connect)

    name_line_edit.clear()


def save_submitted(reddit: Reddit, name_line_edit: QLineEdit, quantity_spin_box: QSpinBox):
    multi_name = name_line_edit.text()
    num_to_save = quantity_spin_box.text()
    print("Multi to save from: " + multi_name)
    print("# of items to save: " + num_to_save)
    gui_connect = GuiInterface()
    gui_connect.multi_name = name_line_edit.text()
    gui_connect.number_of_items = int(num_to_save)
    save_hot(reddit, gui_connect)
    name_line_edit.clear()
    quantity_spin_box.setValue(quantity_spin_box.minimum())
