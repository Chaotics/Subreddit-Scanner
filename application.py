import sys
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton

# sub-classes the QMainWindow QtWidget class to display a window
class AppWindow(QMainWindow):
    # uses the init method to setup the window GUI, with the passed in width and height
    def __init__(self, width, height, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)
        self.window_width = width
        self.window_height = height
        self.setup_gui()

    # the main method that sets up the GUI
    def setup_gui(self):
        # sets the title to the application window
        self.setWindowTitle("Subreddit Scanner")
        # add the vertical layout
        vlayout = QVBoxLayout()
        # adds the necessary buttons for each functionality of the application
        self.add_buttons(vlayout)
        # adds a dummy widget so it can be added as the central widget to the QMainWindow
        central_widget = QWidget()
        central_widget.setLayout(vlayout)
        self.setCentralWidget(central_widget)

    # method that adds all the buttons on the main menu
    def add_buttons(self, vlayout):
        # first creates a list of buttons to add
        button_names = ["Create", "Backup", "Mimic", "Save Hot Items", "Quit"]
        button_spacing = 50
        # then calculates the theoretical maximum button height
        button_height = (self.window_height - (len(button_names) * button_spacing)) / len(button_names)
        # and then a button for each button name in the list is created, aligned to the center of the layout
        for i in range(0, len(button_names)):
            button = QPushButton(button_names[i])
            button.setFixedSize(150, min(button_height, 100))
            vlayout.addWidget(button, alignment=QtCore.Qt.AlignCenter)


# method responsible for starting the application
def start_app():
    # creates an application instance
    app = QApplication([])
    window_width = 800
    window_height = 600
    # adds a window to the application
    window = AppWindow(width=window_width, height=window_height)
    screen_size = app.desktop().screenGeometry()
    # resizes the window to be in the middle of the screen and sized correctly
    window.setGeometry((screen_size.width() - window_width) / 2,
                       (screen_size.height() - window_height) / 2,
                       window_width, window_height)
    # shows the window on the screen
    window.show()
    # calls app.exec_ to start an endless event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()