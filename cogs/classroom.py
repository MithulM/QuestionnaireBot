import discord
from discord.ext import commands
import asyncio
import random


class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.questionFiles = {}
        self.client = client
        self.MAX_Q = 5
        self.userPoints = {}

    @commands.command()
    async def startGame(self, ctx):
        if len(self.userPoints) == 0 or len(self.questionFiles) == 0:
            await ctx.send(embed = discord.Embed(title = "There are no players or questions in game.", color = 0x00aa00))
            return
        channel = await ctx.guild.create_text_channel('classroom-game-channel')
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        for user in self.userPoints:
            await channel.set_permissions(ctx.message.guild.get_member(user), send_messages=True)
        i = 1
        while self.questionFiles:
            randQ, randA = random.choice(list(self.questionFiles.items()))
            del self.questionFiles[randQ]
            embed = discord.Embed(title=f"Question #{i}", description=randQ, color=0x00aa00)
            await channel.send(embed=embed)
            await asyncio.sleep(3)
            embed = discord.Embed(title=f"Times up!!", description="The answer was: " + randA, color=0x00aa00)
            await channel.send(embed=embed)
            await asyncio.sleep(1)
            embed = discord.Embed(title=f"Scores", description=self.points(ctx), color=0x00aa00)
            await asyncio.sleep(1)
            await channel.send(embed=embed)
            i += 1
        embed = discord.Embed(title=f"Game has ended.", color=0x00aa00)
        await channel.send(embed=embed)
        self.questionFiles = {}
        self.userPoints = {}
        # await channel.delete()

    @commands.command()
    async def add(self, ctx, question, answer, *a):
        if len(self.questionFiles) > self.MAX_Q - 1:
            embed = discord.Embed(title=f"Can't add anymore question.",
                                  description=f"Maximum number of questions reached",
                                  footer=f"Number of questions: {len(self.questionFiles)}",
                                  color=0x00aa00
                                  )
        else:
            if question in self.questionFiles:
                self.questionFiles[question] = answer
                embed = discord.Embed(title=f'Updated question',
                                      description=f"Old Q: {question}\nNew A: {answer}",
                                      footer=f"Number of questions: {len(self.questionFiles)}",
                                      color=0x00aa00
                                      )
            else:
                self.questionFiles[question] = answer
                embed = discord.Embed(title=f'Question added',
                                      description=f"Q: {question}\nA: {answer}",
                                      footer=f"Number of questions: {len(self.questionFiles)}",
                                      color=0x00aa00
                                      )
        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, all=""):
        if len(self.questionFiles) == 0:
            embed = discord.Embed(title=f'No questions to remove :slight_frown:',
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
            await ctx.send(embed=embed)
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

    @commands.command()
    async def showQ(self, ctx):
        if len(self.questionFiles) == 0:
            embed = discord.Embed(title=f'There are no questions. :slight_frown:',
                                  color=0x00aa00
                                  )
        else:
            embed = discord.Embed(title=f'All questions & answers',
                                  description=self.questionOutput(),
                                  color=0x00aa00
                                  )
        await ctx.send(embed=embed)

    @commands.command()
    async def party(self, ctx):
        string = ""
        for k, v in self.userPoints.items():
            string += f"{ctx.message.guild.get_member(k)} \n"
        if string == "":
            embed = discord.Embed(title=f'No party members  :slight_frown:',
                                  color=0x00aa00
                                  )
        else:
            embed = discord.Embed(title=f'Party members: ',
                              description = string,
                              color=0x00aa00
                              )
        await ctx.send(embed=embed)

    def points(self, ctx):
        string = "Player: Points\n"
        for k, v in self.userPoints.items():
            string += f"{ctx.message.guild.get_member(k)}: {v}\n"
        return string

    @commands.command()
    async def join(self, ctx):
        username = ctx.message.author.name + "#" + ctx.message.author.discriminator
        self.userPoints[ctx.message.author.id] = 0
        embed = discord.Embed(title=f'User added',
                              description=f"User: {username}\n Points: 0",
                              color=0x00aa00
                              )
        await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        userid = ctx.message.author.id
        if userid in self.userPoints:
            del self.userPoints[ctx.message.author.id]
            embed = discord.Embed(title=f'User left',
                                  description=f"User: {ctx.message.guild.get_member(userid)}\n",
                                  color=0x00aa00
                                  )
        else:
            embed = discord.Embed(title=f'Seems like you are not in the party.',
                                  color=0x00aa00
                                  )
        await ctx.send(embed=embed)

    def questionOutput(self):
        string = ""
        for k, v in self.questionFiles.items():
            string += f"Q: {k}\nA: {v}\n\n"
        return string


def setup(client):
    client.add_cog(BlackBoard(client))
