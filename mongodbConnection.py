import pymongo
from pymongo import MongoClient 

cluster = MongoClient("mongodb+srv://<username>:<password>@tweets.drdld.mongodb.net/Data?retryWrites=true&w=majority")

db = cluster["Data"]
collection  = db["Tweets"]

# db.Tweets.createIndex({_id})
# db.Tweets.createIndex({Tweets:1},{unique:true})

def get_post(post):
    # collection.insert_one(post,upsert=True)
    collection.insert_one(post)
    # collection.createIndex({tweet:1}, {unique:true})
