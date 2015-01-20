import tweepy, time, os, sys, json, random, pymysql
from tweepy import Stream
from tweepy.streaming import StreamListener
from database import Database
from twitter import Twitter
from fractal import Fractal

sentences = [
  "Fractal?",
  "Here's your fractal",
  "Here, have a fractal",
  "I hope you like your fractal",
  "How about this fractal?",
  "I made this fractal just for you"
]

def sendFractal(tweet):

  print "got one"

  # Don't do anything if it's our own tweet
  tweetUser = tweet["user"]
  username = tweetUser["screen_name"]
  if username == "fractal_bot":
    print "not sending one to myself"
    return

  # Check if it's a mention
  entities = tweet["entities"]
  userMentions = entities["user_mentions"]
  isMention = False
  for mention in userMentions:
    if mention["screen_name"] == "fractal_bot":
      isMention = True
      print "mention!"
      break
  if not isMention:
    print "not a mention"
    return

  # Skip if it's a retweet
  if "retweeted_status" in tweet:
    print "retweet, skipping"
    return
  print "not a retweet"

  # Check the already sent list
  if not db.canSend(username):
    print "already sent to this guy " + str(username)
    return
  else:
    db.saveSend(username)

  print "log to this user saved: " + str(username)

  # Check the blacklist
  if db.userIsInBlacklist(username):
    print "blacklist. Skipping user " + str(username)
    return

  print "not in blacklist"

  print "generating fractal to " + str(username)
  fractal.generate()

  print "Sending tweet"
  tweetId = tweet["id"]
  tweetUser = tweet["user"]
  sentence = random.choice(sentences)
  twitter.api.update_with_media("fractal.png", "@" + tweetUser["screen_name"] + " " + sentence, in_reply_to_status_id=tweetId)
  print "done!"

class Listener(StreamListener):
  def on_data(self, data):
    jsonData = json.loads(data)
    sendFractal(jsonData)
    return True
  def on_error(self, status):
    print "Error!"
    cur.close()
    conn.close()
    sys.exit()

# Start Fractal generator
fractal = Fractal()

# Start Twitter
twitter = Twitter()
stream = Stream(twitter.auth, Listener())

# Start database
db = Database()

# Start reading stream
print "reading mentions"
stream.filter(track=["fractal_bot"])
