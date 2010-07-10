from twisted.enterprise import adbapi

from twistar import DBObject
from twistar.dbconfig import Registry


class User(DBObject):
    HASMANY = ['pictures']
    HASONE = ['avatar']
    HABTM = ['favorite_colors']

class Picture(DBObject):
    BELONGSTO = ['user']

class Avatar(DBObject):
    pass

class FavoriteColors(DBObject):
    HABTM = ['users']    

class FakeObject(DBObject):
    pass

Registry.register(Picture, User, Avatar, FakeObject)


def initDB(location):
    Registry.DBPOOL = adbapi.ConnectionPool('sqlite3', location, check_same_thread=False)
    def runInitTxn(txn):
        txn.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       first_name TEXT, last_name TEXT, age INTEGER)""")
        txn.execute("""CREATE TABLE avatars (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,
                       color TEXT, user_id INTEGER)""")        
        txn.execute("""CREATE TABLE pictures (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,
                       size INTEGER, user_id INTEGER)""")
    return Registry.DBPOOL.runInteraction(runInitTxn)