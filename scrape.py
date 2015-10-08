# stdlib imports
import calendar
from concurrent import futures
import time

# custom imports
from pymongowrapper import MongoDB
from redditwrapper import RedditWrapper
from redditconfig import *


#set up database and reddit connections
with MongoDB(db = DB_NAME, collection = COLLECTION_NAME) as db:
    with RedditWrapper("front_page") as r:

        # scrape according to params in redditconfig
        threads = r.get_threads()
        
        # iterate through each thread, get more details, insert into database
        filter_doc = {"time_recorded" : calendar.timegm(time.gmtime())}
        list_ids = []       
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            for t in executor.map(r.general_processing, threads):
                update_doc = {'$push':{"thread_list":t}}
                list_ids.append(t['id_num'])                
                #each record pushed individually but all go to same record indicated by filter_doc
                db.update(filter_doc, update_doc, upsert=True)
                
        #finally add an overall list of the ordering to the same record for ease of use
        update_doc = {'$push':{"order":{'$each':list_ids}}}
        db.update(filter_doc, update_doc, upsert=True)


