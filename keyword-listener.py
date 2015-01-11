import tweepy, time, os, sys, json, random, pymysql
from tweepy import Stream
from tweepy.streaming import StreamListener

latestId = 0
sentences = [
  "Fractal?",
  "Here's your fractal",
  "Here, have a fractal",
  "Your fractal is right here",
  "I hope you like your fractal"
]

def canSend(username): # Check if we already sent a fractal to this user today
  try:
    cur.execute("""SELECT * FROM logs WHERE adddate(created_at, INTERVAL 1 DAY) >= now() and username = %s""", username)
    result = cur.fetchone()
    print "can send query result"
    print result
    if result is None:
      return True
    else:
      return False

  except Exception as e:
    print "Error running canSend: " + str(username)
    print e

  return False

def saveSend(username): # Save
  try:
    cur.execute("""INSERT INTO logs (username) values (%s)""", (username))
    conn.commit()
  except Exception as e:
    print "Error running saveSend: " + str(username)
    print e

def sendFractal(latestId, tweet):

  print "got one"

  # Don't do anything if it's our own tweet
  tweetUser = tweet["user"]
  username = tweetUser["screen_name"]
  if username == "fractal_bot":
    return

  # Check the already sent list
  if not canSend(username):
    print "already sent to this guy " + str(username)
    return
  else:
    saveSend(username)

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

# Read the twitter auth parameters. They should be in the order shown below and
# follow the format: parameter=value
f = open("config.txt", "r")
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

# Start reading mention stream
print "reading tweets containing 'fractal' or 'mandelbrot'..."
stream.filter(track=["fractal", "mandelbrot"])
