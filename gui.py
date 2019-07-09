from sys import stderr

from prawcore.exceptions import Conflict

from generic import get_user
from subreddit_bot import SubredditBot


class GuiInterface(SubredditBot):
    multi_name = ""
    subreddit_list = []
    subreddit_string = None
    number_of_items = 0
    write_item = None

    def send_error(self, error):
        stderr.write(error)

    def create_write(self, to_write):
        print(to_write)

    def create_read(self, reddit):
        self.subreddit_list = self.subreddit_string.split(',')
        print(self.subreddit_list)
        multi = self.create_multi(reddit)
        items_read = [self.subreddit_list, multi]
        return items_read

    def backup_write(self, to_write):
        print(to_write)

    def backup_read(self, reddit):
        return self.create_multi(reddit)

    def mimic_write(self, to_write):
        print(to_write)

    def mimic_read(self, reddit):
        feed_name = self.multi_name

        multi_list = reddit.user.multireddits()
        user_name = get_user()
        match = False
        correct_multi = None
        while not match:
            for multi in multi_list:
                print(multi)
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
        print(to_write)

    def save_read(self, reddit):
        feed_name = self.multi_name
        multi = reddit.multireddit(get_user(), feed_name)
        # old wa to check validity of the multi name, we must do this in the gui
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
                # TODO
                print("This occured")
                # should send to the screen an error dialog here and somehow get the users data again
                return multi
                # continue
        return multi
