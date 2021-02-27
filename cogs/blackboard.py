import discord
from discord.ext import commands


class BlackBoard(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    def addQuestion(self, ctx):
        pass



def setup(client):
    client.add_cog(BlackBoard(client))
