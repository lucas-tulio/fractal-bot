import tweepy
import time
import os
import sys
from tweepy import Stream
from tweepy.streaming import StreamListener
import json

latestId = 0

def sendFractal(latestId, tweet):

  print "got one"
  if latestId == 0 or latestId != tweet["id"]:
  
    print "this is a new one! Generating fractal..."
    tweetText = tweet["text"]

    parameters = tweetText[13:]

    fractalType = parameters[:10]
    if fractalType == "mandelbrot":
      fractalType = "mandelbrot"
    else:
      fractalType = parameters[:5]
      if fractalType == "julia":
        fractalType = "julia"
      else:
        fractalType = "mandelbrot"

    os.system("python " + fractalType + ".py " + parameters)

    print "Sending tweet"
    latestId = tweet["id"]
    tweetUser = tweet["user"]
    api.update_with_media(fractalType + ".png", "@" + tweetUser["screen_name"] + " Here's your fractal", in_reply_to_status_id=latestId)
    print "done!"

class listener(StreamListener):
  def on_data(self, data):
    jsonData = json.loads(data)
    sendFractal(latestId, jsonData)
    return True
  def on_error(self, status):
    print "Error!"
    sys.exit()

# Read parameters. They should be in the order shown below and
# follow the format: parameter=value
f = open("config.txt", "r")
consumer_key = f.readline().split("=")[1].rstrip("\n")
consumer_secret = f.readline().split("=")[1].rstrip("\n")
access_token = f.readline().split("=")[1].rstrip("\n")
access_token_secret = f.readline().split("=")[1].rstrip("\n")
f.close()

# Authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
stream = tweepy.Stream(auth, listener())

# Start reading mention stream
print "reading mentions..."
stream.filter(track=["@fractal_bot"])
