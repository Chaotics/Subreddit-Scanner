import scanner_bot
import sys
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QStackedWidget, QMainWindow, QWidget, QVBoxLayout, QPushButton
import widgets
from application import AppWindow
# sub-classes the QMainWindow QtWidget class to display a window

# method responsible for starting the application
def start_app():

    redditInstance = scanner_bot.login()
    print("Logged in successfully...")
    # creates an application instance
    app = QApplication([])
    window_width = 800
    window_height = 600
    # adds a window to the application
    window = AppWindow(width=window_width, height=window_height, reddit=redditInstance)
    #window.reddit = redditInstance
    # resizes the window to be in the middle of the screen and sized correctly
    screen_size = app.desktop().screenGeometry()
    window.setGeometry((screen_size.width() - window_width) / 2,
                       (screen_size.height() - window_height) / 2,
                       window_width, window_height)

    app.setStyleSheet("""
    .QWidget{
        background-color:rgb(00, 235, 215);
    }""")
    # shows the window on the screen
    window.show()

    # calls app.exec_ to start an endless event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    start_app()
    
