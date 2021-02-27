import discord
from collections import defaultdict
from discord.ext import commands

class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.questionFiles = defaultdict()
        self.client = client
        self.defaultFile = None

    @commands.command()
    async def add(self, ctx, question, answer):
        self.questionFiles[question] = answer
        embed = discord.Embed(title=f'Question added',
                              description=f"Q: {question}\nA: {answer}",
                              footer=f"Number of questions: {len(self.questionFiles)}",
                              color=0x00aa00
                              )
        await ctx.send(embed = embed)

    @commands.command()
    async def remove(self, ctx):
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
