#coding=utf8

from datetime import datetime
import peewee
from utils import dbpath

proxy_db = peewee.Proxy()


def init_close_db(old_func):
    def new_func(*args, **kwargs):
        # the db file can't be accessed by others
        #db = peewee.SqliteDatabase(dbpath, check_same_thread=True)
        #db = peewee.SqliteDatabase(dbpath, check_same_thread=False)
        #db = peewee.SqliteDatabase(dbpath, threadlocals=False)
        # OK, together with this proxy
        db = peewee.SqliteDatabase(dbpath, threadlocals=True)
        proxy_db.initialize(db)
        r = old_func(*args, **kwargs)
        proxy_db.initialize(None)
        return r
    return new_func


class XmlItem(object):
    def __init__(self, name):
        self.name = name.strip()
        self.score = 0
        self.create_time = datetime.now()
        self.access_time = datetime.now()

    def update_access_time(self):
        self.access_time = datetime.now()

    @init_close_db
    def convert(self):
        try:
            return Item.get(name=self.name)
        except:
            print "The word [%s] is in xml but not in db." % self.name


class Item(peewee.Model):
    name = peewee.CharField(primary_key=True)
    phonetic = peewee.CharField()
    meaning = peewee.TextField()
    example = peewee.TextField()

    class Meta:
        database = proxy_db

    def getattr(self, attr):
        return object.__getattribute__(self, attr)

    def setattr(self, attr, value):
        object.__setattr__(self, attr, value)

    def convert(self):
        return XmlItem(self.name)


if __name__ == '__main__':
    #Item.create_table()
    # create_table(True), fail silently if the table already exists
    Item.create_table(True)
