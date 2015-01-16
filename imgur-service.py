import pyimgur

def sendFractalOfTheDay():

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

  # Tweet
  