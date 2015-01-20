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

def send_fractal(tweet):

  print "got one"

  # Don't do anything if it's our own tweet
  tweet_id = tweet["id"]
  tweet_user = tweet["user"]
  username = tweet_user["screen_name"]
  if username == "fractal_bot":
    print "not sending one to myself"
    return

  # Check if it's a mention
  entities = tweet["entities"]
  user_mentions = entities["user_mentions"]
  is_mention = False
  for mention in user_mentions:
    if mention["screen_name"] == "fractal_bot":
      print "mentions " + str(mention["screen_name"])
      is_mention = True
      print "mention!"
      break
  if not is_mention:
    print "not a mention"
    return

  # Skip if it's a retweet
  if "retweeted_status" in tweet:
    print "retweet, skipping"
    return
  print "not a retweet"

  # Check the already sent list
  if not db.can_send(username):
    print "already sent to this guy " + str(username)
    return
  else:
    db.save_send(username)

  print "log to this user saved: " + str(username)

  # Check the blacklist
  if db.is_user_in_blacklist(username):
    print "blacklist. Skipping user " + str(username)
    return

  print "not in blacklist"

  print "generating fractal to " + str(username)
  fractal.generate()

  print "Sending tweet"
  sentence = random.choice(sentences)
  twitter.api.update_with_media("fractal.png", "@" + username + " " + sentence, in_reply_to_status_id=tweet_id)
  print "done!"

class Listener(StreamListener):
  def on_data(self, data):
    json_data = json.loads(data)
    send_fractal(json_data)
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
