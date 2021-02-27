import discord
from discord.ext import commands

class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addQuestion(self, ctx):
        pass

    @commands.command()
    def removeQuestion(self, ctx):
        pass

    @commands.command()
    def points(self, ctx):
        pass

    @commands.command()
    def startGame(self, ctx):
        pass

    @commands.command()
    def endGame(self, ctx):
        pass

    @commands.command()
    def join(self, ctx):
        pass

    @commands.command()
    def leave(self, ctx):
        pass

    @commands.command()
    def printQuestion(self, ctx):
        pass

    @commands.command()
    def printAnswer(self, ctx):
        pass

    @commands.command()
    def getData(self, ctx):
        pass




def setup(client):
    client.add_cog(BlackBoard(client))
