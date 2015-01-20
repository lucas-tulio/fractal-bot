from datetime import date
import pyimgur

class Imgur:

  def __init__(self):

    # Get imgur params
    f = open("./conf/imgur.conf", "r")
    client_id = f.readline().split("=")[1].rstrip("\n")
    client_secret = f.readline().split("=")[1].rstrip("\n")
    f.close()

    # Start the imgur api
    self.api = pyimgur.Imgur(client_id=client_id, client_secret=client_secret)
