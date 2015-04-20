import pyimgur, tweepy, sys, pymysql
from datetime import date
from imgur import Imgur
from database import Database
from twitter import Twitter
from fractal import Fractal

# Generate the Fractal of the Day
fract = Fractal()
fract.generate(fotd=True)

# Upload
im = Imgur()
image = im.api.upload_image("fotd.png", title="Fractal of the day (1080p) - " + str(date.today()))
print(image.title)
print(image.link)
print(image.size)
print(image.type)
print "deletion link: imgur.com/delete/" + str(image._delete_or_id_hash)

if image.link == "":
  print("no link")
  sys.exit(0)

# Log the Fractal of the Day
db = Database()
db.log_fotd(image.link, image._delete_or_id_hash, image.size)

# Tweet
twitter = Twitter()
twitter.api.update_with_media("fotd.png", "Fractal of the day " + str(image.link) + " #fractal")
print("done")
