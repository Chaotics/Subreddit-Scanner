from subreddit_bot import subredditBot 
from prawcore.exceptions import Conflict, BadRequest
from generic import get_user

class Terminal(subredditBot):
    def createWrite(self, toWrite):
        print(toWrite)

    def createRead(self, reddit):
        multi = self.createMulti(reddit)
        subreddit_list = self.read_subreddits()
        itemsRead = [subreddit_list, multi]
        return itemsRead
    




    def backupWrite(self, toWrite):
        print(toWrite)
    def backupRead(self, reddit):
        return self.createMulti(reddit)
   


    def mimicWrite(self, toWrite):
        print(toWrite)

    def mimicRead(self, reddit):
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




    def createMulti(self, reddit):
        multi = None
        feed_name = None

        while multi is None:
            feed_name = input("\nWhat would you like to name this new feed? (limit 50 characters)\n")
            # the name is not allowed to be longer than 50 characters (per Reddit custom feed name specifications)
            if len(feed_name) > 50:
                print("The maximum custom feed name length is 50 characters. The name you chose was %d characters long. Please try again" % len(feed_name))
                continue
            if len(feed_name) <= 1:
                print("The minimum custom feed name length is 1 character. The name you chose was %d characters long. Please try again" % len(feed_name))
                continue
            # and also makes sure that the custom feed created doesn't already exist for the user
            try:
                multi = reddit.multireddit.create(display_name=feed_name, subreddits=[])
                break
            except Conflict:
                print("The custom feed with that name already exists on your account. Please choose a different name")
                continue
        print("Successfully created an empty custom feed named %s\n" % feed_name)
        return multi
    
    
    def read_subreddits(self):
        """Method that reads in a list of subreddits from the user to be added to a custom feed"""
        # starts by asking the user for the number of subreddits they want to add
        subreddit_count = None
        while subreddit_count is None:
            try:
                subreddit_count = int(input("Please enter the number of subreddit(s) you want to add to your collection!\n"))
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
