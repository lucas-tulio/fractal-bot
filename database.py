import pymysql

class Database:

  def __init__(self):

    # Read parameters
    f = open("./conf/db.conf", "r")
    db_host = f.readline().split("=")[1].rstrip("\n")
    db_port = f.readline().split("=")[1].rstrip("\n")
    db_user = f.readline().split("=")[1].rstrip("\n")
    db_password = f.readline().split("=")[1].rstrip("\n")
    db_schema = f.readline().split("=")[1].rstrip("\n")
    f.close()

    # Start database
    self.conn = pymysql.connect(host=db_host, port=int(db_port), user=db_user, passwd=db_password, db=db_schema, charset='utf8')
    self.cur = self.conn.cursor()

  # Logs the Fractal of the Day
  def logFractalOfTheDay(self, link, deleteHash, size):
    try:
      self.cur.execute("""INSERT INTO fotd (link, deletehash, size) values (%s, %s, %s)""", (link, deleteHash, int(size)))
      self.conn.commit()
    except Exception as e:
      print "Error logging fractal of the day: " + str(username)
      print e
