import configparser
import time

import praw
from prawcore.exceptions import BadRequest

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


def create_feed(reddit, subreddit_bot):
    """Method that creates a custom feed that the user requests"""
    # starts by prompting the user for a name for the custom feed
    subreddit_bot.reset_write()
    items_read = subreddit_bot.create_read(reddit)
    if items_read is None:
        return
    subreddit_list = items_read[0]
    multi = items_read[1]
    # next, the user is prompted for all the subreddits they want to add to the feed
    if subreddit_list:
        subreddit_bot.create_write("Adding the chosen subreddits to the custom feed\n")
    for subreddit in subreddit_list:
        # once the list of subreddits is fetched from the user, each of them is added to feed one by one
        try:
            multi.add(subreddit)
            subreddit_bot.create_write("Successfully added the subreddit '%s' to the feed" % subreddit)

        except BadRequest:
            # if adding the subreddit fails due to a BadRequest, it means that the subreddit provided wasn't valid
            # so the appropriate error message is printed
            subreddit_bot.send_error(
                "Failed to add the subreddit '%s' to the feed because it is not a valid subreddit" % subreddit)
    # finally, the link to the custom feed is output into the console so they can readily access it
    subreddit_bot.create_write(
        "\nFinished adding the given subreddits to the custom feed. In order to access it, visit:\n%s%s" % (
            REDDIT_URL, multi.path))


def backup_tofeed(reddit, subreddit_bot):
    subreddit_bot.reset_write()
    multi = subreddit_bot.backup_read(reddit)
    subreddit_bot.backup_write("Now copying subreddits over...\n")

    user_subreddits = reddit.user.subreddits()
    for subreddit in user_subreddits:
        multi.add(subreddit)
        subreddit_bot.backup_write("Copied %s" % str(subreddit))

    subreddit_bot.backup_write(
        "\nSuccessfully backed up subreddits! In order to access the backup visit:\n%s%s" % (REDDIT_URL, multi.path))


def mimic_feed(reddit, subreddit_bot):
    subreddit_bot.reset_write()
    correct_multi = subreddit_bot.mimic_read(reddit)
    subreddit_bot.mimic_write("Removing current subreddits...\n")
    user_subreddits = reddit.user.subreddits()
    for subreddit in user_subreddits:
        subreddit.unsubscribe()
        subreddit_bot.mimic_write("Removed %s" % str(subreddit))

    subreddit_bot.mimic_write("\nCopying subreddits over...\n")
    # TODO subscribe all at once
    subreddits_to_add = correct_multi.subreddits
    for subreddit in subreddits_to_add:
        subreddit.subscribe()
        subreddit_bot.mimic_write("Subscribed to %s" % str(subreddit))

    subreddit_bot.mimic_write("\nSuccessfully mimiced subreddits of the given feed!")


def save_hot(reddit, subreddit_bot):
    subreddit_bot.reset_write()
    commands = subreddit_bot.save_read(reddit)
    hot_list = commands[0]
    count = commands[1]
    subreddit_bot.save_write("Saving items...\n")
    try:
        i = 0
        for item in hot_list:
            subreddit_bot.save_write("Saved \"%s\"" % item.title)
            item.save()
            i += 1
            if i == count:
                break
    except:
        subreddit_bot.send_error("\nAn error has occurred, could not get items in multi requested.")
        return

    subreddit_bot.save_write("\nSuccessfully saved %d of the hottest topics\n" % count)
