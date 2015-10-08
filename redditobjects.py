import time
from redditconfig import *

def get_dict_if_exists(obj):
    """Helper function for classes returning a dictionary representation
    for all properties"""
    try:
        return obj.getDict()
    except NameError:
        return obj
    except AttributeError:
        return obj

class RedditThread:
    """Represents the minimum information saved from a Reddist post"""

    # attributes to exclude from dictionary representation
    EXCLUDE = ("dictionary_representation", "dict", "reddit_conn")
    
    def __init__(self, post, flat_comments):       
        self.user = getattr(post.author, "name", post.author)
        self.title = getattr(post, "title")
        self.ups = getattr(post, "ups")
        self.created = getattr(post, "created")
        self.id_num = getattr(post, "id")
        self.comments = flat_comments
        self.subreddit = getattr(post.subreddit, 'display_name', post.subreddit)

    def __str__(self):
        return "class RedditThread Title: %s Subreddit: %s"%(self.title, self.subreddit)

    def dictionary_representation(self):
        return {key: get_dict_if_exists(val)
                for key, val in self.__dict__.items()
                if key not in self.EXCLUDE}

    
class RedditThreadDetailed(RedditThread):
    """Adds information about comments and users making those comments to base class RedditThread"""

    # attributes to exclude from dictionary representation
    EXCLUDE = ("dictionary_representation", "dict", "reddit_conn")

    def __init__(self, thread, flat_comments,  reddit_conn):
        RedditThread.__init__(self, thread, flat_comments)
        self.reddit_conn = reddit_conn
    
    def __str__(self):
        return "class RedditThread Title: %s Subreddit: %s First User Listed:%s"% \
            (self.title, self.subreddit, self.users[0].username)

    def dictionary_representation(self):
        return {key: get_dict_if_exists(val)
                for key, val in self.__dict__.items()
                if key not in self.EXCLUDE}

    def get_comments_and_commenters(self):
        """Get text of top comments and information about related user, 
        including the user's other recent comments and own submissions.
        Top comments are defined post-nesting representing what users see
        when opening the user page rather than the overall tree structure 
        of comments."""
        user_list = []
        comment_list = []
        for comment in self.comments:
            if comment is not None:
                if hasattr(comment, 'author') and comment.author is not None:               
                    try:
                        userObject = User(self.reddit_conn, comment.author.name)
                        time.sleep(TIME_SLEEP)
                        userObject.get_user_comments_and_posts()
                    except:
                        pass
                    else:
                        user_list.append(userObject.dictionary_representation())
                        comment_list.append(comment.body)

        self.users  = user_list
        self.comments = comment_list

class User:
    """Convenient wrapper to convert praw user to dictionary.
    Holds and retrieves user name, comments, and posts."""

    # attributes to exclude from dictionary representation    
    EXCLUDE = ("dictionary_representation", "dict", "reddit_conn")

    def __init__(self, reddit_conn, username):
        self.username = username
        self.reddit_conn = reddit_conn

    def __str__(self):
        return "class User, name is %s"%self.username

    def dictionary_representation(self):
        return {key: get_dict_if_exists(val)
                for key, val in self.__dict__.items()
                if key not in self.EXCLUDE}
    
    def get_user_comments_and_posts(self):
        self.get_comments()
        self.get_posts()
      
    def get_comments(self):
        self.comments =  []
        comments = self.reddit_conn.get_user_comments(self.username)
        for c in comments:
            subreddit_name = getattr(c.subreddit, 'display_name', c.subreddit)
            self.comments.append(Comment(c.created_utc, c.ups, subreddit_name).dictionary_representation())
       
    def get_posts(self):
        self.threads =  []
        threads = self.reddit_conn.get_user_submissions(self.username)
        for s in threads:
            self.threads.append(RedditThread(s, []).dictionary_representation())


class Comment:
    """Convenient wrapper to convert praw comment to dictionary."""

    # attributes to exclude from dictionary representation
    EXCLUDE = ("dictionary_representation", "dict", "reddit_conn")
    
    def __init__(self, time, ups, subreddit):
        self.time = time
        self.ups = ups
        self.subreddit = subreddit

    def __str__(self):
        return "class Comment, votes: %d, subreddit: %s, posted at: %d"%(self.ups, self.subreddit, self.time)

    def dictionary_representation(self):
        return {key: get_dict_if_exists(val)
                for key, val in self.__dict__.items()
                if key not in self.EXCLUDE}

