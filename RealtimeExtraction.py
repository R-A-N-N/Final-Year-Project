
import tweepy as tw
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import pymongo
from pymongo import MongoClient 
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import nltk 
import string
import re
import os
from model_traning import *
from mongodbConnection import *


# consumer_key= '<KEY>'
# consumer_secret= '<KEY>'
# access_token= '<KEY>'
# access_token_secret= '<KEY>'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

    
producer = KafkaProducer(bootstrap_servers="localhost:9092")
topic_name = 'fyp'

loaded_vectorizer = pickle.load(open('vectorizer.pickle', 'rb'))

    
def pre_process(tweet_str):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    str1 = emoji_pattern.sub(r'', tweet_str) # no emoji
    str1 = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",str1).split())
   
    # print(str1)
    return str1


def get_twitter_data():

    # getting the last value of the id from mongo db cluster 
    last_value = collection.find().sort([("_id", -1)]).limit(1)
    for doc in last_value:
    # print(last_value)
        print(doc)
        id1 = doc['_id']
        id1 += 1

  
    naive_bayes_from_pickle = pickle.loads(saved_model)
    csvFile = open('/Users/nidhivanjare/Documents/GitHub/Final-Year-Project/Extracted Data.csv', 'a')
    csvWriter = csv.writer(csvFile)

    # Define the search term and the date_since date as variables
    file = csv.reader(open('/Users/nidhivanjare/Documents/GitHub/Final-Year-Project/GeoNames.csv'), delimiter=',')
    
    for line in file:
        
        # print(line)
        str1 = ""
        for ele in line: 
            str1 += ele
            str1 + ", Thane"
            search_words = str1
            # print(search_words)

            # Collect tweets
            tweets = tw.Cursor(api.search_tweets,
                        q =search_words,
                        lang="en", count= 1 ,tweet_mode="extended").items()
            tweets
            # Iterate and print tweets
            
            for tweet in tweets:
            
                csvWriter.writerow([tweet.created_at, tweet.full_text ,tweet.user.screen_name , tweet.user.location])
                # print(tweet.full_text)
                producer.send(topic_name, str.encode(tweet.full_text))

                str2 = pre_process(tweet.full_text)
                print(str2)
                lst = [[str2]]
                # print(lst)
                df1 = pd.Series((v1[0] for v1 in lst))
                # print(df1)
                trial1 = loaded_vectorizer.transform(df1)
                # print(trial1)
                predict = naive_bayes_from_pickle.predict(trial1)
                # print(str2)
                print(predict)
                lst.clear()
                
                if (predict == '1'):
                    post = {"_id": id1, "tweet": tweet.full_text}
                    id1 = id1+1
                    get_post(post)

        
                
get_twitter_data()


def periodic_work(interval):
    while True:
        get_twitter_data()
        sleep(interval)


periodic_work(60*0.1)




