#!/bin/env python3
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from discord.ext import commands
import asyncio
import sys
import git


class Tavernier(commands.Bot):

    def __init__(self, **attrs):
        self.prefix = "$"
        super().__init__(command_prefix=self.prefix)
        self.db = create_engine('sqlite:///db/tavernier.db')
        clientid = self.initdb()
        self.add_command(self.hello)
        self.add_command(self.ping)
        self.add_command(self.gohome)
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

    def triggeredresponse(self):
        sys.path.append("resources")
        import response
        return response.response

    @staticmethod
    def update():
        g = git.cmd.Git(".")
        g.pull()

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """T'envoie manger tes morts"""
        await self.reply("mange tes morts bâtard")

    @commands.command(pass_context=True)
    async def hello(self, ctx):
        """Dit hello"""
        await self.send_message(ctx.message.channel, "hello " + ctx.message.author.display_name)

    @commands.command(pass_context=True, name="goHome")
    async def gohome(self, ctx):
        """Redémarre ou éteint le tavernier"""
        await self.send_message(ctx.message.channel, "Petit update d'abord ?")
        self.update()
        await self.send_message(ctx.message.channel, "Ciao les nazes !")
        await self.logout()

    @asyncio.coroutine
    async def on_message(self, msg):
        if msg.author != msg.server.me:
            if not msg.content.startswith(self.prefix):
                resp = self.triggeredresponse()
                for word in msg.content.split():
                    print(word)
                    if word in resp.keys():
                        print(word + "-->" + resp[word])
                        await self.send_message(msg.channel, resp[word])
                        break
            else:
                await self.process_commands(msg)


if __name__ == '__main__':
    tavernier = Tavernier()
