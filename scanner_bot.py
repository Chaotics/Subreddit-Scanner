import configparser
import praw
import signal
import sys

#a signal handler to handle shutdown of the bot
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


def readSubreddits():
    subredditCount = None;
    while subredditCount is None:
        try:
            subredditCount = int(input("Please enter the number of subreddits you want to add to your collection!\n"))
            break;
        except ValueError:
            print("Please enter an integer value!\n")
            continue;
    subredditList = []
    print("\nPlease enter", subredditCount, "subreddits, each followed by a new line.")
    for i in range(0, subredditCount):
        #reads in a line the user enters and stores it in an array
        subredditList.append(input(""))
    return subredditList

def run_bot():
    """ Method that will run the Subreddit-Scanner bot """
    reddit = login()
    print("Logged in successfully...\n")

    subredditList = readSubreddits();
    print("\nGenerating custom feed for:")
    for subreddit in subredditList:
        print(subreddit)


    #at this point we have to choose where to store "subreddit list-> either locally in a file or in a database"
    #we must also take the list and check its validity -> create custom thread


if __name__ == '__main__':
    #sets up signal to be recognized by user
    signal.signal(signal.SIGINT, signal_handler)
    print('To close the bot please press Ctrl + C')
    run_bot()
    signal.pause() #this is currently here to show the functionality of the signal signal_handler
    #when we actually make the bot, it will run indefintely so this pause will not be necessary
