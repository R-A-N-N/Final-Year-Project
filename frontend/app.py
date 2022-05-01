# Entry point for flask
from flask import Flask, render_template, request
import subprocess as sp
from pymongo import MongoClient
from mongopass import mongopass

app = Flask("myapp")

client = MongoClient(mongopass)
db = client.Data
myCollection = db.Tweets

@app.route("/")
def my_home():

	tweets = (myCollection.find())
	return render_template('response.html', tweets=tweets)

if __name__ == "__main__":
	app.run()