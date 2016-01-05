import pymysql

class Database:

  def __init__(self):

    self.cur = None
    self.conn = None

    # Read parameters
    f = open("./conf/db.conf", "r")
    self.db_host = f.readline().split("=")[1].rstrip("\n")
    self.db_port = f.readline().split("=")[1].rstrip("\n")
    self.db_user = f.readline().split("=")[1].rstrip("\n")
    self.db_password = f.readline().split("=")[1].rstrip("\n")
    self.db_schema = f.readline().split("=")[1].rstrip("\n")
    f.close()

  def __del__(self):
    self._disconnect()

  def _connect(self):
    self.conn = pymysql.connect(host=self.db_host, port=int(self.db_port), user=self.db_user, passwd=self.db_password, db=self.db_schema, charset='utf8')
    self.cur = self.conn.cursor()

  def _disconnect(self):
    if self.cur != None:
      self.cur.close()
    if self.conn != None:
      self.conn.close()

  #
  # Logs the Fractal of the Day
  #
  def log_fotd(self, link, delete_hash, size):
    self._connect()
    try:
      self.cur.execute("""INSERT INTO fotd (link, deletehash, size) VALUES (%s, %s, %s)""", (link, delete_hash, int(size)))
      self.conn.commit()
    except Exception as e:
      print("Error logging fractal of the day")
      print(e)
    self._disconnect()

  #
  # Check if we already sent a fractal to this user in the past x days
  #
  def can_send(self, username):
    self._connect()
    try:
      self.cur.execute("""SELECT * FROM logs WHERE username = %s AND adddate(created_at, INTERVAL 1 DAY) >= now() """, username)
      result = self.cur.fetchone()
      if result is None:
        return True
      else:
        return False

    except Exception as e:
      print("Error running can_send for " + str(username))
      print(e)

    self._disconnect()
    return False

  #
  # Log a reply
  #
  def save_send(self, username):
    self._connect()
    try:
      self.cur.execute("""INSERT INTO logs (username) VALUES (%s)""", (username))
      self.conn.commit()
    except Exception as e:
      print("Error running save_send for " + str(username))
      print(e)
    self._disconnect()

  #
  # Check if the user is in the blacklist
  #
  def is_user_in_blacklist(self, username):
    self._connect()
    try:
      self.cur.execute("""SELECT username FROM blacklist WHERE username = %s""", username)
      result = self.cur.fetchone()
      if result is None:
        return False
      else:
        return True

    except Exception as e:
      print("Error running blacklist check for " + str(username))
      print(e)

    self._disconnect()
    return False
