import configparser
import praw
import signal
import sys
def signal_handler(sig, frame):
        print('Closing bot...')
        sys.exit(0)


def login():
    """Method used to login onto Reddit and obtain a praw.Reddit instance using the configuration within config.ini"""
    # utilizes a ConfigParser object to parse through the config.ini file
    config = configparser.ConfigParser()
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


def run_bot():
    """ Method that will run the Subreddit-Scanner bot """
    reddit = login()


if __name__ == '__main__':
    run_bot()
    signal.signal(signal.SIGINT, signal_handler)
    print('To close the bot please press Ctrl + C')
    signal.pause() #this is currently here to show the functionality of the signal signal_handler
    #when we actually make the bot, it will run indefintely so this pause will not be necessary
