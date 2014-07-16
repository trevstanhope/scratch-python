import os
import sys
import time
import reddit
from reddit.objects import Redditor, Submission

__author__ = 'Trevor Stanhope'
__version__ = '0.1'

class RedditBot(object):

    def __init__(self, uname, passwd, target):
        self.api = reddit.Reddit(user_agent='ibelievenot')
        self.api.login(uname, passwd)
        self.count = 0
        self.redditor = self.api.get_redditor(target, fetch=False)

    def run(self):
        for post in self.redditor.get_overview():
            try:
                post.downvote()
                print "Downvoted: %s" % post.__unicode__()
                self.count += 1
            except:
                exception('Cannot upvote!')
            time.sleep(2)

def main(target):
    bot = RedditBot('ibelievenot', '$7@Nh0p3', target)
    try:
        bot.run()
    except:
        raise
    finally:
        print('All done! Downvoted %d submissions/comments!' %bot.count)
    return 0

if __name__ == '__main__':
    target = sys.argv[-1]
    sys.exit(main(target))
