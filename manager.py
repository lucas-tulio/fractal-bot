import tweepy

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

# Read tweets
public_tweets = api.home_timeline()
for tweet in public_tweets:
  print tweet.id

