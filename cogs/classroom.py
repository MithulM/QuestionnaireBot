import discord
from discord.ext import commands
import asyncio
import random
import math

class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.questionFiles = {}
        self.client = client
        self.MAX_Q = 25
        self.userPoints = {}
        self.defaultChannel = None
        self.time = 10
        self.notAnswerd = set()
        self.answer = ""
        self.point = 1000
        self.endGame = False

    @commands.command()
    async def start(self, ctx):
        if len(self.userPoints) == 0 or len(self.questionFiles) == 0:
            await ctx.send(embed = discord.Embed(title = "There are no players or questions.", color = 0x00aa00))
            return
        channel = await ctx.guild.create_text_channel('classroom-game')
        self.defaultChannel = channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        for user in self.userPoints:
            await channel.set_permissions(ctx.message.guild.get_member(user), send_messages=True)
        i = 1
        while self.questionFiles:
            randQ, randA = random.choice(list(self.questionFiles.items()))
            self.point = 1000
            del self.questionFiles[randQ]
            embed = discord.Embed(title=f"Question **#{i}**", description=randQ, color=0x00aa00)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/two-oclock_1f551.png")
            await channel.send(embed=embed)
            if self.endGame:
                break
            self.notAnswerd = set(self.userPoints.keys())
            self.answer = randA
            await asyncio.sleep(self.time)
            if self.endGame:
                break
            embed = discord.Embed(title=f"Time's up!", description="The answer was: " + randA, color=0x00aa00)
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/grinning-face-with-sweat_1f605.png")
            await channel.send(embed=embed)
            if self.endGame:
                break
            await asyncio.sleep(1)
            if self.endGame:
                break
            embed = discord.Embed(title=f"Scores", description=self.points(ctx), color=0x00aa00)
            await asyncio.sleep(1)
            if self.endGame:
                break
            await channel.send(embed=embed)
            if self.endGame:
                break
            i += 1
        embed = discord.Embed(title=f"The game has ended. Deleting channel in 5 seconds", color=0x00aa00)
        embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/waving-hand_1f44b.png")
        await channel.send(embed=embed)
        await asyncio.sleep(5)
        self.questionFiles = {}
        self.userPoints = {}
        self.gameChannel = None
        await channel.delete()

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.defaultChannel != None and self.defaultChannel.id == message.channel.id:
            if not message.author.bot and message.content[0] != "!":
                if message.author.id in self.notAnswerd:
                    if self.answer.lower() == message.content.lower():
                        await message.author.send(f"{message.content} is **correct**")
                        self.userPoints[message.author.id] += self.point
                        self.point = math.ceil(self.point * .85)
                        self.notAnswerd.remove(message.author.id)
                    else:
                        await message.author.send(f"{message.content} is **incorrect,**\nTry again")
                if not message.author.bot:
                    await message.delete()

    @commands.command()
    async def abort(self, ctx):
        self.endGame = True
        await ctx.send(embed = discord.Embed(title="Game aborted", color=0x00aa00))

    @commands.command()
    async def timer(self, time):
        self.time = int(time)

    @commands.command()
    async def add(self, ctx, question, answer, *a):
        if len(self.questionFiles) > self.MAX_Q - 1:
            embed = discord.Embed(title=f"Can't add anymore questions",
                                  description=f"Max number of questions reached",
                                  footer=f"Number of questions: **{len(self.questionFiles)}**",
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/face-with-monocle_1f9d0.png")
        else:
            if question in self.questionFiles:
                self.questionFiles[question] = answer
                embed = discord.Embed(title=f'Updated question',
                                      description=f"**New Q:** {question}\n**New A:** {answer}",
                                      footer=f"Number of questions: **{len(self.questionFiles)}**",
                                      color=0x00aa00
                                      )
                embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/ok-hand_1f44c.png")
            else:
                self.questionFiles[question] = answer
                embed = discord.Embed(title=f'Question added',
                                      description=f"**Q:** {question}\n**A:** {answer}",
                                      footer=f"Number of questions: **{len(self.questionFiles)}**",
                                      color=0x00aa00
                                      )
                embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/check-mark-button_2705.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def remove(self, ctx, all=""):
        if len(self.questionFiles) == 0:
            embed = discord.Embed(title=f'No questions to remove',
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/worried-face_1f61f.png")
            await ctx.send(embed=embed)
            return
        question = []
        questions = ""
        for i, (k, v) in enumerate(self.questionFiles.items()):
            question.append(k)
            questions += f"{i + 1}) {k}\n"
        if all == "":
            embed = discord.Embed(title=f'Which question would you like to remove?',
                                  description="Example: **!remove 5**\nPlease enter a number to remove:\n" + questions,
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/twitter/259/thinking-face_1f914.png")
            await ctx.send(embed=embed)
        elif 0 <= int(all) - 1 < len(question):
            del self.questionFiles[question[int(all) - 1]]
            embed = discord.Embed(title=f'Removed question **#{all}**',
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/thumbs-up_1f44d.png")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f'Please enter a **valid index** to remove',
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/pouting-face_1f621.png")
            await ctx.send(embed=embed)

    @commands.command()
    async def showQ(self, ctx):
        if len(self.questionFiles) == 0:
            embed = discord.Embed(title=f'There are no questions',
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/cold-face_1f976.png")
        else:
            embed = discord.Embed(title=f'Questions & answers:',
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
            embed = discord.Embed(title=f'No party members',
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/sneezing-face_1f927.png")
        else:
            embed = discord.Embed(title=f'Party members:',
                              description = string,
                              color=0x00aa00
                              )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/partying-face_1f973.png")
        await ctx.send(embed=embed)

    def points(self, ctx):
        string = ""
        for k, v in sorted(self.userPoints.items(), key = lambda x: x[1], reverse=True):
            string += f"**{ctx.message.guild.get_member(k)}**: __{v}__\n"
        return string

    @commands.command()
    async def join(self, ctx):
        username = ctx.message.author.name + "#" + ctx.message.author.discriminator
        self.userPoints[ctx.message.author.id] = 0
        embed = discord.Embed(title=f'User added',
                              description=f"**User:** {username}\n",
                              color=0x00aa00
                              )
        num = random.randint(0, 100)
        if num < 20:
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/cowboy-hat-face_1f920.png")
        elif num < 40:
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/disguised-face_1f978.png")
        elif num < 60:
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/nerd-face_1f913.png")
        elif num < 80:
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/robot_1f916.png")
        else:
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/alien_1f47d.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        userid = ctx.message.author.id
        if userid in self.userPoints:
            del self.userPoints[ctx.message.author.id]
            embed = discord.Embed(title=f'User left',
                                  description=f"**User:** {ctx.message.guild.get_member(userid)}\n",
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/loudly-crying-face_1f62d.png")
        else:
            embed = discord.Embed(title=f'You are not in the party!',
                                  color=0x00aa00
                                  )
            embed.set_thumbnail(url="https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/72/twitter/259/grimacing-face_1f62c.png")
        await ctx.send(embed=embed)

    def questionOutput(self):
        string = ""
        for k, v in self.questionFiles.items():
            string += f"**Q:** {k}\n**A:** {v}\n\n"
        return string

    @commands.command()
    async def loadQ(self, ctx, spliting, *a):
        for i in a:
            q, ans = i.split(spliting)
            await self.add(ctx, q, ans)

    @commands.command()
    async def help(self, ctx):
        string = ""
        string += "**join**\n Adds you to the party \n"
        string += "**leave**\n Removes you from the party \n"
        string += "**party**\n Displays all party members \n\n"
        string += "**add**\n Adds question and answer to the list \n"
        string += "**remove**\n Removes question and answer from the list \n"
        string += "**showQ**\n Displays list of all questions\n\n"
        string += "**start**\n Starts the game\n"
        string += "**abort**\n Ends the game\n\n"
        string += "**timer**\n Sets delay for showing the answers\n"
        string += "**loadQ**\n Separates question from answer\n"
        embed = discord.Embed(title=f'Commands',
                              description=string,
                              color=0x0182ff
                              )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(BlackBoard(client))
