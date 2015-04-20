import tweepy, time, os, sys, json, random, pymysql
from tweepy import Stream
from tweepy.streaming import StreamListener
from database import Database
from twitter import Twitter
from fractal import Fractal
from datetime import datetime

sentences = [
  "Fractal?",
  "Here's your fractal",
  "Here, have a fractal",
  "I hope you like your fractal",
  "How about this fractal?",
  "I made this fractal just for you"
]

def log(text):
  print(str(datetime.now()) + ": " + str(text))

def send_fractal(tweet):

  log("got one")

  # Don't do anything if it's our own tweet
  tweet_id = tweet["id"]
  tweet_user = tweet["user"]
  username = tweet_user["screen_name"]
  if username == "fractal_bot":
    log("not sending one to myself")
    return

  # Check if it's a mention
  entities = tweet["entities"]
  user_mentions = entities["user_mentions"]
  is_mention = False
  for mention in user_mentions:
    if mention["screen_name"] == "fractal_bot":
      log("mentions " + str(mention["screen_name"]))
      is_mention = True
      log("mention!")
      break
  if not is_mention:
    log("not a mention")
    return

  # Skip if it's a retweet
  if "retweeted_status" in tweet:
    log("retweet, skipping")
    return
  log("not a retweet")

  # Check the already sent list
  if not db.can_send(username):
    log("already sent to this guy " + str(username))
    return
  else:
    db.save_send(username)

  log("log to this user saved: " + str(username))

  # Check the blacklist
  if db.is_user_in_blacklist(username):
    log("blacklist. Skipping user " + str(username))
    return

  log("not in blacklist")

  log("generating fractal to " + str(username))
  fractal.generate()

  log("Sending tweet")
  sentence = random.choice(sentences)
  twitter.api.update_with_media("fractal.png", "@" + username + " " + sentence, in_reply_to_status_id=tweet_id)
  log("done!")

class Listener(StreamListener):
  def on_data(self, data):
    json_data = json.loads(data)
    send_fractal(json_data)
    return True
  def on_error(self, status):
    log("Error!")
    log(status)
    db._disconnect()
    sys.exit()
  def on_timeout(self):
    log("Timed out")
    return True
  def on_disconnect(self, notice):
    log("disconnected")
    log(str(notice))
    return

# Start Fractal generator
fractal = Fractal()

# Start database
db = Database()

# Start Twitter
twitter = Twitter()
stream = Stream(twitter.auth, Listener())

# Start reading stream
log("reading mentions")
stream.filter(track=["fractal_bot"])
log("script stopped running")
