#!/bin/env python3
#import sqlite3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import sys


sys.path.append('./resources')
from discord.ext import commands


class Tavernier(commands.Bot):

    def __init__(self, **attrs):
        super().__init__(command_prefix="|", self_bot=True)
        self.db = create_engine('sqlite://db/tavernier.db')

    def __del__(self):
        self.db.close()

    def init(self):
        curs = self.db.cursor()
        try:
            curs.execute("SELECT count(*) from registry ")
            print(curs.fetchall())
        except sqlite3.OperationalError as e:
            print("Installing DB")
            curs.close()
            self.initdb()

    def initdb(self):
        import sys
        sys.path.append('./resources')
        from initdatabases import creates
        print(creates)
        curs = self.db.cursor()
        try:
            for table in creates:
                col = ""
                for column in table['structure']:
                    col += column + ","
                sql = "CREATE TABLE " + table['name'] + "(" + col[:-1] + ")"
                curs.execute(sql)
            self.populatedb()
        except sqlite3.DatabaseError as e:
            print(e)

#    def populatedb(self):


Base = declarative_base()


class Registry(Base):
    __tablename__ = 'registry'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)

    def __repr__(self):

if __name__ == '__main__':
    tavernier = Tavernier()
    tavernier.init()
