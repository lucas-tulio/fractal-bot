from datetime import date
import pyimgur, tweepy, sys, pymysql

def logFractalOfTheDay(link, deleteHash, size):
  try:
    cur.execute("""INSERT INTO fotd (link, deletehash, size) values (%s, %s, %s)""", (link, deleteHash, int(size)))
    conn.commit()
  except Exception as e:
    print "Error logging fractal of the day: " + str(username)
    print e

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
print "deletion link: imgur.com/delete/" + str(image._delete_or_id_hash)

if image.link == "":
  print "no link"
  sys.exit(0)

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

# Start database
conn = pymysql.connect(host=db_host, port=int(db_port), user=db_user, passwd=db_password, db=db_schema, charset='utf8')
cur = conn.cursor()
logFractalOfTheDay(image.link, image._delete_or_id_hash, image.size)

# Tweet
api.update_with_media("fotd.png", "Fractal of the day " + str(image.link) + " #fractal")
print "done"
