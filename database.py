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

  def __del__(self):
    self.cur.close()
    self.conn.close()

  #
  # Logs the Fractal of the Day
  #
  def logFotd(self, link, deleteHash, size):
    try:
      self.cur.execute("""INSERT INTO fotd (link, deletehash, size) values (%s, %s, %s)""", (link, deleteHash, int(size)))
      self.conn.commit()
    except Exception as e:
      print "Error logging fractal of the day: " + str(username)
      print e

  #
  # Check if we already sent a fractal to this user in the past x days
  #
  def canSend(username):
    try:
      self.cur.execute("""SELECT * FROM logs WHERE username = %s AND adddate(created_at, INTERVAL 1 DAY) >= now() """, username)
      result = self.cur.fetchone()
      if result is None:
        return True
      else:
        return False

    except Exception as e:
      print "Error running canSend: " + str(username)
      print e

    return False

  #
  # Log a reply
  #
  def saveSend(username):
    try:
      self.cur.execute("""INSERT INTO logs (username) values (%s)""", (username))
      self.conn.commit()
    except Exception as e:
      print "Error running saveSend: " + str(username)
    print e

  #
  # Check if the user is in the blacklist
  #
  def userIsInBlacklist(username):
    try:
      self.cur.execute("""SELECT username FROM blacklist WHERE username = %s""", username)
      result = self.cur.fetchone()
      if result is None:
        return False
      else:
        return True

    except Exception as e:
      print "Error running canSend: " + str(username)
      print e

    return False
