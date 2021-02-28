import discord
from collections import defaultdict
from discord.ext import commands


class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.questionFiles = {}
        self.client = client
        self.MAXQ = 5
        self.userPoints = {}

    @commands.command()
    async def add(self, ctx, question, answer, *a):
        if len(self.questionFiles) > self.MAXQ - 1:
            embed = discord.Embed(title=f"Can't add anymore question.",
                                  description=f"Maximum number of questions reached",
                                  footer=f"Number of questions: {len(self.questionFiles)}",
                                  color=0x00aa00
                                  )
        else:
            try:
                self.questionFiles[question]
                self.questionFiles = answer
                embed = discord.Embed(title=f'Updated question',
                                      description=f"Old Q: {question}\nNew A: {answer}",
                                      footer=f"Number of questions: {len(self.questionFiles)}",
                                      color=0x00aa00
                                      )
            except KeyError:
                self.questionFiles[question] = answer
                embed = discord.Embed(title=f'Question added',
                                      description=f"Q: {question}\nA: {answer}",
                                      footer=f"Number of questions: {len(self.questionFiles)}",
                                      color=0x00aa00
                                      )
        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, all = ""):
        if len(self.questionFiles) == 0:
            embed = discord.Embed(title=f'There are no questions to remove.',
                                  color=0x00aa00
                                  )
            await ctx.send(embed=embed)
            return
        question = []
        questions = ""
        for i, (k, v) in enumerate(self.questionFiles.items()):
            question.append(k)
            questions += f"{i + 1}) {k}\n"
        if all == "":
            embed = discord.Embed(title=f'Which one question do you want to remove?',
                                  description="Example: !remove 5\nPlease enter the number to remove:\n" + questions,
                                  color=0x00aa00
                                  )
            await ctx.send(embed = embed)
        elif 0 <= int(all) - 1 < len(question):
                del self.questionFiles[question[int(all) - 1]]
                embed = discord.Embed(title=f'Removed question at position {all}',
                                      color=0x00aa00
                                      )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'Please enter a valid index to remove',
                                  color=0x00aa00
                                  )
            await ctx.send(embed=embed)

    def line(self, ctx):
        string = ""
        for k, v in self.questionFiles.items():
            string += f"Q: {k}\nA: {v}\n\n"
        return string

    @commands.command()
    async def show(self, ctx):
        if len(self.questionFiles) == 0:
            embed = discord.Embed(title=f'There are no questions.',
                                  color=0x00aa00
                                  )
        else:
            embed = discord.Embed(title=f'All questions & answers',
                              description=self.line(ctx),
                              color=0x00aa00
                              )
        await ctx.send(embed=embed)

    @commands.command()
    async def points(self, ctx):
        string = "Player: Points\n"
        for k, v in self.userPoints.items():
            string += f"{k}: {v}\n"
        embed = discord.Embed(title=f'Points of all players',
                              description=string,
                              color=0x00aa00
                              )
        await ctx.send(embed = embed)

    @commands.command()
    async def startGame(self, ctx):
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
        if username in self.userPoints:
            del self.userPoints[username]
            embed = discord.Embed(title=f'User left',
                                  description=f"User: {username}\n",
                                  color=0x00aa00
                                  )
        else:
            embed = discord.Embed(title=f'Seems like you are not in the party.',
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

    def addPoints(self):
        pass


def setup(client):
    client.add_cog(BlackBoard(client))