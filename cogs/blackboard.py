import discord
from collections import defaultdict
from discord.ext import commands

class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.userPoints = {}
        self.questionFiles = {}
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

    def line(self, ctx):
        string = ""
        for k, v in self.questionFiles.items():
            string += f"Q: {k}\n A: {v}\n"
        return string

    @commands.command()
    async def show(self, ctx):
        embed = discord.Embed(title=f'All questions & answers',
                              description= self.line(ctx),
                              color=0x00aa00
                              )
        await ctx.send(embed=embed)

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
        username = ctx.message.author.name + "#" + ctx.message.author.discriminator
        self.userPoints[username] = 0
        embed = discord.Embed(title=f'User added',
                              description=f"User: {username}\n Points: 0",
                              color=0x00aa00
                              )
        await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        username = ctx.message.author.name + "#" + ctx.message.author.discriminator
        del self.userPoints[username]
        embed = discord.Embed(title=f'User left',
                              description=f"User: {username}\n",
                              color=0x00aa00
                              )
        await ctx.send(embed=embed)

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
