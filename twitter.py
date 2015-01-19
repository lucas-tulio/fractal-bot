import tweepy

class Twitter:

  def __init__(self):

    # Read parameters
    f = open("bot.conf", "r")
    consumer_key = f.readline().split("=")[1].rstrip("\n")
    consumer_secret = f.readline().split("=")[1].rstrip("\n")
    access_token = f.readline().split("=")[1].rstrip("\n")
    access_token_secret = f.readline().split("=")[1].rstrip("\n")
    f.close()

    # Start the api
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    self.api = tweepy.API(auth)
