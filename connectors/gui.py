from prawcore.exceptions import Conflict

from PyQt5.QtWidgets import QTextEdit, QMessageBox
from PyQt5.QtGui import QTextCursor, QGuiApplication
from connectors.generic import get_user
from connectors.subreddit_bot import SubredditBot


class GuiInterface(SubredditBot):

    def __init__(self, write_item: QTextEdit):
        self.multi_name = ""
        self.subreddit_list = []
        self.subreddit_string = None
        self.number_of_items = 0
        self.write_item = write_item

    def reset_write(self):
        self.write_item.clear()

    def send_error(self, error):
        err_dialog = QMessageBox()
        err_dialog.setIcon(QMessageBox.Critical)
        err_dialog.setText(error)
        err_dialog.setWindowTitle("Error")
        err_dialog.exec_()

    def write_to_screen(self, to_write):
        self.write_item.moveCursor(QTextCursor.End)
        self.write_item.append(to_write)
        self.write_item.moveCursor(QTextCursor.End)
        QGuiApplication.processEvents()

    def create_write(self, to_write):
        self.write_to_screen(to_write)

    def create_read(self, reddit):
        self.subreddit_list = [] if self.subreddit_string == '' else self.subreddit_string.split(',')
        multi = self.create_multi(reddit)
        if multi is not None:
            items_read = (self.subreddit_list, multi)
        else:
            items_read = None
        return items_read

    def backup_write(self, to_write):
        self.write_to_screen(to_write)

    def backup_read(self, reddit):
        return self.create_multi(reddit)

    def mimic_write(self, to_write):
        self.write_to_screen(to_write)

    def mimic_read(self, reddit):
        feed_name = self.multi_name

        multi_list = reddit.user.multireddits()
        user_name = get_user()
        match = False
        correct_multi = None
        while not match:
            for multi in multi_list:
                if multi == ("/user/" + user_name + "/m/" + feed_name):
                    match = True
                    correct_multi = multi
            if match:
                break
            # The following must be sent to the screen somehow! we should re-take the input and somehow stop the
            # current process
            feed_name = input("\nPlease enter a feed you own!\n")
            break

        return correct_multi

    def save_write(self, to_write):
        self.write_to_screen(to_write)

    def save_read(self, reddit):
        feed_name = self.multi_name
        multi = reddit.multireddit(get_user(), feed_name)
        # old way to check validity of the multi name, we must do this in the gui
        # while multi is None:
        #     feed_name = input("\nFeed invalid, please re-enter field\n")
        #     multi = reddit.multireddit(get_user(), feed_name)
        count = self.number_of_items
        # while(count > 100):
        #     count = int(input("\nPlease re-enter the number of items you would like to save (max 100)\n"))
        hot_list = multi.hot()
        commands = [hot_list, count]
        return commands

    def create_multi(self, reddit):
        multi = None
        feed_name = self.multi_name
        while multi is None:
            try:
                multi = reddit.multireddit.create(display_name=feed_name, subreddits=[])
                break
            except Conflict:
                self.send_error("There was an error creating the multi-reddit due to a conflict. Possibly because a "
                                "multi-reddit with that name already exists")
                return multi
        self.create_write("Created Multi-Reddit named: %s\n" % str(feed_name))
        return multi
