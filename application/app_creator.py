import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from application.widgets import WidgetCreator


class AppWindow(QMainWindow):
    # uses the init method to setup the window GUI, with the passed in width and height
    def __init__(self, width, height, reddit, *args, **kwargs):
        self.reddit = reddit
        super(AppWindow, self).__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.window_width = width
        self.window_height = height
        self.submenus = []
        # sets the title to the application window
        self.setWindowTitle("Subreddit Scanner")
        # add the vertical layout
        vlayout = QVBoxLayout()
        # adds the necessary buttons for each functionality of the application
        self.add_buttons(vlayout)
        # adds a dummy widget so it can be added as the central widget to the QMainWindow
        menu_widget = QWidget()
        menu_widget.setLayout(vlayout)
        central_widget = QWidget(self)
        self.widget_stack = QStackedWidget(central_widget)
        self.widget_stack.resize(self.window_width, self.window_height)
        self.widget_stack.addWidget(menu_widget)
        self.add_widgets()
        self.setCentralWidget(central_widget)

    # adds all of the widgets to the app that correspond to the buttons
    def add_widgets(self):
        widget_control = WidgetCreator(self.reddit, self.back_clicked)
        self.widget_stack.addWidget(widget_control.make_create_menu())
        self.widget_stack.addWidget(widget_control.make_backup_menu())
        self.widget_stack.addWidget(widget_control.make_mimic_menu())
        self.widget_stack.addWidget(widget_control.make_save_menu())
        self.widget_stack.addWidget(widget_control.make_unsave_menu())

    # method that switches the top widget to the main menu
    def back_clicked(self):
        self.widget_stack.setCurrentIndex(0)

    # method that switches the top widget to that of create
    def create_clicked(self):
        self.widget_stack.setCurrentIndex(1)

    # method that switches the top widget to that of backup
    def backup_clicked(self):
        self.widget_stack.setCurrentIndex(2)

    # method that switches the top widget to that of mimic
    def mimic_clicked(self):
        self.widget_stack.setCurrentIndex(3)

    # method that switches the top widget to that of save
    def save_clicked(self):
        self.widget_stack.setCurrentIndex(4)

    # method that switches the top widget to that of unsave
    def unsave_clicked(self):
        self.widget_stack.setCurrentIndex(5)

    # method that exits the application when clicked
    def quit_clicked(self):
        sys.exit(0)

    # method that adds all the buttons on the main menu
    def add_buttons(self, vlayout):
        # first creates a list of buttons to add
        button_names = ["Create", "Backup", "Mimic", "Save Hot Items", "Unsave", "Quit"]
        button_methods = [self.create_clicked, self.backup_clicked, self.mimic_clicked, self.save_clicked,
                          self.unsave_clicked, self.quit_clicked]
        button_spacing = 20
        # then calculates the theoretical maximum button height
        button_height = (self.window_height - (len(button_names) * button_spacing)) / len(button_names)
        button_width = 150
        current_hlayout = QHBoxLayout()
        current_hlayout.setAlignment(QtCore.Qt.AlignCenter)
        current_line_buttons = 0
        # and then a button for each button name in the list is created, aligned to the center of the layout
        for i in range(0, len(button_names)):
            button = QPushButton(button_names[i])
            button.setFixedSize(button_width, min(button_height, 80))
            button.clicked.connect(button_methods[i])
            if (current_line_buttons * button_spacing) + ((current_line_buttons+1) * button_width) > self.window_width:
                vlayout.addLayout(current_hlayout)
                current_hlayout = QHBoxLayout()
                current_hlayout.setAlignment(QtCore.Qt.AlignCenter)
                current_line_buttons = 0
            current_hlayout.addWidget(button, alignment=QtCore.Qt.AlignCenter)
            current_line_buttons += 1
        vlayout.addLayout(current_hlayout)
        vlayout.setAlignment(QtCore.Qt.AlignCenter)
        vlayout.setSpacing(button_spacing)