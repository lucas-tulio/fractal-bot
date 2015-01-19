from datetime import date
import pyimgur

class Imgur:

  def __init__(self):

    # Get imgur params
    f = open("./conf/imgur.conf", "r")
    clientId = f.readline().split("=")[1].rstrip("\n")
    clientSecret = f.readline().split("=")[1].rstrip("\n")
    f.close()

    # Start the imgur api
    self.api = pyimgur.Imgur(client_id=clientId, client_secret=clientSecret)
