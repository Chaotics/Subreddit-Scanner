from sys import stderr

from prawcore.exceptions import Conflict, BadRequest

from connectors.generic import get_user
from connectors.subreddit_bot import SubredditBot, is_valid_multi_name


class Terminal(SubredditBot):

    def send_error(self, error):
        stderr.write(error)

    def write_to_screen(self, to_write):
        print(to_write)

    def create_write(self, to_write):
        self.write_to_screen(to_write)

    def create_read(self, reddit):
        multi = self.create_multi(reddit)
        subreddit_list = self.read_subreddits()
        items_read = [subreddit_list, multi]
        return items_read

    def backup_write(self, to_write):
        self.write_to_screen(to_write)

    def backup_read(self, reddit):
        return self.create_multi(reddit)

    def mimic_write(self, to_write):
        self.write_to_screen(to_write)

    def mimic_read(self, reddit):
        feed_name = input("\nWhat feed would you like to mimic?\n")

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
            feed_name = input("\nPlease enter a feed you own!\n")

        return correct_multi

    def save_write(self, to_write):
        self.write_to_screen(to_write)

    def save_read(self, reddit):
        feed_name = input("\nWhat feed would you like to save?\n")
        multi = reddit.multireddit(get_user(), feed_name)

        while multi is None:
            feed_name = input("\nFeed invalid, please re-enter field\n")
            multi = reddit.multireddit(get_user(), feed_name)

        count = int(input("\nHow many items would you like to save? (max 100)\n"))
        while count > 100:
            count = int(input("\nPlease re-enter the number of items you would like to save (max 100)\n"))
            while count < 1:
                count = int(input("\nPlease re-enter the number of items you would like to save (min 1)\n"))

        while count < 1:
            count = int(input("\nPlease re-enter the number of items you would like to save (min 1)\n"))
            while count > 100:
                count = int(input("\nPlease re-enter the number of items you would like to save (max 100)\n"))

        hot_list = multi.hot()
        commands = (hot_list, count)
        return commands

    def unsave_write(self, to_write):
        self.write_to_screen(to_write)

    def unsave_read(self, reddit):
        count = int(input("\nHow many items would you like to unsave from saved items? (max 1000)\n"))
        while count < 1 or count > 1000:
            count = int(input("\nPlease re-enter the number of items you would like to unsave (from 1-1000)\n"))

        saved_list = reddit.user.me().saved(limit=count)
        commands = (saved_list, count)
        return commands

    def create_multi(self, reddit):
        multi = None
        feed_name = None

        while multi is None:
            feed_name = input("\nWhat would you like to name this new feed? (limit 50 characters)\n")
            # the name is not allowed to be longer than 50 characters (per Reddit custom feed name specifications)
            if not is_valid_multi_name(feed_name):
                self.send_error("The name chosen for the multi is invalid. It must be between 2-50 characters and "
                                "contain at least two alphanumeric characters. Please try again")
                continue
            # and also makes sure that the custom feed created doesn't already exist for the user
            try:
                multi = reddit.multireddit.create(display_name=feed_name, subreddits=[])
                break
            except Conflict:
                print("The custom feed with that name already exists on your account. Please choose a different name")
                continue
            except BadRequest:
                print(
                    "There was an unidentified error with the input. Likely do character types entered or to an "
                    "invalid config.ini file.")
                return None

        print("Successfully created an empty custom feed named %s\n" % feed_name)
        return multi

    def read_subreddits(self):
        """Method that reads in a list of subreddits from the user to be added to a custom feed"""
        # starts by asking the user for the number of subreddits they want to add
        subreddit_count = None
        while subreddit_count is None:
            try:
                subreddit_count = int(
                    input("Please enter the number of subreddit(s) you want to add to your collection!\n"))
                break
            # if the user input is not a valid number, then it keeps re-prompting the user
            except ValueError:
                print("Please enter an integer value!\n")
                continue

        # next, reads the number of lines for each subreddit and returns the list read
        subreddit_list = []
        print("\nPlease enter", subreddit_count, "subreddits, each followed by a new line.")
        for i in range(0, subreddit_count):
            # reads in a line the user enters and stores it in an array
            subreddit_list.append(input(""))
        return subreddit_list
