import pyimgur

# Get imgur params
imgurFile = open("imgur.conf", "r")
clientId = imgurFile.readline().split("=")[1].rstrip("\n")
clientSecret = imgurFile.readline().split("=")[1].rstrip("\n")
imgurFile.close()

# Upload
imgur = pyimgur.Imgur(client_id=clientId, client_secret=clientSecret)
today = date.today()
image = imgur.upload_image("fotd.png", title="Fractal of the day - " + str(today))
print(image.title)
print(image.link)
print(image.size)
print(image.type)

# Twitter settings
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

# Tweet
api.update("Fractal of the day " + str(image.link))
print "done"