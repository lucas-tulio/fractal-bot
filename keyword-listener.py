import tweepy, time, os, sys, json, random, pymysql
from tweepy import Stream
from tweepy.streaming import StreamListener

latestId = 0
sentences = [
  "Fractal?",
  "Here's your fractal",
  "Here, have a fractal",
  "I hope you like your fractal",
  "How about this fractal?",
  "I made this fractal just for you"
]

# Check if we already sent a fractal to this user in the past x days
def canSend(username):
  try:
    cur.execute("""SELECT * FROM logs WHERE adddate(created_at, INTERVAL 1 DAY) >= now() and username = %""", username)
    result = cur.fetchone()
    if result is None:
      return True
    else:
      return False

  except Exception as e:
    print "Error running canSend: " + str(username)
    print e

  return False

# Log
def saveSend(username):
  try:
    cur.execute("""INSERT INTO logs (username) values (%s)""", (username))
    conn.commit()
  except Exception as e:
    print "Error running saveSend: " + str(username)
    print e

# Check if the user is in the blacklist
def userIsInBlacklist(username):
  try:
    cur.execute("""SELECT username FROM blacklist WHERE username = %s""", username)
    result = cur.fetchone()
    if result is None:
      return False
    else:
      return True

  except Exception as e:
    print "Error running canSend: " + str(username)
    print e

  return False

def sendFractal(latestId, tweet):

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
    if mention["screen_name"] == "fractal_bot"
    isMention = True
    break

  if not isMention:
    return

  # Skip if it's one of those stupid youtube automatic tweets
  if "@YouTube" in tweet["text"] or "analytics" in tweet["text"] or "Analytics" in tweet["text"]:
    print "Skipping tweet to " + str(username)
    return

  # Skip if it's a retweet
  if "retweeted_status" in tweet:
    print "retweet, skipping"
    return
  print "not a retweet"

  # Check the already sent list
  if not canSend(username):
    print "already sent to this guy " + str(username)
    return
  else:
    saveSend(username)

  print "log to this user saved: " + str(username)

  # Check the blacklist
  if userIsInBlacklist(username):
    print "blacklist. Skipping user " + str(username)
    return

  print "not in blacklist"

  print "generating fractal to " + str(username)
  os.system("python generate.py")

  print "Sending tweet"
  latestId = tweet["id"]
  tweetUser = tweet["user"]
  sentence = random.choice(sentences)
  api.update_with_media("fractal.png", "@" + tweetUser["screen_name"] + " " + sentence, in_reply_to_status_id=latestId)
  print "done!"

class listener(StreamListener):
  def on_data(self, data):
    jsonData = json.loads(data)
    sendFractal(latestId, jsonData)
    return True
  def on_error(self, status):
    print "Error!"
    cur.close()
    conn.close()
    sys.exit()

# Read twitter and database parameters
# They should be in the order shown below and follow the format:
# parameter=value
f = open("bot.conf", "r")
consumer_key = f.readline().split("=")[1].rstrip("\n")
consumer_secret = f.readline().split("=")[1].rstrip("\n")
access_token = f.readline().split("=")[1].rstrip("\n")
access_token_secret = f.readline().split("=")[1].rstrip("\n")
db_host = f.readline().split("=")[1].rstrip("\n")
db_port = f.readline().split("=")[1].rstrip("\n")
db_user = f.readline().split("=")[1].rstrip("\n")
db_password = f.readline().split("=")[1].rstrip("\n")
db_schema = f.readline().split("=")[1].rstrip("\n")
f.close()

# Authenticate
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
stream = tweepy.Stream(auth, listener())

# Start database
conn = pymysql.connect(host=db_host, port=int(db_port), user=db_user, passwd=db_password, db=db_schema, charset='utf8')
cur = conn.cursor()

# Start reading stream
print "reading mentions"
stream.filter(track=["fractal_bot"])
