import tweepy, time, os, sys, json, random
from tweepy import Stream
from tweepy.streaming import StreamListener

latestId = 0
sentences = [
  "Fractal?",
  "Did you just say \"fractal\"?",
  "Here's your fractal",
  "Here, have a fractal",
  "Your fractal is right here",
  "I hope you like your fractal!"
]

def sendFractal(latestId, tweet):

  print "got one"

  # Don't do anything if it's our own tweet
  tweetUser = tweet["user"]
  username = tweetUser["screen_name"]
  if username == "fractal_bot":
    return

  fractalType = ""
  if bool(random.getrandbits(1)):
    fractalType = "mandelbrot"
  else:
    fractalType = "julia"

  os.system("python " + fractalType + ".py")

  print "Sending tweet"
  latestId = tweet["id"]
  tweetUser = tweet["user"]
  sentence = random.choice(sentences)
  api.update_with_media(fractalType + ".png", "@" + tweetUser["screen_name"] + " " + sentence, in_reply_to_status_id=latestId)
  print "done!"

class listener(StreamListener):
  def on_data(self, data):
    jsonData = json.loads(data)
    sendFractal(latestId, jsonData)
    return True
  def on_error(self, status):
    print "Error!"
    sys.exit()

# Read the twitter auth parameters. They should be in the order shown below and
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
print "reading tweets containing 'fractal' or 'mandelbrot'..."
stream.filter(track=["fractal", "mandelbrot"])
