import praw
import configparser
from prawcore.exceptions import Conflict, BadRequest

REDDIT_URL = "https://www.reddit.com"


def login():
    """Method used to login onto Reddit and obtain a praw.Reddit instance using the configuration within config.ini"""
    # utilizes a ConfigParser object to parse through the config.ini file
    config = configparser.ConfigParser(interpolation=None)
    config.read("config.ini")

    # fetches the required config options in order to ensure that the bot can function
    user_agent = config["DEFAULT"]["user_agent"]
    client_id = config["DEFAULT"]["client_id"]
    client_secret = config["DEFAULT"]["client_secret"]
    username = config["DEFAULT"]["username"]
    password = config["DEFAULT"]["password"]

    # verifies that none of the required configuration options for login were left blank
    if '' in [user_agent, client_id, client_secret, username, password]:
        raise Exception("One or more of the required configuration options were left empty")

    # returns the created Reddit instance
    return praw.Reddit(user_agent=user_agent,
                       client_id=client_id,
                       client_secret=client_secret,
                       username=username,
                       password=password)


def get_user():
    # utilizes a ConfigParser object to parse through the config.ini file to get the username
    config = configparser.ConfigParser()
    config.read("config.ini")

    return config["DEFAULT"]["username"]




def create_feed(reddit, subredditBot):
    """Method that creates a custom feed that the user requests"""
    # starts by prompting the user for a name for the custom feed
    itemsRead = subredditBot.createRead(reddit)

    subreddit_list = itemsRead[0]
    multi = itemsRead[1]
    # next, the user is prompted for all the subreddits they want to add to the feed
    
    print("\nAdding the chosen subreddits to the custom feed\n")
    for subreddit in subreddit_list:
        # once the list of subreddits is fetched from the user, each of them is added to feed one by one
        try:
            multi.add(subreddit)
            subredditBot.createWrite("Successfully added the subreddit '%s' to the feed" % subreddit)
            
        except BadRequest:
            # if adding the subreddit fails due to a BadRequest, it means that the subreddit provided wasn't valid
            # so the appropriate error message is printed
            subredditBot.createWrite("Failed to add the subreddit '%s' to the feed because it is not a valid subreddit" % subreddit)

    # finally, the link to the custom feed is output into the console so they can readily access it
    subredditBot.createWrite("\nFinished adding the given subreddits to the custom feed. In order to access it, visit:\n%s%s" % (REDDIT_URL, multi.path))


def backup_tofeed(reddit, subredditBot):
    multi = subredditBot.backupRead(reddit)
    # print("Now copying subreddits over...")

    # userSubreddits = reddit.user.subreddits()
    # for subreddit in userSubreddits:
    #     multi.add(subreddit)
    #     subredditBot.backupWrite(subreddit)

    # subredditBot.backupWrite("\nSuccessfully backed up subreddits! In order to access the backup visit:\n%s%s" % (REDDIT_URL, multi.path))

def mimic_feed(reddit, subredditBot):
    correct_multi = subredditBot.mimicRead(reddit)
    print("\nRemoving current subreddits...")
    user_subreddits = reddit.user.subreddits()
    for subreddit in user_subreddits:
        subreddit.unsubscribe()
        print(subreddit)

    print("\nCopying subreddits over...")
    #TODO subscribe all at once
    subreddits_to_add = correct_multi.subreddits
    for subreddit in subreddits_to_add:
        subreddit.subscribe()
        print(subreddit)



def save_hot(reddit, subredditBot):
    feed_name = input("\nWhat feed would you like to save?\n")
    multi = reddit.multireddit(get_user(), feed_name)
    while multi is None:
        feed_name = input("\nFeed invalid, please re-enter field\n")
        multi = reddit.multireddit(get_user(), feed_name)
    count = int(input("\nHow many items would you like to save? (max 100)\n"))
    while(count > 100):
        count = int(input("\nPlease re-enter the number of items you would like to save (max 100)\n"))
    list = multi.hot()

    print("Saving items...")
    try:
        i = 0
        for item in list:
            print(item.title)
            item.save()
            i += 1
            if i == count:
                break
    except:
        print("\nAn error has occured, could not get items in multi requested")
        return

    print("Saved successfully!\n")
