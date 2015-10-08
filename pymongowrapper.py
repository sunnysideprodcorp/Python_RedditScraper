from pymongo import MongoClient

class MongoDB(object):
    """Provides a RAII wrapper for PyMongo db connections.

    Available collection functions limited to those in
    attributes_to_pass. Number of simultaneous connection 
    users also tracked. """

    ATTRIBUTES_TO_PASS = ("update", "insert", "count")
    client = None #MongoClient()
    num_users = 0

    def __init__(self, db, collection):
        MongoDB.client = MongoDB.client or MongoClient()
        self.collection = MongoDB.client[db][collection]
        MongoDB.num_users += 1


    def __enter__(self, *args):
        return self

    def __exit__(self, type, value, traceback):
        MongoDB.num_users -= 1
        if MongoDB.num_users is 0:
            self.client.close()
        

    def __getattr__(self, attr):
        if attr in self.ATTRIBUTES_TO_PASS:
            return getattr(self.collection, attr)
        else:
            return getattr(self, attr)

def main():

    with MongoDB(db = "db1", collection = "c1") as m: 
        print(m.count())
        m.update({"jello":5} , {"hello":"you"}, upsert = True)
        print(m.count())
        m.insert({"joe":6})
        with MongoDB(db ='db1', collection = 'c2') as j:
            j.insert({"joe":6})
            print(j.count())

if __name__ == "__main__":
    main()
