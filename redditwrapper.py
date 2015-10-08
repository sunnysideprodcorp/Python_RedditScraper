# public APIs
import praw
import sys

# custom imports
from redditobjects import *
from redditconfig import *

class RedditWrapper(object):
    reddit_conn = None

    def __init__(self, where_scrape):      
        self.reddit_conn = self.reddit_conn or  praw.Reddit(user_agent=where_scrape+"sunnysideworks.nyc")
        self.where_scrape = where_scrape

    def __enter__(self, *args):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def get_threads(self):
        if self.where_scrape == "front_page":
            return self.reddit_conn.get_front_page(limit=TOP_REDDIT_LIMIT)       
        else:
            return self.reddit_conn.get_subreddit(sys.argv[2]).get_hot(limit=SUBREDDIT_LIMIT)

    def get_user_comments(self, username):
        return self.reddit_conn.get_redditor(username).get_comments(limit=COMMENT_LIMIT)

    def get_user_submissions(self, username):
        return self.reddit_conn.get_redditor(username).get_submitted(limit=COMMENT_LIMIT)

    def general_processing(self, thread):
        try:
            flat_comments = praw.helpers.flatten_tree(thread.comments)
        except:
            pass
        else:
            thread_details = RedditThreadDetailed(thread, flat_comments[:COMMENT_LIMIT], self)
            thread_details.get_comments_and_commenters()
            return thread_details.dictionary_representation()

