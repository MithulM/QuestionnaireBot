import discord
from discord.ext import commands

class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addQuestion(self, ctx):
        pass

    @commands.command()
    async def removeQuestion(self, ctx):
        pass

    @commands.command()
    async def points(self, ctx):
        pass

    @commands.command()
    async def startGame(self, ctx):
        pass

    @commands.command()
    async def endGame(self, ctx):
        pass

    @commands.command()
    async def join(self, ctx):
        pass

    @commands.command()
    async def leave(self, ctx):
        pass

    @commands.command()
    async def printQuestion(self, ctx):
        pass

    @commands.command()
    async def printAnswer(self, ctx):
        pass

    @commands.command()
    async def getData(self, ctx):
        pass




def setup(client):
    client.add_cog(BlackBoard(client))
