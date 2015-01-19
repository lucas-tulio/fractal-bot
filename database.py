import pymysql

class Database:

  def __init__(self):

    # Read parameters
    f = open("db.conf", "r")
    db_host = f.readline().split("=")[1].rstrip("\n")
    db_port = f.readline().split("=")[1].rstrip("\n")
    db_user = f.readline().split("=")[1].rstrip("\n")
    db_password = f.readline().split("=")[1].rstrip("\n")
    db_schema = f.readline().split("=")[1].rstrip("\n")
    f.close()

    # Start database
    self.conn = pymysql.connect(host=db_host, port=int(db_port), user=db_user, passwd=db_password, db=db_schema, charset='utf8')
    self.cur = self.conn.cursor()
