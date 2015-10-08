# public APIs
import praw
import sys

# custom imports
from redditobjects import *
from redditconfig import *

class RedditWrapper(object):
    praw_object = None

    def __init__(self, where_scrape):      
        RedditWrapper.praw_object = RedditWrapper.praw_object or  praw.Reddit(user_agent=where_scrape+"sunnysideworks.nyc")
        self.where_scrape = where_scrape
    def __enter__(self, *args):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def getThreads(self):
        if self.where_scrape == "front_page":
            return  RedditWrapper.praw_object.get_front_page(limit=TOP_REDDIT_LIMIT)       
        else:
            return  RedditWrapper.praw_object.get_subreddit(sys.argv[2]).get_hot(limit=SUBREDDIT_LIMIT)


    def map_func(self, thread):
        try:
            flat_comments = praw.helpers.flatten_tree(thread.comments)
        except:
            pass
        else:
            thread_details = RedditThreadDetailed( thread, flat_comments[:COMMENT_LIMIT], self)
            thread_details.get_comments_info()
            return thread_details.getDict()

    def get_user_comments(self, username):
        return self.praw_object.get_redditor(username).get_comments(limit=COMMENT_LIMIT)

    def get_user_submissions(self, username):
        return self.praw_object.get_redditor(username).get_submitted(limit=COMMENT_LIMIT)