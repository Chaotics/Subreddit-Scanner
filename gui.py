from subreddit_bot import subredditBot 
from sys import stderr
from prawcore.exceptions import Conflict, BadRequest
from generic import get_user


class guiInterface(subredditBot):
    multiName = ""
    subreddit_list = []
    subreddit_string = None
    numberOfItems = 0
    guiItemToWriteTo = None
    

    def sendError(self, error):
        stderr.write(error)

    def createWrite(self, toWrite):
        print(toWrite)
    
    def createRead(self, reddit):
        self.subreddit_list = (self.subreddit_string).split(',')
        print(self.subreddit_list)
        multi = self.createMulti(reddit)            
        itemsRead = [self.subreddit_list, multi]   
        return itemsRead 

    def backupWrite(self, toWrite):
        print(toWrite)
    
    def backupRead(self, reddit):
        return self.createMulti(reddit)


    def mimicWrite(self, toWrite):
        print(toWrite)
    
    def mimicRead(self, reddit):
        feed_name = self.multiName

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
            #The following must be sent to the screen somehow! we should re-take the input and somehow stop the current process
            feed_name = input("\nPlease enter a feed you own!\n")
            break
        
        return correct_multi


    def saveWrite(self, toWrite):
        print(toWrite)
    
    def saveRead(self, reddit):
        feed_name = self.multiName
        multi = reddit.multireddit(get_user(), feed_name)
        #old wa to check validity of the multi name, we must do this in the gui
        # while multi is None:
        #     feed_name = input("\nFeed invalid, please re-enter field\n")
        #     multi = reddit.multireddit(get_user(), feed_name)
        count = self.numberOfItems
        # while(count > 100):
        #     count = int(input("\nPlease re-enter the number of items you would like to save (max 100)\n"))
        list = multi.hot()
        commands = [list, count]
        return commands

    
    def createMulti(self, reddit):
        multi = None
        feed_name = self.multiName
        while multi is None:
            try:
                multi = reddit.multireddit.create(display_name=feed_name, subreddits=[])
                break
            except Conflict:
                #TODO
                print("This occured")
                #should send to the screen an error dialog here and somehow get the users data again
                return multi
                #continue
        return multi


