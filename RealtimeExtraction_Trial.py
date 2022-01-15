
import tweepy as tw
from time import sleep
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime


consumer_key= 'qc8vFuKFgGzcoxbhAkREHxRoE'
consumer_secret= 'ui2u5ZnJYLPtBrTNMreRGIeRZBLwGoF1W9XPmdYvSVofWg6o6A'
access_token= '1429353996188196876-CBoTpX136goMmypFtgTk2WO4sqH0ZC'
access_token_secret= '2ETqV9DxxdlVqMEEDw9A9kbY2Dy4L4rtlOlpuAoVYuEXl'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# def normalize_timestamp(time):
#     mytime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
#     return (mytime.strftime("%Y-%m-%d%H:%M:%S"))
    
producer = KafkaProducer(bootstrap_servers="localhost:9092")
topic_name = 'trial'

def get_twitter_data():
    res = api.search_tweets("BCCI OR Sourav OR Ganguly")
    for i in res:
        record = ''
        record += str(i.user.id_str)
        record += ';'
        try:
            record += str(i.full_text)
            record += ';'
        except AttributeError:
            record += 'NONE'
            record += ';'
        record += str((i.created_at))
        record += ';'
        record += str(i.user.followers_count)
        record += ';'
        record += str(i.user.location)
        record += ';'
        record += str(i.favorite_count)
        record += ';'
        record += str(i.retweet_count)
        record += ';'
        producer.send(topic_name, str.encode(record))


get_twitter_data()


def periodic_work(interval):
    while True:
        get_twitter_data()
        sleep(interval)


periodic_work(60*0.1)
