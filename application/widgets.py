from functools import partial
from typing import Tuple

from PyQt5 import QtCore
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QWidget, QSpinBox, QLineEdit, QTextEdit, QVBoxLayout, QFormLayout, QPushButton, QSizePolicy

from connectors.generic import create_feed, backup_tofeed, mimic_feed, save_hot, unsave
from connectors.gui import GuiInterface, send_error_dialog


class WidgetCreator:

    def __init__(self, reddit, parent_back_func):
        self.ignore_input = False
        self.reddit = reddit
        self.parent_back_func = parent_back_func

    # method responsible for creating the create sub-menu
    def make_create_menu(self):
        create_menu_widget = QWidget()
        form_layout = QFormLayout()
        name_line_edit = QLineEdit()
        subreddits_text_edit = QTextEdit()
        subreddits_text_edit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        subreddits_text_edit.setFixedHeight(100)
        submit_button = QPushButton("Submit")
        form_layout.addRow("Name (50 character limit): ", name_line_edit)
        form_layout.addRow("Subreddits (comma separated): ", subreddits_text_edit)
        main_layout, display_text_edit = self.create_central_layout((name_line_edit, subreddits_text_edit))
        main_layout.insertLayout(1, form_layout)
        main_layout.addWidget(submit_button)
        submit_button.clicked.connect(
            partial(self.create_submitted, name_line_edit, subreddits_text_edit, display_text_edit))
        create_menu_widget.setLayout(main_layout)
        return create_menu_widget

    # method responsible for creating the backup sub-menu
    def make_backup_menu(self):
        backup_menu_widget = QWidget()
        form_layout = QFormLayout()
        name_line_edit = QLineEdit()
        submit_button = QPushButton("Submit")
        form_layout.addRow("Name of multifeed to backup to: ", name_line_edit)
        main_layout, display_text_edit = self.create_central_layout((name_line_edit,))
        main_layout.insertLayout(1, form_layout)
        main_layout.addWidget(submit_button)
        submit_button.clicked.connect(partial(self.backup_submitted, name_line_edit, display_text_edit))
        backup_menu_widget.setLayout(main_layout)
        return backup_menu_widget

    # method responsible for creating the mimic sub-menu
    def make_mimic_menu(self):
        mimic_menu_widget = QWidget()
        form_layout = QFormLayout()
        name_line_edit = QLineEdit()
        submit_button = QPushButton("Submit")
        form_layout.addRow("Name of multifeed to mimic: ", name_line_edit)
        main_layout, display_text_edit = self.create_central_layout((name_line_edit,))
        main_layout.insertLayout(1, form_layout)
        main_layout.addWidget(submit_button)
        submit_button.clicked.connect(partial(self.mimic_submitted, name_line_edit, display_text_edit))
        mimic_menu_widget.setLayout(main_layout)
        return mimic_menu_widget

    # method responsible for creating the save sub-menu
    def make_save_menu(self):
        save_menu_widget = QWidget()
        form_layout = QFormLayout()
        name_line_edit = QLineEdit()
        quantity_spin_box = QSpinBox()
        quantity_spin_box.setValue(1)
        quantity_spin_box.setRange(1, 100)
        submit_button = QPushButton("Submit")
        form_layout.addRow("Name of multifeed: ", name_line_edit)
        form_layout.addRow("Number of items to save: ", quantity_spin_box)
        main_layout, display_text_edit = self.create_central_layout((name_line_edit, quantity_spin_box))
        main_layout.insertLayout(1, form_layout)
        main_layout.addWidget(submit_button)
        submit_button.clicked.connect(
            partial(self.save_submitted, name_line_edit, quantity_spin_box, display_text_edit))
        save_menu_widget.setLayout(main_layout)
        return save_menu_widget

    # method responsible for creating the unsave sub-menu
    def make_unsave_menu(self):
        unsave_menu_widget = QWidget()
        form_layout = QFormLayout()
        quantity_spin_box = QSpinBox()
        quantity_spin_box.setValue(1)
        quantity_spin_box.setRange(1, 1000)
        submit_button = QPushButton("Submit")
        form_layout.addRow("Number of items to unsave: ", quantity_spin_box)
        main_layout, display_text_edit = self.create_central_layout((quantity_spin_box,))
        main_layout.insertLayout(1, form_layout)
        main_layout.addWidget(submit_button)
        submit_button.clicked.connect(
            partial(self.unsave_submitted, quantity_spin_box, display_text_edit))
        unsave_menu_widget.setLayout(main_layout)
        return unsave_menu_widget

    # method responsible for creating the generic layout for each sub-menu
    def create_central_layout(self, input_fields: Tuple):
        central_layout = QVBoxLayout()
        back_button = QPushButton("<--- Back to Main Menu")
        display_text_edit = QTextEdit()
        display_text_edit.setReadOnly(True)
        back_button.pressed.connect(
            partial(self.handle_back_pressed, input_fields + (display_text_edit,)))
        central_layout.setSpacing(20)
        central_layout.addWidget(back_button, alignment=QtCore.Qt.AlignLeft)
        central_layout.addWidget(display_text_edit)
        return central_layout, display_text_edit

    def handle_back_pressed(self, input_fields: Tuple):
        if self.ignore_input:
            send_error_dialog("Please do not attempt to change screens while there is a function in process.")
            return

        self.parent_back_func()
        for field in input_fields:
            if isinstance(field, QSpinBox):
                field.setValue(field.minimum())
            else:
                field.clear()

    # TODO All of the following submit functions must be changed in order to error check BEFORE we send it to the gui
    #  class examples of the old error check methods have been put inside the gui class for reference and commented
    #  out method that gets executed when the submit button for create is pressed
    def create_submitted(self, name_line_edit: QLineEdit, subreddits_text_edit: QTextEdit,
                         display_text_edit: QTextEdit):
        if self.ignore_input:
            send_error_dialog("Please do not attempt to change screens while there is a function in process.")
            return

        multi_name = name_line_edit.text()
        subreddits = subreddits_text_edit.toPlainText()
        gui_connect = GuiInterface(display_text_edit)
        gui_connect.multi_name = multi_name
        gui_connect.subreddit_string = subreddits

        self.ignore_input = True
        QGuiApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        create_feed(self.reddit, gui_connect)
        name_line_edit.clear()
        subreddits_text_edit.clear()
        gui_connect.write_to_screen("\n")
        QGuiApplication.restoreOverrideCursor()
        self.ignore_input = False

    # method that gets executed when the submit button for backup is pressed
    def backup_submitted(self, name_line_edit: QLineEdit, display_text_edit: QTextEdit):
        if self.ignore_input:
            send_error_dialog("Please do not attempt to change screens while there is a function in process.")
            return

        gui_connect = GuiInterface(display_text_edit)
        gui_connect.multi_name = name_line_edit.text()

        self.ignore_input = True
        QGuiApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        backup_tofeed(self.reddit, gui_connect)
        name_line_edit.clear()
        gui_connect.write_to_screen("\n")
        QGuiApplication.restoreOverrideCursor()
        self.ignore_input = False

    # method that gets executed when the submit button for mimic is pressed
    def mimic_submitted(self, name_line_edit: QLineEdit, display_text_edit: QTextEdit):
        if self.ignore_input:
            send_error_dialog("Please do not attempt to change screens while there is a function in process.")
            return

        gui_connect = GuiInterface(display_text_edit)
        gui_connect.multi_name = name_line_edit.text()

        self.ignore_input = True
        QGuiApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        mimic_feed(self.reddit, gui_connect)
        name_line_edit.clear()
        gui_connect.write_to_screen("\n")
        QGuiApplication.restoreOverrideCursor()
        self.ignore_input = False

    # method that gets executed when the submit button for save is pressed
    def save_submitted(self, name_line_edit: QLineEdit, quantity_spin_box: QSpinBox,
                       display_text_edit: QTextEdit):
        if self.ignore_input:
            send_error_dialog("Please do not attempt to change screens while there is a function in process.")
            return

        num_to_save = quantity_spin_box.text()
        gui_connect = GuiInterface(display_text_edit)
        gui_connect.multi_name = name_line_edit.text()
        gui_connect.number_of_items = int(num_to_save)

        self.ignore_input = True
        QGuiApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        save_hot(self.reddit, gui_connect)
        name_line_edit.clear()
        quantity_spin_box.setValue(quantity_spin_box.minimum())
        gui_connect.write_to_screen("\n")
        QGuiApplication.restoreOverrideCursor()
        self.ignore_input = False

    def unsave_submitted(self, quantity_spin_box: QSpinBox, display_text_edit: QTextEdit):
        if self.ignore_input:
            send_error_dialog("Please do not attempt to change screens while there is a function in process.")
            return

        num_to_unsave = quantity_spin_box.text()
        gui_connect = GuiInterface(display_text_edit)
        gui_connect.number_of_items = int(num_to_unsave)

        self.ignore_input = True
        QGuiApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        unsave(self.reddit, gui_connect)
        quantity_spin_box.setValue(quantity_spin_box.minimum())
        gui_connect.write_to_screen("\n")
        QGuiApplication.restoreOverrideCursor()
        self.ignore_input = False
