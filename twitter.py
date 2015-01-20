import tweepy

class Twitter:

  def __init__(self):

    # Read parameters
    f = open("./conf/twitter.conf", "r")
    consumer_key = f.readline().split("=")[1].rstrip("\n")
    consumer_secret = f.readline().split("=")[1].rstrip("\n")
    access_token = f.readline().split("=")[1].rstrip("\n")
    access_token_secret = f.readline().split("=")[1].rstrip("\n")
    f.close()

    # Start the api
    self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    self.auth.set_access_token(access_token, access_token_secret)
    self.api = tweepy.API(self.auth)
