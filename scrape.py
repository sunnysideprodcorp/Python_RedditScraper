# stdlib imports
import calendar
from concurrent import futures
import time

# custom imports
from pymongowrapper import MongoDB
from redditwrapper import RedditWrapper
from redditconfig import *



with MongoDB(db = DB_NAME, collection = COLLECTION_NAME) as db:
    with RedditWrapper("front_page") as r:

        threads = r.getThreads()
        
        filter_doc = {"time_recorded" : calendar.timegm(time.gmtime())}
        list_ids = []
        
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            for t in executor.map(r.map_func, threads):
                print("in scrape.py")
                print(t)
                update_doc = {'$push':{"thread_list":t}}
                list_ids.append(t['id_num'])                
                db.update(filter_doc, update_doc, upsert=True)
                
        update_doc = {'$push':{"order":{'$each':list_ids}}}
        db.update(filter_doc, update_doc, upsert=True)


