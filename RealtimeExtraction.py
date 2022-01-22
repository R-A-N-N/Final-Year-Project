
import tweepy as tw
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
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




consumer_key= 'qc8vFuKFgGzcoxbhAkREHxRoE'
consumer_secret= 'ui2u5ZnJYLPtBrTNMreRGIeRZBLwGoF1W9XPmdYvSVofWg6o6A'
access_token= '1429353996188196876-CBoTpX136goMmypFtgTk2WO4sqH0ZC'
access_token_secret= '2ETqV9DxxdlVqMEEDw9A9kbY2Dy4L4rtlOlpuAoVYuEXl'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


    
producer = KafkaProducer(bootstrap_servers="localhost:9092")
topic_name = 'fyp'


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
                        q=search_words,
                        lang="en", count= 1 ,tweet_mode="extended").items()
            tweets
            # Iterate and print tweets
            for tweet in tweets:
                csvWriter.writerow([tweet.created_at, tweet.full_text ,tweet.user.screen_name , tweet.user.location])
                # print(tweet.full_text)
                producer.send(topic_name, str.encode(tweet.full_text))

                str2 = pre_process(tweet.full_text)
                lst = [str2]
                df = pd.Series( (v[0] for v in lst) )
                trial1 = count_vector.transform(df)
                predict = naive_bayes.predict(trial1)
                # print(tweet.full_text)
                print(predict)



get_twitter_data()


def periodic_work(interval):
    while True:
        get_twitter_data()
        sleep(interval)


periodic_work(60*0.1)




