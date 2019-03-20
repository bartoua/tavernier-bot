#!/bin/env python3
import sqlite3
from discord.ext import commands


class Tavernier(commands.Bot):

    def __init__(self, **attrs):
        super().__init__(command_prefix="|", self_bot=True)
        self.db = sqlite3.connect("db/tavernier.db")

    @classmethod
    def init(cls):
        curs = cls.db.cursor()
        try:
            curs.execute("SELECT count(*) from registry ")
            print(curs.fetchall())
        except sqlite3.ProgrammingError as e:
            cls.initdb()

    @classmethod
    def initdb(cls):
        curs = cls.db.cursor()




if __name__ == '__main__':
    Tavernier.init()
