import pymongo
from pymongo import MongoClient 

cluster = MongoClient("mongodb+srv://<username>:<password>@tweets.drdld.mongodb.net/Data?retryWrites=true&w=majority")

db = cluster["Data"]
collection  = db["Tweets"]

# db.Tweets.createIndex({_id})
collection.create_index('tweet', unique = True) 
# collection.create_index('tweet', unique = True) 

def get_post(post):

    try:
        # collection.insert_one(post,upsert=True)
        collection.insert_one(post)
        # collection.createIndex({tweet:1}, {unique:true})
    except pymongo.errors.DuplicateKeyError:
        pass

