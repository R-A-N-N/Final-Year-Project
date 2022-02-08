import pymongo
from pymongo import MongoClient 

# cluster = MongoClient("mongodb+srv://<username>:<Password>@tweets.drdld.mongodb.net/Data?retryWrites=true&w=majority")

db = cluster["Data"]
collection  = db["Tweet"]

def get_post(post):
    # collection.insert_one(post,upsert=True)
    collection.insert_one(post)
    # collection.createIndex({tweet:1}, {unique:true})
