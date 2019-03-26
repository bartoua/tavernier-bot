#!/bin/env python3
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from discord.ext import commands


class Tavernier(commands.Bot):

    def __init__(self, **attrs):
        super().__init__(command_prefix="$")
        self.db = create_engine('sqlite:///db/tavernier.db')
        clientid = self.initdb()
        self.add_command(self.hello)
        self.add_command(self.ping)
        self.run(clientid)

    def initdb(self):
        metadata = MetaData()
        self.registry = Table('registry', metadata,
                              Column('id', Integer, primary_key=True),
                              Column('name', String),
                              Column('value', String)
                              )
        metadata.create_all(self.db)
        toto = self.registry.select().where(self.registry.c.name == "clientid")
        res = self.db.execute(toto)
        clientid = res.fetchall()[0][2]
        return clientid

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        await self.reply("mange tes morts bâtard")

    @commands.command(pass_context=True)
    async def hello(self, ctx):
        await self.send_message(ctx.message.channel, "hello " + ctx.message.author.display_name)


if __name__ == '__main__':
    tavernier = Tavernier()
