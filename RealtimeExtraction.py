
import tweepy as tw
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime
import csv


consumer_key= 'qc8vFuKFgGzcoxbhAkREHxRoE'
consumer_secret= 'ui2u5ZnJYLPtBrTNMreRGIeRZBLwGoF1W9XPmdYvSVofWg6o6A'
access_token= '1429353996188196876-CBoTpX136goMmypFtgTk2WO4sqH0ZC'
access_token_secret= '2ETqV9DxxdlVqMEEDw9A9kbY2Dy4L4rtlOlpuAoVYuEXl'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


    
producer = KafkaProducer(bootstrap_servers="localhost:9092")
topic_name = 'fyp'

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
                print(tweet.full_text)
                producer.send(topic_name, str.encode(tweet.full_text))



get_twitter_data()


def periodic_work(interval):
    while True:
        get_twitter_data()
        sleep(interval)


periodic_work(60*0.1)
