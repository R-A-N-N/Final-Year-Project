import pymongo
from pymongo import MongoClient 

def get_post(post):
    cluster = MongoClient("mongodb+srv://<username>:<password>@<luserName>.drdld.mongodb.net/<Database_Name>?retryWrites=true&w=majority")

    db = cluster["Data"]
    collection  = db["Tweets"]

    collection.insert_one(post)
